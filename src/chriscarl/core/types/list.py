#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
Author:         Chris Carl
Email:          chrisbcarl@outlook.com
Date:           2024-11-25
Description:

core.types.list is all about these array-lists.
core.types are modules that pertain to data structures, algorithms, conversions. non-self-referential, low-import, etc.

Updates:
    2025-02-16 - core.types.list - FIX: would skip over 0's as not real values...
    2025-01-31 - core.types.list - added rows_to_str_rows
    2025-01-14 - core.types.list - removed contains
    2025-01-01 - core.types.list - added n_sized_chunks and n_chunks
    2024-12-09 - core.types.list - added as_list
    2024-11-25 - core.types.list - initial commit
'''

# stdlib imports
from __future__ import absolute_import, print_function, division, with_statement  # , unicode_literals
import os
import sys
import logging
from typing import List, Union, Callable, Any, Generator, Iterable, Tuple, Optional, Dict

# third party imports

# project imports
from chriscarl.core.lib.stdlib.typing import T_TYPING, isinstance_raise

SCRIPT_RELPATH = 'chriscarl/core/types/list.py'
if not hasattr(sys, '_MEIPASS'):
    SCRIPT_FILEPATH = os.path.abspath(__file__)
else:
    SCRIPT_FILEPATH = os.path.abspath(os.path.join(sys._MEIPASS, SCRIPT_RELPATH))  # pylint: disable=no-member
SCRIPT_DIRPATH = os.path.dirname(SCRIPT_FILEPATH)
SCRIPT_NAME = os.path.splitext(os.path.basename(__file__))[0]
THIS_MODULE = sys.modules[__name__]
LOGGER = logging.getLogger(__name__)
LOGGER.addHandler(logging.NullHandler())


def dedupe(lst):
    # type: (list) -> list
    vals = {line: 1 for line in lst}
    return list(vals.keys())


def find_index(filter, lst):
    # type: (Callable[[Any], bool], list) -> Generator[int, None, None]
    '''
    Description:
        like map and filter, use a lambda to find all of the indexes that meet that lambda
    '''
    for i, x in enumerate(lst):
        if filter(x):
            yield i


def frequency_table(lst):
    # type: (list) -> Union[dict, Any]
    frequency = {}
    for ele in lst:
        if ele not in frequency:
            frequency[ele] = 0
        frequency[ele] += 1
    return frequency


def generate_list_by_frequency(lst, ascending=True):
    # type: (list, bool) -> Generator[Any, None, None]
    frequency = frequency_table(lst)
    for k, v in sorted(frequency.items(), key=lambda tpl: tpl[1], reverse=not ascending):
        yield k


def sorted_list_by_frequency(lst, ascending=True):
    # type: (list, bool) -> List[Any]
    return list(generate_list_by_frequency(lst, ascending=ascending))


def as_list(obj_or_list, typing=List[Any]):
    # type: (Union[list, object], T_TYPING) -> List[Any]
    if not isinstance(obj_or_list, list):
        obj_or_list = [obj_or_list]
    isinstance_raise(obj_or_list, typing)
    return obj_or_list


def n_sized_chunks(lst, n):
    # type: (list, int) -> Generator[list, None, None]
    '''
    https://stackoverflow.com/a/312464
    '''
    if n < 1:
        raise ValueError('how can you divide a list into {} sized chunks... idiot'.format(n))
    for i in range(0, len(lst), n):
        yield lst[i:i + n]


def n_chunks(lst, n):
    # type: (list, int) -> Generator[list, None, None]
    '''
    if I want to divide 0, 1, 2, 3, 4 into 3 chunks, i'd expect 01, 23, 4 or 0, 12, 34
    '''
    if n < 1:
        raise ValueError('how can you divide a list into {} chunks... idiot'.format(n))
    i = 0
    even = len(lst) % n == 0
    size = len(lst) // n if even else len(lst) // n + 1
    while i < len(lst):
        yield lst[i:i + size]
        i += size
        if not even and size - 1 > 0 and (len(lst) - i) % (size - 1) == 0:  # if remaining list is divisible by dropping down chunk lenght, do it
            size -= 1
            even = True


def rows_to_str_rows(rows, on_list=None):
    # type: (List[dict], Optional[Callable[[list], str]]) -> Tuple[List[Dict[str, str]], List[str], int]
    '''
    Description:
        analyze/process a list of rows
            massage into strings
            AND get headers
            AND get max cell length
    Arguments:
        rows: List[dict]
        on_list: Optional[Callable[[list], str]]
            if a list is detected, THIS converts it to a string
    Returns:
        Tuple[List[Dict[str, str]], List[str], int]
            - rows of dicts of strings
            - headers
            - max string length of cells
    '''
    isinstance_raise(rows, List[dict])
    headers = []
    max_col_count = -1
    row_strs = []
    for r, row in enumerate(rows):
        row_str = {}
        for key, value in row.items():
            if key not in headers:
                headers.append(key)
            value_str = str(value) if value is not None else ''
            if isinstance(value, (set, list, dict)):
                if isinstance(value, list):
                    if not on_list:
                        raise NotImplementedError(f'row {r} has key w/ value type: {type(value)}, no handler passed!')
                    value_str = on_list(value)
                else:
                    raise NotImplementedError(f'row {r} has key {key!r} w/ value type: {type(value)}! Only primitives allowed!')
            row_str[key] = value_str
            max_col_count = max([max_col_count, len(value_str)])
        row_strs.append(row_str)
    max_col_count = max([max_col_count] + [len(header) for header in headers])

    return row_strs, headers, max_col_count


def matrix_to_str_rows(matrix, on_list=None):
    # type: (List[List[Any]], Optional[Callable[[list], str]]) -> Tuple[List[List[str]], List[str], int]
    isinstance_raise(matrix, List[List[Any]])
    rows = []
    for row in matrix:
        rows.append({str(idx): val for idx, val in enumerate(row)})
    row_strs, headers, max_col_count = rows_to_str_rows(rows, on_list=on_list)
    matrix_reloaded = [list(row_str.values()) for row_str in row_strs]
    return matrix_reloaded, headers, max_col_count


matrix_to_str_rows.__doc__ = (rows_to_str_rows.__doc__ or '').replace(rows_to_str_rows.__name__, matrix_to_str_rows.__name__)
