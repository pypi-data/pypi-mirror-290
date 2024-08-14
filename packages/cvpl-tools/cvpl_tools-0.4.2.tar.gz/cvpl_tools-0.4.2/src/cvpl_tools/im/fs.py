"""This file provides code for image I/O operations, including multithreaded settings
"""
from __future__ import annotations

import copy
import enum
import json
from typing import Any

import napari
import numpy as np
import cvpl_tools.im.ndblock as cvpl_ndblock
from cvpl_tools.im.ndblock import NDBlock
import dask.array as da
import shutil
import os
from cvpl_tools.fs import ensure_dir_exists as ensure_dir_exists
from cvpl_tools.napari.zarr import add_ome_zarr_array_from_path


class ImageFormat(enum.Enum):
    NUMPY = 0
    DASK_ARRAY = 1
    NDBLOCK = 2


def save(file: str, im):
    """Save an image object into given path

    Supported im object types:
    - np.ndarray
    - dask.Array
    - cvpl_tools.im.ndblock.NDBlock

    Args:
        file: The full/relative path to the directory to be saved to
        im: Object to be saved
    """
    if isinstance(im, np.ndarray):
        NDBlock.save(file, NDBlock(im))
        fmt = ImageFormat.NUMPY
    elif isinstance(im, da.Array):
        NDBlock.save(file, NDBlock(im))
        fmt = ImageFormat.DASK_ARRAY
    elif isinstance(im, NDBlock):
        NDBlock.save(file, im)
        fmt = ImageFormat.NDBLOCK
    else:
        raise ValueError(f'Unexpected input type im {type(im)}')
    with open(f'{file}/fmt.txt', mode='w') as outfile:
        outfile.write(str(fmt.value))


def load(file: str):
    """Load an image from the given directory.

    The image is one saved by cvpl_tools.im.fs.save()

    Args:
        file: Full path to the directory to be read from

    Returns:
        Recreated image; this method attempts to keep meta and content of the loaded image stays
        the same as when they are saved
    """
    with open(f'{file}/fmt.txt') as outfile:
        fmt = ImageFormat(int(outfile.read()))
    if fmt == ImageFormat.NUMPY:
        im = NDBlock.load(file).arr
    elif fmt == ImageFormat.DASK_ARRAY:
        im = NDBlock.load(file).arr
    elif fmt == ImageFormat.NDBLOCK:
        im = NDBlock.load(file)
    else:
        raise ValueError(f'Unexpected input type im {fmt}')
    return im


def display(file: str, viewer_args: dict):
    """Display an image in the viewer; supports numpy or dask ome zarr image

    The image is one saved by cvpl_tools.im.fs.save()

    Args:
        file: Full path to the directory to be read from
        viewer_args: contains viewer and arguments passed to the viewer's add image functions
    """
    viewer_args = copy.copy(viewer_args)
    viewer: napari.Viewer = viewer_args.pop('viewer')

    with open(f'{file}/fmt.txt') as outfile:
        fmt = ImageFormat(int(outfile.read()))
    if fmt == ImageFormat.NUMPY:
        is_numpy = True
    elif fmt == ImageFormat.DASK_ARRAY:
        is_numpy = False
    elif fmt == ImageFormat.NDBLOCK:
        properties = NDBlock.load_properties(f'{file}/properties.json')
        repr_fmt: cvpl_ndblock.ReprFormat = properties['repr_format']
        if repr_fmt == cvpl_ndblock.ReprFormat.NUMPY_ARRAY:
            is_numpy = True
        elif repr_fmt == cvpl_ndblock.ReprFormat.NUMPY_ARRAY:
            is_numpy = False
        else:
            raise ValueError(f'Image to be displayed can not be a dict of blocks that is {repr_fmt}')

    if is_numpy:
        is_label: bool = viewer_args.pop('is_label', False)
        fn = viewer.add_labels if is_label else viewer.add_image
        im = NDBlock.load(file).arr
        fn(im, **viewer_args)
    else:
        # image saved by NDBlock.save(file)
        add_ome_zarr_array_from_path(viewer, f'{file}/dask_im', use_zip=False, kwargs=viewer_args)


class CachePath:
    def __init__(self, path: str, meta: dict = None):
        """Create a CachePath object that manages meta info about the cache file or directory

        Args:
            path: The path associated with this CachePath object
            meta: The meta information associated with this object; will be automatically inferred
                from the path (only able to do so in some situations) if None is provided
        """
        self._path = path

        if meta is None:
            meta = CachePath.meta_from_filename(os.path.split(path)[1])

        self._meta = meta
        for key in ('is_dir', 'is_tmp', 'cid'):
            assert key in meta, f'Missing key {key}'

    @property
    def path(self):
        return self._path

    @property
    def is_dir(self):
        return self._meta['is_dir']

    @property
    def is_tmp(self):
        return self._meta['is_tmp']

    @property
    def cid(self):
        return self._meta['cid']

    @property
    def meta(self):
        return self._meta

    @staticmethod
    def meta_from_filename(file: str, return_none_if_malform=False) -> dict[str, Any] | None:
        """Retrieve meta information from the path

        Args:
            file: filename of the (existing to planning to be created) CachePath object
            return_none_if_malform: If True, return None instead of throwing error if a malformed
                filename is given

        Returns:
            A dictionary of the meta information
        """
        if file.startswith('file_'):
            is_dir = False
            rest = file[len('file_'):]
        elif file.startswith('dir_'):
            is_dir = True
            rest = file[len('dir_'):]
        else:
            if return_none_if_malform:
                return None
            else:
                raise ValueError(f'path is not expected when parsing is_file: {file}')
        if rest.startswith('tmp_'):
            is_tmp = True
            rest = rest[len('tmp_'):]
        elif rest.startswith('cache_'):
            is_tmp = False
            rest = rest[len('cache_'):]
        else:
            if return_none_if_malform:
                return None
            else:
                raise ValueError(f'path is not expected when parsing is_tmp: {file}')
        return dict(
            is_dir=is_dir,
            is_tmp=is_tmp,
            cid=rest
        )

    @staticmethod
    def filename_form_meta(meta: dict[str, Any]) -> str:
        """obtain filename from the meta dict"""
        s1 = 'dir_' if meta['is_dir'] else 'file_'
        s2 = 'tmp_' if meta['is_tmp'] else 'cache_'
        cid = meta['cid']
        return f'{s1}{s2}{cid}'


class CacheDirectory(CachePath):
    def __init__(self, path: str, remove_when_done: bool = True, read_if_exists: bool = True):
        super().__init__(path, dict(
            is_dir=True,
            is_tmp=remove_when_done,
            cid='_RootDirectory'
        ))
        self.cur_idx = 0
        self.read_if_exists = read_if_exists
        self.children: dict[str, CachePath] = {}

        ensure_dir_exists(path, remove_if_already_exists=False)
        path = self.path
        if self.read_if_exists:
            self.children = CacheDirectory.children_from_path(path)
        else:
            for _ in os.listdir(path):
                raise FileExistsError('when read_if_exists=False, directory must not contain existing files, '
                                      f'please check if any file exists under {path}.')

    def get_children_json(self) -> dict:
        children_json = {}
        for key, child in self.children.items():
            if child.is_dir:
                child: CacheDirectory
                children_json[key] = dict(
                    children=child.get_children_json(),
                    meta=child.meta
                )
            else:
                children_json[key] = meta

    def get_children_str(self):
        return json.dumps(self.get_children_json(), indent=2)

    @staticmethod
    def children_from_path(path: str) -> dict[str, CachePath]:
        """Examine an existing directory path, return recursively all files and directories as """
        children = {}
        for filename in os.listdir(path):
            subpath = f'{path}/{filename}'
            meta = CachePath.meta_from_filename(filename, return_none_if_malform=True)
            if meta is not None:
                if meta['is_dir']:
                    child = CacheDirectory(subpath, remove_when_done=meta['is_tmp'], read_if_exists=True)
                    child.children = CacheDirectory.children_from_path(subpath)
                else:
                    child = CachePath(subpath, meta)
                children[meta['cid']] = child
        return children

    def __getitem__(self, cid: str) -> CachePath | CacheDirectory:
        """Get a CachePath object by its cid"""
        return self.children[cid]

    def __contains__(self, item: str):
        """Checks if an object is cached"""
        return item in self.children

    def cache(self,
              is_dir=False,
              cid: str = None
              ) -> tuple[bool, CachePath | CacheDirectory]:
        """Return a directory that is guaranteed to be empty within the temporary directory

        This is the interface to create new CachePath or CacheDirectory within this directory.
        The directory will not be immediately created but need to be done manually if is_dir=False

        Args:
            is_dir: If False, this creates a subfolder that have no children; if True, this creates
                a CacheDirectory recursively
            cid: If specified, will attempt to find cache if already exists; otherwise a temporary
                cache will be returned

        Returns:
            A tuple (is_cached, CachePath), is_cached giving whether the file is cached or is newly
            created. If is_cached is True, then the user should directly read from the cached file
            instead
        """
        is_tmp = cid is None
        if is_tmp:
            cid = f'_{self.cur_idx}'
            self.cur_idx += 1
        else:
            if cid in self.children:
                return True, self.children[cid]

        meta = dict(
            is_dir=is_dir,
            is_tmp=is_tmp,
            cid=cid
        )
        filename = CachePath.filename_form_meta(meta)
        tmppath = f'{self.path}/{filename}'
        if is_dir:
            cache_path = CacheDirectory(tmppath, is_tmp, self.read_if_exists)
        else:
            cache_path = CachePath(tmppath, meta)
        self.children[cid] = cache_path
        return False, cache_path

    def cache_im(self,
                 fn,
                 cid: str = None,
                 save_fn=save,
                 load_fn=load,
                 viewer_args: dict = None):
        """Caches an image object

        Args:
            fn: Computes the image if it's not already cached
            cid: The cache ID within this directory
            save_fn: fn(file: str, im) Used to save the image to file
            load_fn: fn(file: str) Used to load the image from file
            viewer_args: contains viewer and arguments passed to the viewer's add image functions

        Returns:
            The cached image loaded
        """
        is_cached, cache_path = self.cache(is_dir=False, cid=cid)
        raw_path = cache_path.path
        if not is_cached:
            im = fn()
            save_fn(raw_path, im)

        assert os.path.exists(raw_path), f'Directory should be created at path {raw_path}, but it is not found'
        if viewer_args is None:
            viewer_args = {}
        if viewer_args.get('viewer', None) is not None:
            viewer_args['name'] = viewer_args.get('name', cid)  # name of the image layer is defaulted to cid
            display(raw_path, viewer_args)

        return load_fn(raw_path)

    def remove_tmp(self):
        """traverse all subnodes and self, removing those with is_tmp=True"""
        if self.is_tmp:
            shutil.rmtree(self.path)
        else:
            for ch in self.children.values():
                if ch.is_tmp:
                    shutil.rmtree(ch.path)
                elif ch.is_dir:
                    assert isinstance(ch, CacheDirectory)
                    ch.remove_tmp()

    def __enter__(self):
        """Called using the syntax:

        with CacheDirectory(...) as cache_dir:
            ...
        """
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.remove_tmp()
