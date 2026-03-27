#!/usr/bin/env python
# -*- coding: utf-8 -*-
r'''
Author:         Chris Carl
Email:          chrisbcarl@outlook.com
Date:           2026-03-26
Description:

core.math.counting is all of the counting learnings I have had over time.
core are modules that define the bedrock from which other things do import. non-self-referential, low-import, etc.

Updates:
    2026-03-26 - core.math.counting - initial commit

TODO: int_guard, make sure all inputs are ints...
'''

# stdlib imports
from __future__ import absolute_import, print_function, division, with_statement  # , unicode_literals
import os
import sys
import logging

# third party imports

# project imports

SCRIPT_RELPATH = 'chriscarl/core/math/counting.py'
if not hasattr(sys, '_MEIPASS'):
    SCRIPT_FILEPATH = os.path.abspath(__file__)
else:
    SCRIPT_FILEPATH = os.path.abspath(os.path.join(sys._MEIPASS, SCRIPT_RELPATH))  # pylint: disable=no-member
SCRIPT_DIRPATH = os.path.dirname(SCRIPT_FILEPATH)
SCRIPT_NAME = os.path.splitext(os.path.basename(__file__))[0]
THIS_MODULE = sys.modules[__name__]
LOGGER = logging.getLogger(__name__)
LOGGER.addHandler(logging.NullHandler())


def factorial(n):
    # type: (int) -> int
    r'''
    Description:
        Read as "n-bang"
        only positive
    Examples:
        $0! = 1, 1! = 1$
    Arguments:
        $n$: int
    Returns:
        $n!$
    '''
    if not (n >= 0):
        raise ValueError(rf'required: $n \ge 0$, provided n={n}')
    acc = 1
    for i in range(1, n + 1):
        acc *= i
    return acc


def permutation(n, k):
    # type: (int, int) -> int
    r'''
    Description:
        Read as "n Permute k"
    Examples:
        - How many ways can I order 10 objects in 3 slots?  $10 * 9 * 8$, each filled slot reduces what can be picked next
    Arguments:
        $n$: int
        $k$: int
            permute
    Returns:
        (without repetition)
        ${}_{n}{P}_{k} = P(n, k) = \frac{n!}{(n-k)!}$
    '''
    if not (n >= 0):
        raise ValueError(rf'required: $n \ge 0$, provided n={n}')
    if not (k >= 0):
        raise ValueError(rf'required: $k \ge 0$, provided k={k}')
    if (n < k):
        return 0
    return factorial(n) // factorial(n - k)


def combination(n, k):
    # type: (int, int) -> int
    r'''
    Description:
        Read as "n Choose k"
    Examples:
        - How many ways can I combine 5 objects in 10 slots? $0$, not possible
        - How many ways can I combine 10 objects in 5 slots? ${}_{10}{C}_{5}$, permute but remove the duplicates
    Arguments:
        $n$: int
        $k$: int
            chose
    Returns:
        ${}_{n}{C}_{k} = C(n, k) = \binom{n}{k} = \frac{n!}{k!(n-k)!}$
    '''
    if not (n >= 0):
        raise ValueError(rf'required: $n \ge 0$, provided n={n}')
    if not (k >= 0):
        raise ValueError(rf'required: $k \ge 0$, provided k={k}')
    if (n < k):
        return 0
    return factorial(n) // (factorial(k) * factorial(n - k))
