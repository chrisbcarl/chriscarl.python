#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
Author:         Chris Carl
Email:          chrisbcarl@chriscarl.com
Date:           2024-11-24
Description:

core.lib.stdlib.os is all about file system traversal
core.lib.stdlib files are for utilities that make use of, but do not modify the stdlib

Updates:
    2026-01-30 - core.lib.stdlib.os - added wait_for_new_file, listdir
    2026-01-25 - core.lib.stdlib.os - added filename
    2026-01-06 - core.lib.stdlib.os - added is_file, is_dir
    2024-12-04 - core.lib.stdlib.os - added as_posix
    2024-11-27 - core.lib.stdlib.os - added walk
    2024-11-26 - core.lib.stdlib.os - added chdir context manager
    2024-11-24 - core.lib.stdlib.os - initial commit
'''

# stdlib imports
from __future__ import absolute_import, print_function, division, with_statement  # , unicode_literals
import os
import sys
import re
import string
import logging
from typing import Generator, Optional, List
import time

# third party imports

# project imports

SCRIPT_RELPATH = 'chriscarl/core/lib/stdlib/os.py'
if not hasattr(sys, '_MEIPASS'):
    SCRIPT_FILEPATH = os.path.abspath(__file__)
else:
    SCRIPT_FILEPATH = os.path.abspath(os.path.join(sys._MEIPASS, SCRIPT_RELPATH))  # pylint: disable=no-member
SCRIPT_DIRPATH = os.path.dirname(SCRIPT_FILEPATH)
SCRIPT_NAME = os.path.splitext(os.path.basename(__file__))[0]
THIS_MODULE = sys.modules[__name__]
LOGGER = logging.getLogger(__name__)
LOGGER.addHandler(logging.NullHandler())


def abspath(*paths):
    # type: (str) -> str
    return os.path.abspath(os.path.expanduser(os.path.join(*paths)))


TEMP_DIRPATH = abspath('C:/temp' if sys.platform == 'win32' else '/tmp')


def dirpath(*paths):
    # type: (str) -> str
    abs_ = abspath(*paths)
    return os.path.dirname(abs_)


def filename(*paths):
    # type: (str) -> str
    pth = paths[-1]
    return os.path.splitext(os.path.basename(pth))[0]


def make_dirpath(*paths):
    dp = abspath(*paths)
    if not os.path.isdir(dp):
        os.makedirs(dp)


def make_file_dirpath(*paths):
    dp = dirpath(*paths)
    if not os.path.isdir(dp):
        os.makedirs(dp)


class chdir(object):
    '''
    >>> with ContextManager('/tmp'):
    ...     os.chdir('/temp)
    '''
    pwd = ''
    _pwd = ''
    mkdir = True

    def __init__(self, pwd, mkdir=True):
        self.pwd = pwd
        self.mkdir = mkdir

    def __enter__(self):
        LOGGER.debug('chdir to   "%s" from "%s"', self.pwd, self._pwd)
        self._pwd = os.getcwd()
        if self.mkdir:
            make_dirpath(self.pwd)
        os.chdir(self.pwd)
        return self

    def __exit__(self, exc_type, exc_value, exc_traceback):
        LOGGER.debug('chdir undo "%s" from "%s"', self._pwd, self.pwd)
        os.chdir(self._pwd)


def walk(root_dirpath, extensions=None, ignore=None, include=None, case_insensitive=True, relpath=False, basename=False):
    # type: (str, Optional[List[str]], Optional[List[str]], Optional[List[str]], bool, bool, bool) -> Generator[str, None, None]
    ignore = ignore or []
    ignore = [ele.replace('\\', '/') for ele in ignore]
    include = include or []
    include = [ele.replace('\\', '/') for ele in include]
    extensions = extensions or []
    for dirpath, _, filenames in os.walk(root_dirpath):
        dirpath = dirpath.replace('\\', '/')
        if ignore and any(re.search(ign, dirpath, flags=re.IGNORECASE if not case_insensitive else 0) for ign in ignore):
            continue
        for filename in filenames:
            if extensions:
                _, ext = os.path.splitext(filename)
                if not any(ext.endswith(ele) for ele in extensions):
                    continue
            rel = os.path.relpath(os.path.join(dirpath, filename), root_dirpath).replace('\\', '/')
            bname = os.path.basename(filename)
            if include and not any(re.search(inc, rel, flags=re.IGNORECASE if not case_insensitive else 0) for inc in include):
                continue
            if ignore and any(re.search(ign, rel, flags=re.IGNORECASE if not case_insensitive else 0) for ign in ignore):
                continue
            if relpath:
                yield rel
            elif basename:
                yield bname
            else:
                yield abspath(dirpath, filename)


def drives():
    # type: () -> List[str]
    '''https://stackoverflow.com/a/34187346'''
    return [d for d in string.ascii_lowercase if os.path.exists('%s:' % d)]


def current_drive():
    # type: () -> str
    return abspath(os.getcwd())[0].lower()


def as_posix(path, wsl=False):
    # type: (str, bool) -> str
    '''
    Description:
        convert any path into a logical posix path.
        C:\\temp and cwd is on the C:\\ drive returns /temp
        D:\\temp and cwd is on the C:\\ drive returns D:/temp
    '''
    path = abspath(path)
    if sys.platform == 'win32':
        if wsl:
            drive = path[0].lower()
            return '/mnt/{}{}'.format(drive, path[2:].replace('\\', '/'))
        if re.match(r'^[a-z]\:', path, flags=re.IGNORECASE):
            cwd = abspath(os.getcwd())
            if path[0].lower() == cwd[0].lower():
                return path[2:].replace('\\', '/')
    else:
        if path[1] == ':':
            return path[2:].replace('\\', '/')
        return path.replace('\\', '/')

    return path.replace('\\', '/')


def is_file(*paths):
    return os.path.isfile(abspath(*paths))


def is_dir(*paths):
    return os.path.isdir(abspath(*paths))


def wait_for_new_file(dirpath, timeout=10):
    # type: (str, int|float) -> str
    dirpath = abspath(dirpath)
    then = time.time()
    files_then = set(os.listdir(dirpath))
    files_now = set(os.listdir(dirpath))
    while files_now == files_then and time.time() - then < timeout:
        files_now = set(os.listdir(dirpath))
        time.sleep(0.1)
    diff = list(files_now.difference(files_then))
    if not diff:
        raise TimeoutError(f'timeout of {timeout}sec waiting for a new file in "{dirpath}"')

    return abspath(diff[0])


def listdir(dirpath):
    # type: (str) -> List[str]
    dirpath = abspath(dirpath)
    return [os.path.join(dirpath, filename) for filename in os.listdir(dirpath)]
