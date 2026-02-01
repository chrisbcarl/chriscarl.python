#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
Author:         Chris Carl
Email:          chrisbcarl@outlook.com
Date:           2024-11-26
Description:

core.types.str is probably badly named and should be "string" but either sucks, so i'll go with this one.
core.types are modules that pertain to data structures, algorithms, conversions. non-self-referential, low-import, etc.

Updates:
    2025-01-31 - core.types.str - added indent
    2025-01-14 - core.types.str - added contains_insensitive and its variants
    2024-12-13 - core.types.str - added strip_unicode
    2024-11-26 - core.types.str - initial commit
'''

# stdlib imports
from __future__ import absolute_import, print_function, division, with_statement  # , unicode_literals
import os
import sys
import logging
from collections import OrderedDict
from typing import Generator, Union, Callable, Iterable

# third party imports

# project imports
from chriscarl.core.types.list import as_list
from chriscarl.core.types.iterable import contains

SCRIPT_RELPATH = 'chriscarl/core/types/str.py'
if not hasattr(sys, '_MEIPASS'):
    SCRIPT_FILEPATH = os.path.abspath(__file__)
else:
    SCRIPT_FILEPATH = os.path.abspath(os.path.join(sys._MEIPASS, SCRIPT_RELPATH))  # pylint: disable=no-member
SCRIPT_DIRPATH = os.path.dirname(SCRIPT_FILEPATH)
SCRIPT_NAME = os.path.splitext(os.path.basename(__file__))[0]
THIS_MODULE = sys.modules[__name__]
LOGGER = logging.getLogger(__name__)
LOGGER.addHandler(logging.NullHandler())

FILE_SIZE_UNITS = OrderedDict({'p': 5, 't': 4, 'g': 3, 'm': 2, 'k': 1})
FILE_SIZE_UNITS['b'] = 0  # so that this is searched last
for k in list(FILE_SIZE_UNITS.keys()):
    if k != 'b':
        v = FILE_SIZE_UNITS[k]
        FILE_SIZE_UNITS['{}b'.format(k)] = v
BYTES_TO_SIZE_UNITS = ['b', 'k', 'm', 'g', 't', 'p']


def find_index(search, text):
    # type: (str, str) -> Generator[int, None, None]
    len_search = len(search)
    for c, char in enumerate(text):
        if c + len_search > len(text):
            break
        if char == search[0] and text[c:c + len_search] == search:
            yield c


def size_to_bytes(size, into='b'):
    # type: (str, str) -> float
    '''
    Description:
        >>> size_to_bytes('512mb') -> 536870912.0
        >>> size_to_bytes('512mb', into='g') -> 0.5
    '''
    into = into.lower()
    if into[-1] == 's':
        into = into[0:-1]
    contains(FILE_SIZE_UNITS, into)

    size = str(size).lower().replace(' ', '')
    for unit in FILE_SIZE_UNITS:
        if unit in size:
            numeric = size.split(unit)[0]
            num = float(numeric)
            exponent = FILE_SIZE_UNITS[unit]
            num_bytes = num * 1024**exponent
            into_magnitude = (1024**FILE_SIZE_UNITS[into])
            return num_bytes / into_magnitude

    return int(size, base=0)


def bytes_to_size(size, upper=False):
    # type: (Union[int, float], bool) -> str
    '''
    # https://github.com/x4nth055/pythoncode-tutorials/blob/master/general/process-monitor/process_monitor.py
    Returns size of bytes in a nice format
    '''
    units = BYTES_TO_SIZE_UNITS if not upper else [e.upper() for e in BYTES_TO_SIZE_UNITS]
    for unit in units:
        if size < 1024:
            return '{:.2f}{}'.format(size, unit)
        size /= 1024
    return ''  # this will never hit


def strip_unicode(text, encoding='utf-8'):
    # type: (str, str) -> str
    '''
    Description:
        wanna get rid of pesky shit like '\\u0026' or '\x26' which is just an &? then this is for u.
        TODO: chr(0x26) == '&' so maybe some regex replacement is faster.
    '''
    return text.encode(encoding).decode(encoding)


def contains_insensitive(text, token_or_tokens, exc=False, func=any):
    # type: (str, str | list, bool, Callable[[Iterable], bool]) -> bool
    raw_tokens = as_list(token_or_tokens)
    tokens = [str(ele).lower() for ele in raw_tokens]
    return contains(text, tokens, func=func, exc=exc)


def contains_all_insensitive(text, token_or_tokens, exc=False):
    # type: (str, str | list, bool) -> bool
    return contains_insensitive(text, token_or_tokens, exc=exc, func=all)


def contains_any_insensitive(text, token_or_tokens, exc=False):
    # type: (str, str | list, bool) -> bool
    return contains_insensitive(text, token_or_tokens, exc=exc, func=any)


def indent(text, indent='    '):
    return '\n'.join(f'{indent}{line}' for line in text.splitlines())
