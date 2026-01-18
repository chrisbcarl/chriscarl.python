#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
Author:         Chris Carl
Email:          chrisbcarl@outlook.com
Date:           2024-12-29
Description:

core.lib.stdlib.fnmatch is about using the fnmatch module as best I can
core.lib are modules that contain code that is about (but does not modify) the library. somewhat referential to core.functor and core.types.

Updates:
    2024-12-29 - core.lib.stdlib.fnmatch - initial commit
'''

# stdlib imports
from __future__ import absolute_import, print_function, division, with_statement  # , unicode_literals
import os
import sys
import logging
import fnmatch
import fnmatch
from typing import Optional, Union, List, Generator

# third party imports

# project imports
from chriscarl.core.lib.stdlib.os import abspath
from chriscarl.core.lib.stdlib.io import read_text_file
from chriscarl.core.lib.stdlib.typing import isinstance_raise

SCRIPT_RELPATH = 'chriscarl/core/lib/stdlib/fnmatch.py'
if not hasattr(sys, '_MEIPASS'):
    SCRIPT_FILEPATH = os.path.abspath(__file__)
else:
    SCRIPT_FILEPATH = os.path.abspath(os.path.join(sys._MEIPASS, SCRIPT_RELPATH))  # pylint: disable=no-member
SCRIPT_DIRPATH = os.path.dirname(SCRIPT_FILEPATH)
SCRIPT_NAME = os.path.splitext(os.path.basename(__file__))[0]
THIS_MODULE = sys.modules[__name__]
LOGGER = logging.getLogger(__name__)
LOGGER.addHandler(logging.NullHandler())

T_STR_OR_LIST = Optional[Union[str, List[str]]]


def argument_to_fnmatchs(none_str_list):
    # type: (T_STR_OR_LIST) -> List[str]
    fnmatchs = []
    if isinstance(none_str_list, str):
        fnmatchs = [line.strip() for line in none_str_list.splitlines() if line.strip()]
        try:
            fnmatchs = [line.strip() for line in read_text_file(none_str_list).splitlines() if line.strip()]
        except Exception:
            pass
    elif isinstance(none_str_list, list):
        fnmatchs.extend(none_str_list)
    elif none_str_list is None:
        return fnmatchs
    else:
        isinstance_raise(none_str_list, T_STR_OR_LIST)
    return fnmatchs


def walk(root_dirpath, include=None, exclude=None, case_insensitive=True, relpath=False, basename=False):
    # type: (str, T_STR_OR_LIST, T_STR_OR_LIST, bool, bool, bool) -> Generator[str, None, None]
    include_fnmatchs = argument_to_fnmatchs(include)
    exclude_fnmatchs = argument_to_fnmatchs(exclude)

    for dirpath, _, filenames in os.walk(root_dirpath):
        dirpath = dirpath.replace('\\', '/')
        for filename in filenames:
            rel = os.path.relpath(os.path.join(dirpath, filename), root_dirpath).replace('\\', '/')
            bname = os.path.basename(filename)
            if relpath:
                filepath = rel
            elif basename:
                filepath = bname
            else:
                filepath = abspath(dirpath, filename)

            if exclude_fnmatchs:
                if case_insensitive:
                    if any(fnmatch.fnmatch(rel, pat) for pat in exclude_fnmatchs):
                        continue
                else:
                    if any(fnmatch.fnmatchcase(rel, pat) for pat in exclude_fnmatchs):
                        continue
            if include_fnmatchs:
                if case_insensitive:
                    if not any(fnmatch.fnmatch(rel, pat) for pat in include_fnmatchs):
                        continue
                else:
                    if not any(fnmatch.fnmatchcase(rel, pat) for pat in include_fnmatchs):
                        continue
            yield filepath
