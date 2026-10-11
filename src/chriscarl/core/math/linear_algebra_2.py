#!/usr/bin/env python
# -*- coding: utf-8 -*-
r'''
Author:         Chris Carl
Email:          chrisbcarl@outlook.com
Date:           2026-10-11
Description:

core.math.linear_algebra_2 is a re-do of my original linear algebra library with a few improvements
goals:
    - markdown first documentation
    - computed from first principles, not hacky web crap
    - everything is column vectors
TODO: stretch:
    - overload regular lists support [[1],[2],[3]] + [[1],[2],[3]]
        - basically "list" has to check if self is T_MATRIX and other is T_MATRIX THEN do the op.
        - optional return of a class which computes the LU decomp already

Matrices have properties:
    - dimensions, rank, free variables
    - addable, multipliable
    - solve systems of equations as Ax = b through Gaussian Elimination
        - elementary matrixes
            - LU decomp
    - Ax = b (solve for x)
    - invertible

Updates:
    2026-10-11 - core.math.linear_algebra_2 - initial commit
'''

# stdlib imports
from __future__ import absolute_import, print_function, division, with_statement  # , unicode_literals
import os
import sys
import logging
from typing import List, Union, Any, Tuple
import re

# third party imports

# project imports
from chriscarl.core.lib.stdlib.typing import isinstance_raise, raise_w_msg

SCRIPT_RELPATH = 'chriscarl/core/math/linear_algebra_2.py'
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


def is_vector(v):
    # type: (T_MATRIX) -> bool
    try:
        isinstance_raise(v, T_MATRIX)
    except TypeError:
        return False
    for row in v:
        if len(row) != 1:
            return False
    return True


def is_matrix(A):
    # type: (T_MATRIX) -> bool
    try:
        isinstance_raise(A, T_MATRIX)
    except TypeError:
        return False
    length = len(A[0])
    for row in A:
        if len(row) != length:
            return False
    return True


def to_matrix(text):
    # type: (str) -> T_MATRIX
    '''
    Description:
        Given something that looks like a matrix, make it so.

    Arguments:
        1 2 3
        4, 5, 6
        7|8|9

    Returns:
        T_MATRIX
    '''
    A = []
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
        if row:  # could have empty lines in between or latex code or whatever
            A.append(row)
    if not is_matrix(A):
        raise_w_msg(text, T_MATRIX, msg=f'provided text is not of regular matrix form. double check? text was converted to {A}')
    return A


def to_latex(A, notation='bmatrix', indent='    '):
    # type: (T_MATRIX, str, str) -> str
    '''
    Description:
        what it says on the tin. other options include pmatrix, just matrix, array, etc.
    Arguments:
        A: T_MATRIX
        notation: str
            bmatrix, pmatrix, TODO: array, etc.
        indent: str
            if you want different padding for some weird reason
    '''
    lines = [' & '.join([str(ele) for ele in row]) for row in A]
    line_text = '\n'.join(f'    {line} \\\\' for line in lines)
    return f'''\\begin{{{notation}}}
{line_text}
\\end{{{notation}}}'''


def create(m, n, val=0):
    # type: (int, int, int|float) -> T_MATRIX
    r'''
    Description:
        Matrices are given in $m \times n$ format
    '''
    A = [[val for _ in range(m)] for _ in range(n)]
    return A


def get_dimensions(A):
    # type:(T_MATRIX) -> Tuple[int, int]
    r'''
    Returns $m \times n$

    Arguments:
        M: T_MATRIX

    Returns:
        Tuple[int, int] - $m \times n$
    '''
    if not is_matrix(A):
        raise_w_msg(A, T_MATRIX)
    return (len(A), len(A[0]))


# def is_addable(A, B)

#     - dimensions, rank, free variables
#     - addable, multipliable
#     - solve systems of equations as Ax = b through Gaussian Elimination
#         - elementary matrixes
#             - LU decomp
#     - Ax = b (solve for x)
#     - invertible
