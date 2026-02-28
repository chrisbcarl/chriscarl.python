#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
Author:         Chris Carl
Email:          chrisbcarl@outlook.com
Date:           2026-02-15
Description:

core.data_structures.heap is an implementation of heaps that uses an array as a backing store
core are modules that define the bedrock from which other things do import. non-self-referential, low-import, etc.

pytest --cov=chriscarl.core.data_structures.heap tests/core/data_structures/test_heap.py --cov-report term-missing

Updates:
    2026-02-27 - core.data_structures.heap - figured out what was wrong, it was the in-placeness that wasnt true.
    2026-02-15 - core.data_structures.heap - initial commit
'''

# stdlib imports
from __future__ import absolute_import, print_function, division, with_statement  # , unicode_literals
import os
import sys
import logging
from typing import Any, List

# third party imports

# project imports
from chriscarl.core.algorithms.basic import swap
from chriscarl.core.data_structures.tree import TreeNode, to_str

SCRIPT_RELPATH = 'chriscarl/core/data_structures/heap.py'
if not hasattr(sys, '_MEIPASS'):
    SCRIPT_FILEPATH = os.path.abspath(__file__)
else:
    SCRIPT_FILEPATH = os.path.abspath(os.path.join(sys._MEIPASS, SCRIPT_RELPATH))  # pylint: disable=no-member
SCRIPT_DIRPATH = os.path.dirname(SCRIPT_FILEPATH)
SCRIPT_NAME = os.path.splitext(os.path.basename(__file__))[0]
THIS_MODULE = sys.modules[__name__]
LOGGER = logging.getLogger(__name__)
LOGGER.addHandler(logging.NullHandler())


def is_heap(lst, i=0, max_heap=True):
    # type: (List[Any], int, bool) -> bool
    '''
    Description:
        a (max) heap is:
            structural property: an element's children is 0-index * 2 + (1 for left or 2 for right)
            order property: each element is greater than its children
    '''
    truth = True
    if i >= len(lst):
        return truth
    root = lst[i]

    l = i * 2 + 1
    if l < len(lst):
        left = lst[l]
        truth = truth and root > left if max_heap else root < left
        if not truth:
            return False  # short circuit
        truth = truth and is_heap(lst, i=l, max_heap=max_heap)
        if not truth:
            return False

    r = i * 2 + 2
    if r < len(lst):
        right = lst[r]
        truth = truth and root > right if max_heap else root < right
        if not truth:
            return False
        truth = truth and is_heap(lst, i=r, max_heap=max_heap)
        if not truth:
            return False
    return truth


def heapify_up(lst, i, max_heap=True):
    # type: (List[Any], int, bool) -> None
    if i <= 0:
        return
    r = (i - 1) // 2  # to compensate for the 0-indexing
    root = lst[r]
    value = lst[i]
    if max_heap and root < value:
        swap(lst, r, i)
    if not max_heap and root > value:
        swap(lst, r, i)

    heapify_up(lst, r, max_heap=max_heap)


def heapify(lst, max_heap=True):
    # type: (List[Any], bool) -> None
    for idx in range(1, len(lst)):
        heapify_up(lst, idx, max_heap=max_heap)


def insert(value, lst, max_heap=True):
    # type: (Any, List[Any], bool) -> None
    lst.append(value)
    heapify_up(lst, len(lst), max_heap=max_heap)


def heapify_down(lst, i, max_heap=True):
    # type: (List[Any], int, bool) -> None
    if i >= len(lst) - 1:
        return
    # root = lst[i]  # NOTE: BUG: caching the value causes problems...

    l = i * 2 + 1  # to compensate for the 0-indexing
    if l < len(lst):
        if max_heap and lst[l] > lst[i]:
            swap(lst, i, l)
        elif not max_heap and lst[l] < lst[i]:
            swap(lst, i, l)
        heapify_down(lst, l, max_heap=max_heap)

    r = i * 2 + 2  # to compensate for the 0-indexing
    if r < len(lst):
        if max_heap and lst[r] > lst[i]:
            swap(lst, i, r)
        elif not max_heap and lst[r] < lst[i]:
            swap(lst, i, r)
        heapify_down(lst, r, max_heap=max_heap)


# def heapify_down_better(lst, i, max_heap=True):
#     # type: (List[Any], int, bool) -> None
#     # BUG: this is actually wrong and doesnt produce consistently heaped...
#     l, r = i**2 + 1, i**2 + 2
#     worst = i
#     if l < len(lst):
#         if max_heap and lst[l] > lst[worst]:
#             worst = l
#         elif not max_heap and lst[l] < lst[worst]:
#             worst = l
#     if r < len(lst):
#         if max_heap and lst[r] > lst[worst]:
#             worst = r
#         elif not max_heap and lst[r] < lst[worst]:
#             worst = r
#     if worst != i:
#         swap(lst, i, worst)  # could be either left or right
#         heapify_down_better(lst, worst, max_heap=max_heap)


def pop(lst, max_heap=True):
    # type: (List[Any], bool) -> None
    l_idx = len(lst) - 1
    swap(lst, 0, l_idx)
    root = lst.pop(l_idx)
    heapify_down(lst, 0, max_heap=max_heap)
    # BUG: doesnt actually heapify sometimes, use above.
    # heapify_down_better(lst, 0, max_heap=max_heap)

    return root


def heapsort(lst, ascending=True):
    # type: (List[Any], bool) -> None
    new = []
    heapify(lst, max_heap=not ascending)
    while lst:  # O(n)
        ele = pop(lst, max_heap=not ascending)  # O(log_2(n))
        new.append(ele)
    # lst is now empty thanks to all the poping
    lst.extend(new)
