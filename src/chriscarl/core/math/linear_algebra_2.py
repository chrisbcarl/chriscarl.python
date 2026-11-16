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
TODO:
    - to_str should justify all of the values... otherwise you get weird stuff with negatives, looks whack
    - add LaTeX traces for all operations
    - add `fractions` support instead of floats everywhere...
    - overload regular lists support [[1],[2],[3]] + [[1],[2],[3]]
        - basically "list" has to check if self is T_MATRIX and other is T_MATRIX THEN do the op.
        - optional return of a class which computes the LU decomp already

Matrices have properties / operations:
    - dimensions, addable, multipliable (DONE)
        - scale (DONE)
        - add
        - dot product, linear combination
    - gaussian eliminiation (DONE, INITIAL TESTED)
        - rank, free variables
        - ref, rref
        - invertability
    - elementary matrixes
        - LU decomp
    - Ax = b (solve for x)

Updates:
    2026-11-16 - core.math.linear_algebra_2 - added project, modified add to use a variadic list
    2026-11-08 - core.math.linear_algebra_2 - homework involved transposes, magnitudes, dot products, etc, so I got matrix multiply (row interpretation) for free, TODO: test cases
    2026-10-21 - core.math.linear_algebra_2 - not sure why int/float parsing wasn't happening correctly, weird oversight...
    2026-10-11 - core.math.linear_algebra_2 - 17:49 had a lot of fun, brute forced GE + LU + A^{-1}, not bad. Need to test edge cases for matrices, think non-square and non-invertible, etc.
    2026-10-11 - core.math.linear_algebra_2 - initial commit
'''

# stdlib imports
from __future__ import absolute_import, print_function, division, with_statement  # , unicode_literals
import os
import sys
import logging
from typing import List, Sequence, Union, Any, Tuple, Callable
import re
import math
from itertools import combinations

# third party imports

# project imports
from chriscarl.core.lib.stdlib.typing import isinstance_raise, raise_w_msg
from chriscarl.core.types.list import matrix_to_str_rows
from chriscarl.core.types.str import indent

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
T_MATRIX = Sequence[Sequence[Union[int, float]]]  # apparently list doesnt satisfy List anymore... i'm so cooked


def is_vector(*v):
    # type: (T_MATRIX) -> bool
    '''
    Description:
        Returns if something is a COLUMN vector
    Arguments:
        *v: T_MATRIX
            you can check multiple if you like
    Returns:
        bool
    '''
    for vector in v:
        try:
            isinstance_raise(vector, T_MATRIX)
        except TypeError:
            return False
        if len(vector) != 1:
            return False
    return True


def is_matrix(*A):
    # type: (T_MATRIX) -> bool
    '''
    Description:
        Returns if something is a matrix of same column count rows
    Arguments:
        *A: T_MATRIX
            you can check multiple if you like
    Returns:
        bool
    '''
    for matrix in A:
        try:
            isinstance_raise(matrix, T_MATRIX)
        except TypeError:
            return False
        length = len(matrix[0])
        for row in matrix:
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
            fraction = dick['fraction']
            if fraction:
                row.append(float(content))
            else:
                row.append(int(content, base=0))
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
    line_text = '\n'.join(f'{indent}{line} \\\\' for line in lines)
    return f'''\\begin{{{notation}}}
{line_text}
\\end{{{notation}}}'''


def to_str(A, padding=' '):
    # type: (T_MATRIX, str) -> str
    '''
    Description:
        what it says on the tin. just get a simple string output
    Arguments:
        A: T_MATRIX
        padding: str
            space between the nums
    '''
    if not is_matrix(A):
        raise_w_msg(A, T_MATRIX)
    row_strs, _, max_col_count = matrix_to_str_rows(A)
    fmt = f'{{:{max_col_count}s}}'
    text = '\n'.join(padding.join(fmt.format(ele) for ele in row) for row in row_strs)
    return text


def create(m, n, val=lambda i, j: 0):
    # type: (int, int, int|float|Callable[[int, int], int|float]) -> T_MATRIX
    r'''
    Description:
        Matrices are given in $m \times n$ format
    Arguments:
        m: int
            row count, indexed by i starting at 1
        n: int
            column count, indexed by j starting at 1
        val: int|float|Callable[[int, int], int|float]
            whatever you want to fill it with
                - a scalar
                - $f(m, n) \mapsto \mathbb{R}$, m and n are 1-indexed because this is MATH
            see identity(m, n) source as an example
    '''
    A = [[val(i + 1, j + 1) if callable(val) else val for j in range(n)] for i in range(m)]
    return A


def identity(m, n):
    # type: (int, int) -> T_MATRIX
    return create(m, n, val=lambda m, n: 1 if m == n else 0)


def dimensions(A):
    # type:(T_MATRIX) -> Tuple[int, int]
    r'''
    Description:
        Returns $m \times n$
        Also serves as the type checker in many instances
    Arguments:
        M: T_MATRIX
    Returns:
        Tuple[int, int] - $m \times n$
    '''
    if not is_matrix(A):
        raise_w_msg(A, T_MATRIX)
    return (len(A), len(A[0]))


def is_addable(A, B):
    r'''
    Description:
        Both A and B must be of same $m \times n$
    Arguments:
        A: T_MATRIX
        B: T_MATRIX
    Returns:
        bool
    '''
    dimsA, dimsB = dimensions(A), dimensions(B)
    return dimsA == dimsB


def is_multipliable(A, B):
    r'''
    Description:
        if $A \in \mathbb{R}^{m \times n}$ and $B \in \mathbb{R}^{n \times o}$,
            $A \times B \in \mathbb{R}^{m \times o}$
        The reason is because of linear combinations. Matrixes are a row vector of column vectors,
            so $A \times B = [A \times b_0 \quad A\timesb_1 \quad \cdots \ A\timesb_n]$
    Arguments:
        A: T_MATRIX
        B: T_MATRIX
    Returns:
        bool
    '''
    dimsA, dimsB = dimensions(A), dimensions(B)
    return dimsA[1] == dimsB[0]


def row_scale(row, scalar):
    # type: (Sequence[int|float], int|float) -> List[int|float]
    isinstance_raise(row, Sequence[int | float])
    isinstance_raise(scalar, int, float)
    return [ele * scalar for ele in row]


def is_row_addable(row_a, row_b):
    # type: (Sequence[int|float], Sequence[int|float]) -> bool
    isinstance_raise(row_a, Sequence[int | float])
    isinstance_raise(row_b, Sequence[int | float])
    if len(row_a) != len(row_b):
        return False
    return True


def row_add(row_a, row_b):
    # type: (Sequence[int|float], Sequence[int|float]) -> List[int|float]
    if not is_row_addable(row_a, row_b):
        raise ValueError(f'row_a and row_b must have same length! {len(row_a)}  != {len(row_b)}')
    return [a + b for a, b in zip(row_a, row_b)]


def row_sub(row_a, row_b):
    # type: (Sequence[int|float], Sequence[int|float]) -> List[int|float]
    if not is_row_addable(row_a, row_b):
        raise ValueError(f'row_a and row_b must have same length! {len(row_a)}  != {len(row_b)}')
    return [a - b for a, b in zip(row_a, row_b)]


def scale(A, scalar):
    # type: (T_MATRIX, int|float) -> T_MATRIX
    isinstance_raise(A, T_MATRIX)
    isinstance_raise(scalar, int, float)
    return [[ele * scalar for ele in row] for row in A]


def clean_negative_0(*A):
    # type: (T_MATRIX) -> T_MATRIX | Tuple[T_MATRIX, ...]
    r'''
    Description:
        IEEE 754 defines -0, but it doesnt look good, so clean that up
    Arguments:
        *A: T_MATRIX
    Returns:
        T_MATRIX
    '''
    for matrix in A:
        m, n = dimensions(matrix)
        for i in range(m):
            for j in range(n):
                if matrix[i][j] == 0:  # catches 0 and -0
                    matrix[i][j] = 0
    return A[0] if len(A) == 1 else tuple(A)


def copy(*A):
    # type: (T_MATRIX) -> T_MATRIX | Tuple[T_MATRIX, ...]
    r'''
    Description:
        Simple copy.
    Arguments:
        *A: T_MATRIX
    Returns:
        T_MATRIX
    '''
    lst = []
    for matrix in A:
        m, n = dimensions(matrix)
        A2 = create(m, n, val=0)
        for i in range(m):
            for j in range(n):
                if matrix[i][j] == 0:  # catches 0 and -0
                    A2[i][j] = 0
                else:
                    A2[i][j] = matrix[i][j]
        lst.append(A2)
    return lst[0] if len(lst) == 1 else tuple(lst)


def gaussian_elimination(A, floating=False, ops_as_latex=True):
    # type: (T_MATRIX, bool, bool) -> Tuple[T_MATRIX, T_MATRIX, T_MATRIX, T_MATRIX, T_MATRIX | None, str]
    r'''
    Description:
        Swap, scale, and row-reduce in order to get A into I (the identity matrix)
        algorithm:
            swap rows to make sure the leftmost is non zero
            from top to bottom, left to right
                each row = that row - some scalar * top row
                once each row has been dealt with, every row under the top should have a 0 in the element
        (bit tough to explain formally without doing it)
        example:
            # https://en.wikipedia.org/wiki/Gaussian_elimination
            A -> GE ->  P           U               L           rref(A)
            2  1  -1    1  0  0     2   1   -1      1   0   0
            -3 -1 2     0  1  0     0   1   1       3   2   0
            -2 1  2     0  0  1     0   0   -2      -10 -8  2

        >>> P, L, U, rref, A_inverse, ops_string = gaussian_elimination([[2, 1, -1], [-3, -1, 2], [-2, 1, 2]])
        ... print(to_string(P))

    Arguments:
        A: T_MATRIX
        floating: bool = False
            set floating if you want to subtract $\ell_{ij}$ of the other row from the current row
            by hand you'd typically multiply the current row and subtract a multiple of the other row (leads to nice numbers)
        ops_as_latex: bool = True
            in the operations report, output as latex or as simple string?
    Returns:
        T_MATRIX
            P, L, U, rref, A_inverse, ops_string
            Tuple[T_MATRIX, T_MATRIX, T_MATRIX, T_MATRIX, T_MATRIX, str]
                - $P$: permutation matrix
                - $L$: lower triangle
                - $U$: upper triangle, $\operatorname{ref}(A)$
                    - NOTE: U is generated first, L is second, but returned back as L, U
                - $\operatorname{rref}(A)$: reduced as much as possible, may be identity, may be not
                - $A^{-1}$: inverse of A if it exists, else None
                - ops_string: LaTeX operations enumerated out
    '''
    m, n = dimensions(A)  # also type check
    ops = ['Gaussian Elimination with LU Decomposition and Inverse', 'A', copy(A)]

    AUGMENTED = [row + [1 if j == i else 0 for j in range(n)] for i, row in enumerate(A)]
    ops += ['augmentation', copy(AUGMENTED)]  # print(to_str(AUGMENTED))

    start_col = 0  # usually you start at the 1st column, but if all leading is 0, have to move on
    P = identity(m, n)
    # swap rows to make sure the leftmost is non zero
    if AUGMENTED[0][0] != 0:
        ops += ['permutation', None]
    else:
        swap_idx = -1
        for col in range(n):
            for i, row in enumerate(AUGMENTED):
                if row[col] != 0:
                    swap_idx = i
                    break
            if swap_idx != -1:
                start_col = col
                break

        row = AUGMENTED[swap_idx]
        AUGMENTED[swap_idx] = AUGMENTED[0]
        AUGMENTED[0] = row

        row = P[swap_idx]
        P[swap_idx] = P[0]
        P[0] = row

        ops += ['permutation', (0 + 1, swap_idx + 1), copy(P)]  # print(f'R{0 + 1} <-> R{swap_idx + 1}')

    # top to bottom, left to right
    ops += ['permutation-post', copy(AUGMENTED)]  # print(to_str(AUGMENTED))
    above_idx = 0
    for j in range(start_col, n - 1):
        above_row = AUGMENTED[above_idx]
        above_row_leading = AUGMENTED[above_idx][j]
        for i in range(1, m):
            if i == j:
                continue
            below_row = AUGMENTED[i]
            below_row_leading = below_row[j]

            if floating:
                # # ell = leading of my row / leading of their row
                # # R2 <- R2 - ell R1
                # # R3 <- R3 - ell R1
                # # R3 <- R3 - ell R2
                ell = below_row_leading / above_row_leading  # is the actual coefficient to adjust this row by some other above_row row
                ops += [(i + 1, i + 1, ell, above_idx + 1)]  # print(f'R{i + 1} <- R{i + 1} - ({ell}) R{above_idx + 1}')
                AUGMENTED[i] = row_sub(below_row, row_scale(above_row, ell))  # leads to nastier floaty values
            else:
                # R2 <- a R2 - b R1 (a is leading of R1, b is leading of R2)
                # R3 <- a R3 - b R1 (a is leading of R1, b is leading of R3)
                # R3 <- a R3 - b R2 (a is leading of R2, b is leading of R3)
                ops += [
                    (i + 1, above_row_leading, i + 1, below_row_leading, above_idx + 1)
                ]  # print(f'R{i + 1} <- ({above_row_leading}) R{i + 1} - ({below_row_leading}) R{above_idx + 1}')
                AUGMENTED[i] = row_sub(row_scale(below_row, above_row_leading), row_scale(above_row, below_row_leading))
            ops += [copy(AUGMENTED)]  # print(to_str(AUGMENTED))

        above_idx += 1

    U = [[row[j] for j in range(0, n)] for row in AUGMENTED]  # type: T_MATRIX
    L = [[row[j + n] for j in range(0, n)] for row in AUGMENTED]  # type: T_MATRIX

    U, L = clean_negative_0(U, L)
    ops += ['U', copy(U), 'L', copy(L)]  # print('U | L'); print(to_str(AUGMENTED))

    # scale
    ops += ['scale']
    for i in range(m):
        row = AUGMENTED[i]
        leading = row[i]
        AUGMENTED[i] = row_scale(row, 1 / leading)
        ops += [(i + 1, leading, i + 1)]  # print(f'R{row + 1} <- 1/{leading} R{row + 1}')

    ops += ['scale-post', copy(AUGMENTED)]  # print('post-scale'); print(to_str(AUGMENTED))
    # from bottom to top, right to left, eliminate
    below_idx = m - 1  # the bottomost row
    for j in range(n - 1, 0, -1):  # j in 2, 1
        below_row = AUGMENTED[below_idx]
        below_row_trailing = below_row[j]
        for i in range(m - 2, -1, -1):  #  i in 1, 0
            if i == j:
                continue
            above_row = AUGMENTED[i]
            above_row_trailing = above_row[j]

            # R2 <- R2 - ell R3
            if floating:
                # # ell = leading of my row / leading of their row
                # # R2 <- R2 - ell R3
                # # R1 <- R1 - ell R3
                # # R1 <- R1 - ell R2
                ell = above_row_trailing / below_row_trailing  # is the actual coefficient to adjust this row by some other above_row row
                ops += [(i + 1, i + 1, ell, above_idx + 1)]  # print(f'R{i + 1} <- R{i + 1} - ({ell}) R{above_idx + 1}')
                AUGMENTED[i] = row_sub(above_row, row_scale(below_row, ell))  # leads to nastier floaty values
            else:
                # R2 <- a R2 - b R3 (a is trailing of R3, b is trailing of R2)
                # R1 <- a R1 - b R3 (a is trailing of R3, b is trailing of R1)
                # R1 <- a R1 - b R2 (a is trailing of R2, b is trailing of R1)
                ops += [
                    (i + 1, below_row_trailing, i + 1, above_row_trailing, above_idx + 1)
                ]  #print(f'R{i + 1} <- ({below_row_trailing}) R{i + 1} - ({above_row_trailing}) R{above_idx + 1}')
                AUGMENTED[i] = row_sub(row_scale(above_row, below_row_trailing), row_scale(below_row, above_row_trailing))
            ops += [copy(AUGMENTED)]  # print(to_str(AUGMENTED))
        below_idx -= 1

    rref = [[row[j] for j in range(0, n)] for row in AUGMENTED]  # type: T_MATRIX
    A_inverse = [[row[j + n] for j in range(0, n)] for row in AUGMENTED]  # type: T_MATRIX
    rref = clean_negative_0(rref)
    if A_inverse:
        A_inverse = clean_negative_0(A_inverse)
    ops += ['$\\operatorname{{rref}}(A)$', copy(rref), '$A^{-1}$', copy(A_inverse)]  # print('rref | A^{-1}'); print(to_str(rref)); print(to_str(A_inverse))

    ops_strings = []
    if not ops_as_latex:
        for op in ops:
            if isinstance(op, str):
                if op.startswith('$'):
                    ops_strings.append(op[1:-1])
                else:
                    ops_strings.append(op)
            elif op is None:
                ops_strings.append(indent('None'))
            elif isinstance(op, list):
                ops_strings.append(indent(to_str(op)))
            elif isinstance_raise(op, tuple):
                if len(op) == 2:  # permutation
                    ops_strings.append(f'R{op[0]} <-> R{op[1]}')
                elif len(op) == 3:  # scale
                    ops_strings.append(f'R{op[0]} <- 1/{op[1]} R{op[2]}')
                elif len(op) == 4:  # ref float
                    ops_strings.append(f'R{op[0]} <- R{op[1]} - ({op[2]}) R{op[3]}')
                elif len(op) == 5:  # ref non-float
                    ops_strings.append(f'R{op[0]} <- {op[1]} R{op[2]} - {op[3]} R{op[4]}')
        ops_string = print('\n'.join(ops_strings))
    else:
        for op in ops:
            if isinstance(op, str):
                if op.startswith('$'):
                    ops_strings.append(op[1:-1])
                else:
                    ops_strings.append(f'\\text{{{op}}}')
            elif op is None:
                ops_strings.append(indent(f'\\text{{None}}\\\\', indent='    \\quad '))
            elif isinstance(op, list):
                ops_strings.append(f'\\quad {to_latex(op)}')
            elif isinstance_raise(op, tuple):
                if len(op) == 2:  # permutation
                    ops_strings.append(f'R{op[0]} \\leftrightarrow R{op[1]}')
                elif len(op) == 3:  # scale
                    ops_strings.append(f'R{op[0]} \\leftarrow \\frac{{1}}{{{op[1]}}} R{op[2]}')
                elif len(op) == 4:  # ref float
                    ops_strings.append(f'R{op[0]} \\leftarrow R{op[1]} - ({op[2]}) R{op[3]}')
                elif len(op) == 5:  # ref non-float
                    ops_strings.append(f'R{op[0]} \\leftarrow {op[1]} R{op[2]} - ({op[3]}) R{op[4]}')
        ops_string = f'$$\n{"\n".join(f"{string} \\\\" for string in ops_strings)}\n$$'

    return P, L, U, rref, A_inverse, ops_string

    # - gaussian eliminiation
    #     - rank, free variables
    #     - invertability
    # - elementary matrixes
    #     - LU decomp
    # - Ax = b (solve for x)


def try_equal_dimmensions(*vec_or_Mat):
    # type: (T_MATRIX) -> Tuple[int, int]
    m0, n0 = dimensions(vec_or_Mat[0])
    for i in range(1, len(vec_or_Mat)):
        m1, n1 = dimensions(vec_or_Mat[i])
        if not (m0 == m1 and n0 == n1):
            raise ValueError(f'vectors or Matrices must be equal dimensions! the {i}-th object isnt! ${m0} \\times {n0} != {m1} \\times {n1}$')
    return m0, n0


def dot_product(u_A, w_B):
    # type: (T_MATRIX, T_MATRIX) -> float|int
    r'''
    For vectors: Dot Product
    $$
    u, v \in \mathbb{R}^{1 \times n} \\
    \mathbf{u} \cdot \mathbf{w} = \displaystyle\sum_{j=1}^{n} u_j \cdot w_j \in \mathbb{R}^{1 \times 1}
    $$

    For matrices: Frobenius Inner Product
    $$
    A, B \in \mathbb{R}^{m \times n} \\
    \langle A, B \rangle_{\text{F}} = \displaystyle\sum_{i=1}^{n} \displaystyle\sum_{j=1}^{n} u_j \cdot w_j \in \mathbb{R}^{1 \times 1}
    $$

    Geometric Meaning: product of a and b's magnitude with their angle cosine
    '''
    m0, n0 = try_equal_dimmensions(u_A, w_B)
    acc = sum(u_A[i][j] * w_B[i][j] for i in range(m0) for j in range(n0))
    return acc


frobenius_inner_product = dot_product


def l2_norm(s_v_A):
    # type: (float|int|T_MATRIX) -> float|int
    r'''
    L2 Norm or Magnitude (Scalar):
    $$
    s \in \mathbb{R}^{1 \times 1} \\
    \Vert s \Vert = \vert s \vert = \abs{s} \in \mathbb{R}^{1 \times 1} \\
    $$

    L2 Norm or Magnitude (Vector):
    $$
    \mathbf{v} \in \mathbb{R}^{1 \times d} \cup \mathbb{R}^{d\times 1} \\
    \Vert v \Vert_{2} = \sqrt{ \displaystyle\sum_{k=1}^{d} v_{k}^2 } \\
    \Vert v \Vert_{2} = \sqrt{ \mathbf{v} \cdot \mathbf{v} } \\
    $$

    Frobenius L2 Norm (Matrix):
    $$
    \mathbf{A} \in \mathbb{R}^{m \times n} \\
    \Vert A \Vert_{\text{F}} = \sqrt{ \displaystyle\sum_{i=1}^{m} \displaystyle\sum_{j=1}^{n} A_{ij}^2 } \\
    \Vert A \Vert_{\text{F}} = \sqrt{ \langle A, A \rangle_{\text{F}} } \\
    $$
    '''
    if isinstance(s_v_A, (int, float)):
        return abs(s_v_A)
    m, n = dimensions(s_v_A)
    acc = sum(s_v_A[i][j]**2 for i in range(m) for j in range(n))
    return math.sqrt(acc)


magnitude = l2_norm
frobenius_l2_norm = l2_norm


def normalize(v_A, apply=l2_norm):
    # type: (T_MATRIX, Callable[[float|int|T_MATRIX], float|int]) -> T_MATRIX
    r'''
    Normalization: apply a normative process on an object, scaling it
    $$
    v_{\text{L2 norm}} = \dfrac{1}{\Vert v \Vert_{2}} A, \Vert v_{\text{norm}} \Vert = 1 \\
    A_{\text{L2 norm}} = \dfrac{1}{\Vert A \Vert_{\text{F}}} A, \Vert A_{\text{norm}} \Vert = 1 \\
    $$
    '''
    norm = apply(v_A)
    return scale(v_A, 1 / norm)


def unit_vector(v):
    # type: (T_MATRIX) -> T_MATRIX
    r'''
    L2 Normalize a vector : make that normed vector's L2 norm == 1
    $$
    v \ne \vec{0}\\
    u = \dfrac{1}{\Vert v \Vert_{2}} v, \Vert u \Vert = 1 \\
    $$
    '''
    m, n = dimensions(v)
    if not is_vector(v) and not all(v[i][j] == 0 for i in range(m) for j in range(n)):
        raise_w_msg(v, T_MATRIX, msg='must be a non-zero vector')
    return normalize(v, apply=l2_norm)


def add(*vec_or_Mat):
    # type: (T_MATRIX) -> T_MATRIX
    r'''
    L2 Norm or Magnitude (explicit vector notation):
    $$
    \vec{v} \in \mathbb{R}^{1 \times d} \cup \mathbb{R}^{d\times 1} \\
    \vert \vec{v} \vert = \sqrt{\displaystyle\sum_{k=1}^{d} v_{k}} \\
    $$

    L2 Norm or Magnitude (implicit vector notation):
    $$
    v \in \mathbb{R}^{1 \times d} \cup \mathbb{R}^{d\times 1} \\
    \Vert v \Vert_{2} = \sqrt{\displaystyle\sum_{k=1}^{d} v_{k}} \\
    $$
    '''
    m0, n0 = try_equal_dimmensions(*vec_or_Mat)
    return create(m0, n0, val=lambda i, j: sum(vec_or_Mat[k][i - 1][j - 1] + vec_or_Mat[k][i - 1][j - 1] for k in range(len(vec_or_Mat))))


def angle(u_A, w_B, degrees=False):
    # type: (T_MATRIX, T_MATRIX, bool) -> float|int
    r'''
    Angles Between Vectors:
    $$
    \cos(\theta) = \dfrac{\mathbf{u} \cdot \mathbf{v}}{\Vert \mathbf{u} \Vert_{2} \Vert \mathbf{v} \Vert _2} \\
    \theta = \arccos( \dfrac{\mathbf{u} \cdot \mathbf{v}}{\Vert \mathbf{u} \Vert_{2} \Vert \mathbf{v} \Vert _2} ) \\
    $$

    Angles Between Matrices:
    $$
    \cos(\theta) = \dfrac{\langle A, B \rangle_{\text{F}}}{\Vert A\Vert_{\text{F}} \Vert B\Vert_{\text{F}}} = \dfrac{\operatorname{tr}(A^\top B)}{\sqrt{\operatorname{tr}(A^\top A)} \sqrt{\operatorname{tr}(B^\top B)}} \\
    \theta = \arccos( \dfrac{\langle A, B \rangle_{\text{F}}}{\Vert A\Vert_{\text{F}} \Vert B\Vert_{\text{F}}} ) \\
    $$
    '''
    try_equal_dimmensions(u_A, w_B)
    numerator = frobenius_inner_product(u_A, w_B)
    denomenator = frobenius_l2_norm(u_A) * frobenius_l2_norm(w_B)
    cos_theta = numerator / denomenator
    theta = math.acos(cos_theta)
    if degrees:
        return theta * 180 / math.pi
    return theta


def transpose(v_A):
    # type: (T_MATRIX) -> T_MATRIX
    r'''
    Transpose: "swap rows and columns"
    NOTE: In the definition, note the "for all i in n" (typically i in m)
    $$
    A \in \mathbb{m \times n}, A^\top \in \mathbb{n \times m} \\
    (A^\top)_{ij} = A_{ji} \forall i \in [n], j \in [m]
    $$
    '''
    m, n = dimensions(v_A)
    return create(n, m, val=lambda i, j: v_A[j - 1][i - 1])


def column_at(A, j):
    # type: (T_MATRIX, int) -> T_MATRIX
    r'''
    1-indexed, column of a matrix at col j
    '''
    m, n = dimensions(A)
    return create(m, 1, val=lambda i, _: A[i - 1][j - 1])


def columns(A):
    # type: (T_MATRIX) -> Sequence[T_MATRIX]
    r'''
    Return the columns of a matrix, useful for linear combinations.
    '''
    cols = []
    m, n = dimensions(A)
    for j in range(n):
        col = create(m, 1, val=lambda i, _: A[i - 1][j])
        cols.append(col)
    return cols


def row_at(A, i):
    # type: (T_MATRIX, int) -> T_MATRIX
    r'''
    1-indexed, row of a matrix at col i
    '''
    m, n = dimensions(A)
    return create(1, n, val=lambda _, j: A[i - 1][j - 1])


def rows(A):
    # type: (T_MATRIX) -> Sequence[T_MATRIX]
    r'''
    Return the columns of a matrix, useful for ???.
    '''
    rows = []
    m, n = dimensions(A)
    for i in range(m):
        row = create(1, n, val=lambda _, j: A[i][j - 1])
        rows.append(row)
    return rows


def matrix_multiply(A, B, interpretation='row'):
    # type: (T_MATRIX, T_MATRIX, str) -> T_MATRIX
    r'''
    Row interpretation, dot products: each element is the dot product of that ith row and jth column
    $$
    A \in \mathbb{R}^{m \times n}, B \in \mathbb{R}^{n \times d}, C = AB \in \mathbb{R}^{m \times d} \\
    C_{ij} = (A_{ik} \forall k \in [n]) \cdot (B_{kj} \forall k \in [m]) \\
    C_{ij} = A_{i,:} \cdot B_{:,j} = \displaystyle\sum_{k=1}^{n} A_{ik} \times B_{kj} \\
    $$
    '''
    (m0, n0), (m1, n1) = dimensions(A), dimensions(B)
    if not is_multipliable(A, B):
        raise ValueError(f'A is not multipliable with B! ${m0} \\times {n0} \ne {m1} \\times {n1}$')
    if interpretation == 'row':
        C = create(m0, n1, lambda i, j: dot_product(transpose(row_at(A, i)), column_at(B, j)))
        return C
    # TODO: linear combinations for column interpretation
    raise NotImplementedError()


def project(b, V):
    # type: (T_MATRIX, T_MATRIX) -> T_MATRIX
    r'''
    Projection of vector b onto some orthonormal subspace V is very straightforward.
        Abuse the properties of orthogonality and add the components up via
        a linear combination.

    $$
    \begin{aligned}
    \underset{m \times 1}{\vec{b}} &, \underset{m \times n}{\mathcal{V}} = \operatorname{span} \{ v_1, v_2, \cdots, v_n \} \\
    \forall_{k, l \in [m], k \ne l} & V_{k} \perp V_{l} : V_{k} \cdot V_{l} = 0  \\
    C_{j} &= \dfrac{b \cdot v_{j}}{\Vert v_{j} \Vert_{2}^{2}} = \dfrac{b \cdot v_{j}}{v_{j} \cdot v_{j}} v_{j} \\
    \hat{b} &= \displaystyle\sum_{j=1}^{n} C_{j} v_{j} = \displaystyle\sum_{j=1}^{n}\dfrac{b \cdot v_{j}}{\Vert v_{j} \Vert_{2}^{2}} v_{j} = \displaystyle\sum_{j=1}^{n} \dfrac{b \cdot v_{j}}{v_{j} \cdot v_{j}} v_{j} \\
    &= C_1 v_1 + C_2 v_2 + \cdots C_n v_n \\
    \hat{b} &= \operatorname{\text{Proj}}_{\mathcal{V}} \vec{b} \\
    \end{aligned}
    $$
    '''
    m0, n0 = dimensions(V)
    m1, _ = dimensions(b)
    if m0 != m1:
        raise ValueError(f'row count has to match to project b onto V, ${m0} \\ne {m1}$!')

    # check orthonormality of subspace
    for k, l in combinations(range(n0), 2):  # [(0,1), (0,2), (1,2)]
        dp = dot_product(column_at(V, k), column_at(V, l))
        if dp != 0:
            raise ValueError(f'V is not an orthonormal subspace! $v_{k} \\cdot v_{l} \\ne 0$!')

    if n0 == 1:
        # vector b onto subspace 1D V projection
        P = scale(matrix_multiply(V, transpose(V)), 1 / dot_product(V, V))
        return matrix_multiply(P, b)
    else:
        # vector b onto subspace 2D+ V projection (assuming V is an orthonormal basis)
        components = []
        for j in range(n0):
            v_j = column_at(V, j)
            C_i = dot_product(v_j, b) / l2_norm(v_j)**2
            C_i_v_j = scale(v_j, C_i)
            components.append(C_i_v_j)
        return add(*components)  # linear combination of the components
