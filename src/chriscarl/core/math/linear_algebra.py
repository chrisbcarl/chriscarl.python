#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
Author:         Chris Carl
Email:          chrisbcarl@outlook.com
Date:           2026-02-18
Description:

core.math.linear_algebra is codified stuff from learning linear algebra in the way that it stuck with me
core are modules that define the bedrock from which other things do import. non-self-referential, low-import, etc.
lots of credit goes to 3Blue1Brown for the "Essence of linear algebra" series
    https://www.youtube.com/watch?v=fNk_zzaMoSs&list=PLZHQObOWTQDPD3MizzM2xVFitgF8hE_ab

Updates:
    2026-02-18 - core.math.linear_algebra - initial commit
'''

# stdlib imports
from __future__ import absolute_import, print_function, division, with_statement  # , unicode_literals
import os
import sys
import logging
import functools
import re
from typing import List, Union, Generator

# third party imports

# project imports
from chriscarl.core.lib.stdlib.typing import isinstance_raise

SCRIPT_RELPATH = 'chriscarl/core/math/linear_algebra.py'
if not hasattr(sys, '_MEIPASS'):
    SCRIPT_FILEPATH = os.path.abspath(__file__)
else:
    SCRIPT_FILEPATH = os.path.abspath(os.path.join(sys._MEIPASS, SCRIPT_RELPATH))  # pylint: disable=no-member
SCRIPT_DIRPATH = os.path.dirname(SCRIPT_FILEPATH)
SCRIPT_NAME = os.path.splitext(os.path.basename(__file__))[0]
THIS_MODULE = sys.modules[__name__]
LOGGER = logging.getLogger(__name__)
LOGGER.addHandler(logging.NullHandler())

NUMBER_REGEX = re.compile(r'(?P<sign>-)?(?P<whole>\d+)\.?(?P<fraction>\d+)?')
T_MATRIX = List[List[Union[int, float]]]


def to_matrix(text):
    # type: (str) -> T_MATRIX
    matrix = []
    for line in text.splitlines():
        if not line.strip():
            continue
        row = []
        for mo in NUMBER_REGEX.finditer(line):
            start, end = mo.span()
            content = line[start:end]
            dick = mo.groupdict()
            fraction = dick['whole']
            if fraction:
                row.append(float(content))
            else:
                row.append(int(content))
        matrix.append(row)
    return matrix


def is_vector(V):
    # type: (T_MATRIX) -> bool
    try:
        isinstance_raise(V, T_MATRIX)
    except TypeError:
        return False
    for row in V:
        if len(row) != 1:
            return False
    return True


def is_matrix(V):
    # type: (T_MATRIX) -> bool
    try:
        isinstance_raise(V, T_MATRIX)
    except TypeError:
        return False
    length = len(V[0])
    for row in V:
        if len(row) != length:
            return False
    return True


def is_addable(A, B, raise_on_error=False):
    # type: (T_MATRIX, T_MATRIX, bool) -> bool
    rows_A, cols_A = len(A), len(A[0])  # 2x3
    rows_B, cols_B = len(B), len(B[0])  # 3x1
    truth = rows_A == rows_B and cols_A == cols_B
    if raise_on_error and not truth:
        raise ValueError(f"{rows_A} x {cols_A} is not addable with {rows_B} x {cols_B}!")
    return truth


def add(A, B, inplace=False):
    # type: (T_MATRIX, T_MATRIX, bool) -> T_MATRIX
    '''
    Description:
        add is pretty obvious
    Arguments:
        A: T_MATRIX
            the list of rows to add
        B: T_MATRIX
            the list of rows to add
    Return:
        T_MATRIX
    '''
    is_addable(A, B, raise_on_error=True)
    if not inplace:
        A = [row[:] for row in A]
    for r, row in enumerate(A):
        for c, cell in enumerate(row):
            A[r][c] = B[r][c] + cell
    return A


def scalar_multiply(s, A, inplace=False):
    # type: (int|float, T_MATRIX, bool) -> T_MATRIX
    '''
    Description:
        scalar multiply is pretty obvious
    Arguments:
        s: int|float
            the singular value to multiply the matrix by
        A: T_MATRIX
            the list of rows to multiply
    Return:
        T_MATRIX
    '''
    isinstance_raise(s, (int, float))
    if not is_matrix(A):
        raise ValueError('A is not a matrix!')
    if not inplace:
        A = [row[:] for row in A]
    for r, row in enumerate(A):
        for c, cell in enumerate(row):
            A[r][c] = s * cell
    return A


def matrix_to_vectors(A):
    # type: (T_MATRIX) -> Generator[T_MATRIX, None, None]
    '''
    Description:
        0 1 2 is just 0  1  2
        3 4 5         3, 4, 5, right?
    Arguments:
        A: T_MATRIX
            the list of rows to vectorize
    Return:
        T_MATRIX
    '''
    if not is_matrix(A):
        raise ValueError('A is not a matrix!')
    cols = len(A[0])
    for c in range(cols):
        yield [[row[c]] for row in A]


def is_multipliable(A, B, raise_on_error=False):
    # type: (T_MATRIX, T_MATRIX, bool) -> bool
    rows_A, cols_A = len(A), len(A[0])  # 2x3
    rows_B, cols_B = len(B), len(B[0])  # 3x1
    truth = cols_A == rows_B
    if raise_on_error and not truth:
        raise ValueError(f"{rows_A} x {cols_A} is not multipliable with {rows_B} x {cols_B}!")
    return truth


def vector_multiply(A, V):
    # type: (T_MATRIX, T_MATRIX) -> T_MATRIX
    '''
    Description:
        A       x   V   =                   =
        0 1 2       6   6*0 + 7*1 + 8*2     23
        3 4 5   x   7   6*3 + 7*4 + 8*5     86
                    8

        The geometric intuition:
            each element in the vector is SCALING each vector in the matrix... then accumulate
        The programatic intuition:
            resultant is a 2x1, for row in matrix, accumulate by scalled
        result of a 2x3 x 3x1 is a 2x1 and this must be so
    Arguments:
        s: int|float
            the singular value to multiply the matrix by
        A: T_MATRIX
            the list of rows to multiply
    Return:
        T_MATRIX
    '''
    if not is_matrix(A):
        raise ValueError('A is not a matrix!')
    if not is_vector(V):
        raise TypeError("V is not a column-wise vector!")
    is_multipliable(A, V, raise_on_error=True)

    scaled_A_vectors = [scalar_multiply(V[col][0], A_vec) for col, A_vec in enumerate(matrix_to_vectors(A))]
    B = functools.reduce(lambda left, right: [[left[row][0] + right[row][0]] for row in range(len(left))], scaled_A_vectors)
    # TODO: RESUME, so far vector multiply works in a 2x3 x 3x1, but it should apparently also work in a 3x4 x 3x1 according to numpy...
    return B


def matrix_multiply(A, B):
    # type: (T_MATRIX, T_MATRIX) -> T_MATRIX
    '''
    '''
    isinstance_raise(A, T_MATRIX)
    isinstance_raise(B, T_MATRIX)
    C = []
    return C
