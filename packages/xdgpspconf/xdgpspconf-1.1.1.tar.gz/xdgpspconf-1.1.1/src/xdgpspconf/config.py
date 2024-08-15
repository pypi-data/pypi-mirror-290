#!/usr/bin/env python3
# -*- coding: utf-8; mode: python; -*-
# Copyright © 2021-2024 Pradyumna Paranjape
#
# This file is part of xdgpspconf.
#
# xdgpspconf is free software: you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# xdgpspconf is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public License
# along with xdgpspconf. If not, see <https://www.gnu.org/licenses/>. #
r"""
Special case of configuration, where base object is a file

\*\*kwargs
------------
Following kwargs are defined for some functions as indicated.

cname : str
    name of config file
ext : str | list[str]
    extension restriction filter(s)
trace_pwd : Path | os.PathLike
    when supplied, walk up to mountpoint or project-root and inherit all
    locations that contain __init__.py. Project-root is identified by
    existence of ``setup.py`` or ``setup.cfg``. Mountpoint returns ``True``
    for :meth:`Path.is_mount` in unix or is Drive in Windows. If ``True``,
    walk from ``$PWD``.
\*\*kwargs : dict[str, Any]
    remaining kwargs of :py:meth:`xdgpspconf.utils.fs_perm`: passed on

Order
-----
Most to least- dominant (least to most global) order.

- custom supplied, optional
- traced ancestry, optional
- XDG specification paths
- Paths that are improper according to XDG, optional
- root
- shipped

"""

import os
from pathlib import Path
from typing import Any

from xdgpspconf.base import BaseDisc
from xdgpspconf.config_io import parse_rc, write_rc
from xdgpspconf.errors import FailedWriteError
from xdgpspconf.utils import PERMARGS, fs_perm

CONF_EXT = '.yml', '.yaml', '.json', '.toml', '.conf', '.ini', ''
"""Extensions that are supported (parsed) by this module."""


class ConfDisc(BaseDisc):
    r"""
    CONF DISCoverer.

    Each location is config `FILE`, NOT `directory` as with :class:`BaseDisc`.

    See Also
    --------
    :class:`xdgpspconf.base.DataDisc`
    :class:`xdgpspconf.base.StateDisc`

    Parameters
    ----------
    project : str
        project under consideration
    shipped : Path
        ``namespace.__file__``
    form : list[str] | str, optional
        default configuration format. see :attr:`ConfDisc.form`
    \*\*permargs : dict[str, Any]
        all (arguments to :meth:`os.access`) are passed to
        :meth:`xdgpspconf.utils.fs_perm`

    """

    def __init__(self,
                 project: str,
                 shipped: Path | os.PathLike | None = None,
                 form: str | list[str] | None = None,
                 **permargs):
        super().__init__(project, base='config', shipped=shipped, **permargs)
        self.form: str | list[str] | None = form
        """
        Allowed conifiguration formats.

        Effect on methods
        -----------------

        Reader methods
        ~~~~~~~~~~~~~~
        - :meth:`read_config`
        - :meth:`flat_config`

        If ``None``, reader methods set it to all found configuration formats.
        Else, reader methods try to read only these formats.
        If parameter ``form`` is supplied, it determines the format,
        overriding this attribute.
        If this learning is not desired, set this attribute to empty list [].

        Writer methods
        ~~~~~~~~~~~~~~
        - :meth:`write_config`

        If ``None``,  writes in the default (yaml) format.
        If `str`, :meth:`write_config` writes in this format.
        If `list`, :meth:`write_config` writes in the first format in the list.
        If parameter ``form`` is supplied, it determines the format,
        overriding this attribute.
        """

    @property
    def locations(self) -> dict[str, list[Path]]:  # pragma: no cover
        # guard for inherited property
        return self.get_locations('config')

    @property
    def user_xdg_loc(self) -> list[Path]:  # pragma: no cover
        # guard for inherited property
        return self.dir_cnames(super().user_xdg_loc)

    @property
    def improper_loc(self) -> list[Path]:  # pragma: no cover
        # guard for inherited property
        return self.dir_cnames(super().improper_loc)

    @property
    def root_xdg_loc(self) -> list[Path]:  # pragma: no cover
        # guard for inherited property
        return self.dir_cnames(super().root_xdg_loc)

    def __repr__(self) -> str:
        return super().__repr__() + '\n' + f'form: {self.form}'

    def get_locations(self, cname: str = 'config') -> dict[str, list[Path]]:
        """
        XDG, improper, root, shipped locations with custom config file name.

        Parameters
        ----------
        cname : str
            name of configuration file

        Returns
        -------
        dict[str, list[Path]]
            named dictionary containing respective list of Paths
        """
        shipped_loc = [(self.shipped / cname).with_suffix(ext)
                       for ext in CONF_EXT] if self.shipped else []

        return {
            'user_loc': self.dir_cnames(super().user_xdg_loc, cname),
            'improper': self.dir_cnames(super().improper_loc, cname),
            'root_loc': self.dir_cnames(super().root_xdg_loc, cname),
            'shipped': shipped_loc
        }

    def dir_cnames(self, parents: list[Path], cname: str = 'config'):
        """
        Generate potential config file names in parent locations.

        Parameters
        ----------
        parents : list[Path]
            parent file locations
        cname : str
            standard config file name

        Returns:
            list of potential file paths
        """
        config = []
        for loc in parents:
            for ext in CONF_EXT:
                config.append((loc / cname).with_suffix(ext))
                config.append(loc.with_suffix(ext))
            config.append(loc / (self.project + 'rc'))
            config.append(loc.parent / (loc.name + 'rc'))
        return config

    def trace_ancestors(self, child_dir: Path) -> list[Path]:
        """
        Walk up to nearest mountpoint or project root.

        - collect all directories containing __init__.py \
          (assumed to be source directories)
        - project root is directory that contains ``setup.cfg``
          or ``setup.py``
        - mountpoint is a unix mountpoint or windows drive root
        - I **AM** my 0th ancestor

        Parameters
        ----------
        child_dir : Path
            walk ancestry of `this` directory

        Returns
        -------
        list[Path]
            list of Paths to ancestor configs: First directory is most dominant
        """
        config: list[Path] = []
        pedigree = super().trace_ancestors(child_dir)
        if child_dir not in pedigree:  # pragma: no cover
            pedigree = [child_dir, *pedigree]
        config.extend(
            (config_dir / f'.{self.project}rc' for config_dir in pedigree))

        if pedigree:
            for setup in ('pyproject.toml', 'setup.cfg'):
                if (pedigree[-1] / setup).is_file():
                    config.append(pedigree[-1] / setup)
        return config

    def get_conf(self,
                 dom_start: bool = True,
                 improper: bool = False,
                 custom: Path | None = None,
                 **kwargs) -> list[Path]:
        r"""
        Get discovered configuration files.

        Parameters
        ----------
        dom_start : bool
            when ``False``, end with most dominant
        improper : bool
            include improper locations such as *~/.project*
        custom : Path
            custom location
        **kwargs : dict[str, Any]
            cname : str
                name of configuration file. Default: 'config'
            trace_pwd : Path | os.PathLike]
                when supplied, walk up to mountpoint or project-root and
                inherit all locations that contain ``__init__.py``.
                Project-root is identified by existence of ``setup.py`` or
                ``setup.cfg``.  Mountpoint returns ``True``
                for :meth:`Path.is_mount` in unix or is Drive in Windows. If
                ``True``, walk from ``$PWD``.
            \*\*permargs : dict[str, Any]
                passed on to :meth:`xdgpspconf.utils.fs_perm`

        Returns
        -------
        list[Path]
            configuration paths with permissions [dom_start]
        """
        # NOTE: order of following statements IS important
        dom_order: list[Path] = []

        if custom is not None:
            # assume existence and proceed
            dom_order.append(Path(custom))

        rc_val = os.environ.get(self.project.upper() + 'RC')
        if rc_val is not None:  # pragma: no cover
            if not Path(rc_val).is_file():
                raise FileNotFoundError(
                    f'RC configuration file: {rc_val} not found')
            dom_order.append(Path(rc_val))

        trace_pwd = kwargs.get('trace_pwd')
        if trace_pwd is True:
            trace_pwd = Path.cwd()
        if trace_pwd:
            inheritance = self.trace_ancestors(Path(trace_pwd))
            dom_order.extend(inheritance)

        locations = self.get_locations(kwargs.get('cname') or 'config')

        # xdg user locations
        dom_order.extend(locations['user_loc'])

        # deprecated locations
        if improper:
            dom_order.extend(locations['improper'])

        # read-only locations
        dom_order.extend(locations['root_loc'])
        dom_order.extend(locations['shipped'])

        permargs = {key: val for key, val in kwargs.items() if key in PERMARGS}
        permargs = self.permargs | permargs
        dom_order = list(filter(lambda x: fs_perm(x, **permargs), dom_order))
        if dom_start:
            return dom_order
        return list(reversed(dom_order))

    def safe_config(self,
                    ext: str | list[str] | None = None,
                    dom_start: bool = True,
                    mode: str | int = 2,
                    **kwargs) -> list[Path]:
        r"""
        Locate safe writeable paths of configuration files.

        - Doesn't care about accessibility or existence of locations.
        - User must catch:
            - ``PermissionError``
            - ``IsADirectoryError``
            - ``FileNotFoundError``
        - Improper locations (*~/.project*) are deliberately dropped

        .. tip::
            For global storage, use

            .. code-block:: python

                safe_config(..., dom_start=Flase, ...)


        Parameters
        ----------
        ext : str | list[str]
            extension filter(s)
        dom_start : bool
            when ``False``, end with most dominant
        mode : str | int
            permission mode to check
        **kwargs : dict[str, Any]
            custom : Path | os.PathLike
                custom location
            cname : str
                name of configuration file. Default: 'config'
            trace_pwd : Path | os.PathLike | bool
                when supplied, walk up to mountpoint or project-root and
                inherit all locations that contain ``__init__.py``.
                Project-root is identified by existence of ``setup.py`` or
                ``setup.cfg``. Mountpoint returns ``True`` for
                :meth:`Path.is_mount` in unix or is Drive in Windows. If
                ``True``, walk from ``$PWD``.
            \*\*permargs : dict[str, Any]
                passed on to :meth:`xdgpspconf.utils.fs_perm`


        Returns
        -------
            Safe configuration locations (existing and prospective)

        """
        # filter private locations
        private_locs = ['site-packages', 'venv', '/etc', 'setup', 'pyproject']
        if self.shipped is not None:
            private_locs.append(str(self.shipped))
        safe_paths = filter(
            lambda x: not any(private in str(x) for private in private_locs),
            self.get_conf(dom_start=dom_start, mode=mode, **kwargs))
        if ext is None:
            return list(safe_paths)

        # filter extensions
        if isinstance(ext, str):
            ext = [ext]
        return list(
            filter(
                lambda x: x.suffix in ext,  # type: ignore [arg-type]
                safe_paths))

    def read_config(self,
                    flatten: bool = False,
                    dom_start: bool = True,
                    form: list[str] | str | None = None,
                    **kwargs) -> dict[Path, dict[str, Any]]:
        r"""
        Locate Paths to standard directories and parse config.

        Parameters
        ----------
        flatten : bool
            superimpose configurations to return the final outcome
        dom_start : bool
            when ``False``, end with most dominant
        form : list[str] | str, optional
            default configuration format. see :attr:`ConfDisc.form`
        **kwargs : dict[str, Any]
            custom : Path | os.PathLike
                custom location
            cname : str
                name of configuration file. Default: 'config'
            trace_pwd : Path | os.PathLike | bool
                when supplied, walk up to mountpoint or project-root and
                inherit all locations that contain ``__init__.py``.
                Project-root is identified by existence of ``setup.py`` or
                ``setup.cfg``. Mountpoint returns ``True`` for
                :meth:`Path.is_mount` in unix or is Drive in Windows. If
                ``True``, walk from ``$PWD``.
            improper : bool
                include improper locations such as *~/.project*
            \*\*permargs : dict[str, Any]
                passed on to :meth:`xdgpspconf.utils.fs_perm`

        Returns
        -------
        dict[str, Any]
            parsed configuration from each available file

        Raises
        ------
        BadConf
            Bad configuration file format

        Examples
        --------
        >>> mypy_conf = ConfDisc('mypy')
        >>> mypy_conf.read_config()
        {PosixPath('~/.config/mypy/config'): {'mypy': {'mypy-pandas': {
                        'disable_error_code': 'arg-type, assignment'}}}}
        """
        kwargs['mode'] = kwargs.get('mode', 4)
        avail_confs: dict[Path, dict[str, Any]] = {}
        rc_forms: list[str] = []
        form = form or self.form
        # load configs from oldest ancestor to current directory
        for config in self.get_conf(dom_start=dom_start, **kwargs):
            try:
                avail_confs[config], read_form = parse_rc(config,
                                                          project=self.project,
                                                          form=form)
                if read_form:
                    rc_forms.append(read_form)
            except (PermissionError, FileNotFoundError, IsADirectoryError):
                pass

        if self.form is None:
            self.form = list(set(rc_forms))

        if not flatten:
            return avail_confs

        super_config: dict[str, Any] = {}
        for flat_config in reversed(list(avail_confs.values())):
            super_config.update(flat_config)
        return {Path.cwd(): super_config}

    def flat_config(self,
                    dom_start: bool = True,
                    form: list[str] | str | None = None,
                    **kwargs) -> dict[str, Any]:
        r"""
        Locate Paths to standard directories and parse config.

        Parameters
        ----------
        dom_start : bool
            when ``False``, end with most dominant
        form : list[str] | str, optional
            default configuration format. see :attr:`ConfDisc.form`
        **kwargs : dict[str, Any]
            custom : Path | os.PathLike
                custom location
            cname : str
                name of configuration file. Default: 'config'
            trace_pwd : Path | os.PathLike | bool
                when supplied, walk up to mountpoint or project-root and
                inherit all locations that contain ``__init__.py``.
                Project-root is identified by existence of ``setup.py`` or
                ``setup.cfg``. Mountpoint returns ``True`` for
                :meth:`Path.is_mount` in unix or is Drive in Windows. If
                ``True``, walk from ``$PWD``.
            improper : bool
                include improper locations such as *~/.project*
            \*\*permargs : dict[str, Any]
                passed on to :meth:`xdgpspconf.utils.fs_perm`

        Returns
        -------
        dict[str, Any]
            parsed configuration from each available file

        Raises
        ------
        BadConf
            Bad configuration file format

        Examples
        --------
        >>> mypy_conf = ConfDisc('mypy')
        >>> mypy_conf.flat_config()
        {'mypy': {'mypy-pandas': {'disable_error_code': 'arg-type, assignment'}}}
        """
        return (list(
            self.read_config(flatten=True,
                             dom_start=dom_start,
                             form=form,
                             **kwargs).values()))[0]

    def write_config(self,
                     data: dict[str, Any],
                     force: str = 'fail',
                     dom_start: bool = True,
                     form: str | None = None,
                     **kwargs) -> Path:
        """
        Write data to the most global safe configuration file.

        .. tip::
            For global storage, use

            .. code-block:: python

                write_config(..., dom_start=Flase, ...)

        Parameters
        ----------
        data : dict[str, Any]
            serial data to save
        dom_start: when ``False``, end with most dominant
        form : {'yaml', 'json', 'toml', 'ini', 'conf', 'cfg'}
            configuration format see :attr:`ConfDisc.form`
        force: force overwrite {'overwrite','update','fail'}
        **kwargs : dict[str, Any]
            all are passed to :meth:`safe_config`


        Returns
        -------
        Path
            configuration was written here

        Raises
        ------
        FailedWriteError
            Error thrown by last write attempt to write.

        Examples
        --------
        >>> mypy_conf = ConfDisc('mypy')
        >>> mypy_conf_data = {'mypy-pandas':
                {'disable_error_code': 'arg-type, assignment'}}
        >>> mypy_conf.write_config(mypc_conf_data,
                                   cname='config',
                                   ext='',
                                   form='ini')
        PosixPath('/home/pradyumna/.config/mypy/config')

        """
        raise_err: (PermissionError | IsADirectoryError | FileNotFoundError
                    ) = FileNotFoundError('Could not determine config path.')
        if not form:
            if self.form:
                if isinstance(self.form, list):
                    form = self.form[0]
                else:
                    form = self.form

        for config in self.safe_config(dom_start=dom_start, **kwargs):
            try:
                if write_rc(data, config, form=form, force=force):
                    return config
            except (PermissionError, IsADirectoryError,
                    FileNotFoundError) as err:
                raise_err = err
                continue
        raise FailedWriteError from raise_err
