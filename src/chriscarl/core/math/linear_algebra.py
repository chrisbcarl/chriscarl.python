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

- https://www.ling.upenn.edu/courses/cogs501/LinearAlgebraReview.html

Updates:
    2026-02-27 - core.math.linear_algebra - added transpose, magnitude, vector_multiply, orthogonal, orthonormal, matrix_vector_multiply
    2026-02-22 - core.math.linear_algebra - added vectors_to_matrix, confirmed is_multipliable, added matrix_multiply
    2026-02-18 - core.math.linear_algebra - initial commit

TODO:
    - row echelon form:
        - https://www.emathhelp.net/calculators/linear-algebra/reduced-row-echelon-form-rref-calculator/?i=%5B%5B1%2C1%2C1%5D%2C%5B2%2C1%2C3%5D%2C%5B3%2C2%2C4%5D%5D
        - https://math.libretexts.org/Courses/Palo_Alto_College/College_Algebra/05%3A_Systems_of_Equations_and_Inequalities/5.04%3A_Solving_Systems_with_Gaussian_Elimination
    - matrix rank (col or row is same thanks to properties)
        - https://www.emathhelp.net/calculators/linear-algebra/rank-of-matrix-calculator/?i=%5B%5B1%2C1%2C1%5D%2C%5B2%2C1%2C3%5D%2C%5B3%2C2%2C4%5D%5D
    - Elementary operations are reversible transformations that preserve rank. They come in three types
        - Row/Column Swap (Ri ↔ Rj​)
        - Row/Column Scaling (Ri → kRi, k≠0)
        - Row/Column Replacement (Ri ​→ Ri ​+ kRj​)
        - We use these elementary row operations to convert the matrix into either:
        - Row/column Echelon Form or Reduced Row/column Echelon Form
        - Normal Form
'''

# stdlib imports
from __future__ import absolute_import, print_function, division, with_statement  # , unicode_literals
import os
import sys
import logging
from typing import List, Union, Generator, Any
import functools
import itertools
import math
import re

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
T_MATRIX = List[List[Union[int, float, Any]]]


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


def create(n, m, val=0):
    # type: (int, int, int|float) -> T_MATRIX
    A = [[val for _ in range(m)] for _ in range(n)]
    return A


def transpose(A):
    # type: (T_MATRIX) -> T_MATRIX
    if not is_matrix(A):
        raise TypeError('A is not a matrix!')

    n, m = len(A), len(A[0])
    T = create(m, n)
    for r in range(n):
        for c in range(m):
            # "swap rowas and collumns"
            T[c][r] = A[r][c]  # literally turn your brain off, that easy
    return T


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


def magnitude(V):
    # type: (T_MATRIX) -> float
    '''length in the sense of euclidean distance from the origin'''
    if not is_vector(V):
        raise TypeError('V is not a vector!')
    return math.sqrt(sum(row[0]**2 for row in V))


def vector_multiply(V, W):
    # type: (T_MATRIX, T_MATRIX) -> float
    if not is_vector(V):
        raise TypeError('V is not a vector!')
    if not is_vector(W):
        raise TypeError('W is not a vector!')
    n = len(V)
    if len(V) != len(W):
        raise ValueError('vector multiplication requires same dimensions!')
    return sum(V[r][0] * W[r][0] for r in range(n))


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
    if not is_matrix(A):
        raise TypeError('A is not a matrix!')
    if not inplace:
        A = [row[:] for row in A]
    for r, row in enumerate(A):
        for c, cell in enumerate(row):
            if isinstance(s, (int, float)):
                A[r][c] = s * cell
            else:
                A[r][c] = f'{s}*{cell}'
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
        raise TypeError('A is not a matrix!')
    cols = len(A[0])
    for c in range(cols):
        yield [[row[c]] for row in A]


def orthogonal(A):
    # type: (T_MATRIX) -> float
    '''
    - https://www.ling.upenn.edu/courses/cogs501/LinearAlgebraReview.html
        orthogonal if the inner product of every (non-identical) pair is 0.

    '''
    if not is_matrix(A):
        raise TypeError('A is not a matrix!')
    vectors = list(matrix_to_vectors(A))
    return all(vector_multiply(v0, v1) == 0 for v0, v1 in itertools.combinations(vectors, 2))


def orthonormal(VA):
    # type: (T_MATRIX) -> float
    '''
    - https://www.ling.upenn.edu/courses/cogs501/LinearAlgebraReview.html
        if the inner product of every non-identical pair is 0 (i.e. they are orthogonal), and
        the product of every vector with itself is 1 (i.e. the vectors all have geometric length 1).
    '''
    if is_vector(VA):
        return round(magnitude(VA), 9) == 1
    elif is_matrix(VA):
        gonal = orthogonal(VA)
        normal = all(orthonormal(vec) for vec in matrix_to_vectors(VA))
        return gonal and normal
    else:
        raise TypeError('VA is neither a vector nor a matrix!')


def vectors_to_matrix(vecs):
    # type: (List[T_MATRIX]) -> T_MATRIX
    '''
    Description:
        [[1] [2] [3]] + [[1] [2] [3]] = [
            [2],
            [4],
            [6],
        ]
    Arguments:
        A: List[T_MATRIX]
            the list of vectors to matricize
    Return:
        T_MATRIX
    '''
    isinstance_raise(vecs, List[T_MATRIX])
    A = [[row[0]] for row in vecs[0]]  # copy of 1st vector
    if len(vecs[0]) == 1:
        return A  # already done...
    if not is_matrix(A):
        raise TypeError('A is not a matrix!')
    for col in range(1, len(vecs)):
        vec = vecs[col]
        for r, row in enumerate(vec):
            A[r].append(row[0])
    return A


def is_multipliable(A, B, raise_on_error=False):
    # type: (T_MATRIX, T_MATRIX, bool) -> bool
    if not is_matrix(A):
        raise TypeError('A is not a matrix!')
    if not is_matrix(B):
        raise TypeError('B is not a matrix!')
    rows_A, cols_A = len(A), len(A[0])  # 2x3
    rows_B, cols_B = len(B), len(B[0])  # 3x1
    truth = cols_A == rows_B
    if raise_on_error and not truth:
        raise ValueError(f"{rows_A} x {cols_A} is not multipliable with {rows_B} x {cols_B}!")
    return truth


def matrix_vector_multiply(A, V):
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
        raise TypeError('A is not a matrix!')
    if not is_vector(V):
        raise TypeError("V is not a column-wise vector!")
    is_multipliable(A, V, raise_on_error=True)

    scaled_A_vectors = [scalar_multiply(V[col][0], A_vec) for col, A_vec in enumerate(matrix_to_vectors(A))]
    B = functools.reduce(
        lambda left, right: [[left[row][0] + right[row][0]] if isinstance(left[row][0], (int, float)) else [f'{left[row][0]} + {right[row][0]}'] for row in range(len(left))],
        scaled_A_vectors
    )
    return B


def matrix_multiply(A, B):
    # type: (T_MATRIX, T_MATRIX) -> T_MATRIX
    r'''
    Description:
        Expressed as:
            $A \times B$
        Evaluated as:
            B is the 1st transform, A is the 2nd transform, therefore:
            for b_column_vector in B
                new A_vec = A scaled by b_column_vector as new basis
            return accumulated new vectors
    '''
    is_multipliable(A, B, raise_on_error=True)
    C = []
    for col, b_vec in enumerate(matrix_to_vectors(B)):
        a_vec = matrix_vector_multiply(A, b_vec)
        C.append(a_vec)
    return vectors_to_matrix(C)
