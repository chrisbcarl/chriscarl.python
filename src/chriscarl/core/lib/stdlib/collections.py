#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
Author:         Chris Carl
Email:          chrisbcarl@outlook.com
Date:           2024-11-26
Description:

core.lib.stdlib.collections is mostly to do with dictionaries and ordered dicts
core.lib are modules that contain code that is about (but does not modify) the library. somewhat referential to core.functor and core.types.

Updates:
    2024-11-26 - core.lib.stdlib.collections - initial commit
'''

# stdlib imports
from __future__ import absolute_import, print_function, division, with_statement  # , unicode_literals
import os
import sys
import logging
import collections
from typing import Mapping, Any

# third party imports

# project imports

SCRIPT_RELPATH = 'chriscarl/core/lib/stdlib/collections.py'
if not hasattr(sys, '_MEIPASS'):
    SCRIPT_FILEPATH = os.path.abspath(__file__)
else:
    SCRIPT_FILEPATH = os.path.abspath(os.path.join(sys._MEIPASS, SCRIPT_RELPATH))  # pylint: disable=no-member
SCRIPT_DIRPATH = os.path.dirname(SCRIPT_FILEPATH)
SCRIPT_NAME = os.path.splitext(os.path.basename(__file__))[0]
THIS_MODULE = sys.modules[__name__]
LOGGER = logging.getLogger(__name__)
LOGGER.addHandler(logging.NullHandler())


def namedtuple_with_defaults(typename, field_names, default_values=()):
    # https://stackoverflow.com/questions/11351032/namedtuple-and-default-values-for-optional-keyword-arguments
    T = collections.namedtuple(typename, field_names)
    T.__new__.__defaults__ = (None, ) * len(T._fields)
    if isinstance(default_values, Mapping):
        prototype = T(**default_values)
    else:
        prototype = T(*default_values)
    T.__new__.__defaults__ = tuple(prototype)
    return T


def unordered_dict(ordered):
    # type: (collections.OrderedDict) -> dict|list|Any
    if isinstance(ordered, dict):
        ret = {}
        for k, v in ordered.items():
            ret[k] = unordered_dict(v)
    elif isinstance(ordered, (list, set, tuple)):
        ret = [unordered_dict(k) for k in ordered]
    else:
        ret = ordered

    return ret


def compare_ordered_dict(ordered, unordered):
    # type: (collections.OrderedDict, dict) -> bool
    return unordered_dict(ordered) == unordered
