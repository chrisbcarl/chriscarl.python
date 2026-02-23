#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
Author:         Chris Carl
Email:          chrisbcarl@outlook.com
Date:           2026-02-18
Description:

chriscarl.core.math.linear_algebra unit test.

Updates:
    2026-02-18 - tests.chriscarl.core.math.linear_algebra - initial commit
'''

# stdlib imports (expected to work)
from __future__ import absolute_import, print_function, division, with_statement  # , unicode_literals
import os
import sys
import logging
import unittest

# third party imports

# project imports (expected to work)
from chriscarl.core import constants
from chriscarl.core.lib.stdlib.os import abspath
from chriscarl.core.lib.stdlib.unittest import UnitTest

# test imports
import chriscarl.core.math.linear_algebra as lib

SCRIPT_RELPATH = 'tests/chriscarl/core/math/test_linear_algebra.py'
if not hasattr(sys, '_MEIPASS'):
    SCRIPT_FILEPATH = os.path.abspath(__file__)
else:
    SCRIPT_FILEPATH = os.path.abspath(os.path.join(sys._MEIPASS, SCRIPT_RELPATH))  # pylint: disable=no-member
SCRIPT_DIRPATH = os.path.dirname(SCRIPT_FILEPATH)
SCRIPT_NAME = os.path.splitext(os.path.basename(__file__))[0]
THIS_MODULE = sys.modules[__name__]
LOGGER = logging.getLogger(__name__)
LOGGER.addHandler(logging.NullHandler())

constants.fix_constants(lib)  # deal with namespace sharding the files across directories


class TestCase(UnitTest):

    def setUp(self):
        self.A = '''0 1 2
3 4 5'''
        self.A_mat = [
            [0, 1, 2],
            [3, 4, 5],
        ]
        self.B = '''6,7,8,9
10,11,12,13
14,15,16,17'''
        self.B_mat = [
            [6, 7, 8, 9],
            [10, 11, 12, 13],
            [14, 15, 16, 17],
        ]
        self.C = '''1.0
-2.0
3.0'''
        self.C_vec = [
            [1.0],
            [-2.0],
            [3.0],
        ]
        self.str_mat_a = [
            ['a11', 'a12'],
            ['a21', 'a22'],
            ['a31', 'a32'],
        ]
        self.str_mat_b = [
            ['b11', 'b12', 'b13', 'b14'],
            ['b21', 'b22', 'b23', 'b24'],
        ]
        return super().setUp()

    def tearDown(self):
        return super().tearDown()

    # @unittest.skip('lorem ipsum')
    def test_case_0(self):
        variables = [
            (lib.to_matrix, self.A),
            (lib.to_matrix, self.B),
            (lib.to_matrix, self.C),
        ]
        controls = [
            self.A_mat,
            self.B_mat,
            self.C_vec,
        ]
        self.assert_null_hypothesis(variables, controls)

    def test_case_1(self):
        # easy stuff like addition/ scalar multiplication, matrix_to_vectors
        pos2 = [
            [2 * 0, 2 * 1, 2 * 2],
            [2 * 3, 2 * 4, 2 * 5],
        ]
        neg2 = [
            [-2 * 0, -2 * 1, -2 * 2],
            [-2 * 3, -2 * 4, -2 * 5],
        ]
        vec0 = [
            [0],
            [3],
        ]
        vec1 = [
            [1],
            [4],
        ]
        vec2 = [
            [2],
            [5],
        ]
        A_vecs = [
            vec0,
            vec1,
            vec2,
        ]
        vec_mat = [
            [0, 1, 2],
            [3, 4, 5],
        ]
        variables = [
            (lib.is_addable, (self.A_mat, self.A_mat)),
            (lib.is_addable, (self.A_mat, self.B_mat)),
            (lib.is_addable, (self.A_mat, self.B_mat), dict(raise_on_error=True)),
            (lib.add, (self.A_mat, self.A_mat)),
            (lib.scalar_multiply, (1, self.A_mat)),
            (lib.scalar_multiply, (-2, self.A_mat)),
            (lib.matrix_to_vectors, self.C_vec),  # generator
            (lib.matrix_to_vectors, self.A_mat),
            (lib.matrix_to_vectors, [1, 2, 3]),
            (lib.vectors_to_matrix, A_vecs),
            (lib.vectors_to_matrix, vec0),
        ]
        controls = [
            True,
            False,
            ValueError,
            pos2,
            self.A_mat,
            neg2,
            [self.C_vec],
            A_vecs,
            TypeError,
            vec_mat,
            TypeError,
        ]
        self.assert_null_hypothesis(variables, controls)

    def test_case_2(self):
        # is_vector
        not_vec = list(range(10))
        variables = [
            (lib.is_vector, self.C_vec),
            (lib.is_vector, not_vec),
            (lib.is_matrix, self.A_mat),
            (lib.is_matrix, not_vec),
            (lib.is_multipliable, (self.A_mat, self.C_vec)),
            (lib.is_multipliable, (self.A_mat, self.A_mat)),
            (lib.is_multipliable, (self.A_mat, self.A_mat), dict(raise_on_error=True)),
        ]
        controls = [
            True,
            False,
            True,
            False,
            True,
            False,
            ValueError,
        ]
        self.assert_null_hypothesis(variables, controls)

    def test_case_3(self):
        # is_vector
        AxC = [
            [4],
            [10],
        ]
        BxC = [  # np.arary() @ np.array()
            [6., 7., 8., 9.],
            [-20., -22., -24., -26.],
            [42., 45., 48., 51.],
        ]
        mat_a = [
            ['a11', 'a12'],
            ['a21', 'a22'],
            ['a31', 'a32'],
        ]
        vec_b = [
            ['b11'],
            ['b21'],
        ]
        variables = [
            (lib.vector_multiply, (mat_a, vec_b)),
            (lib.vector_multiply, (self.A_mat, self.C_vec)),
            (lib.vector_multiply, (self.B_mat, self.C_vec)),
        ]
        controls = [
            [
                ['b11*a11 + b21*a12'],
                ['b11*a21 + b21*a22'],
                ['b11*a31 + b21*a32'],
            ],
            AxC,
            ValueError,
        ]
        self.assert_null_hypothesis(variables, controls)

    def test_case_4(self):
        A_xform_2 = [
            [0, 1],
            [2, 3],
        ]
        B_xform_1 = [
            [4, 5],
            [6, 7],
        ]
        C_xform = [
            [4 * 0 + 6 * 1, 5 * 0 + 7 * 1],
            [4 * 2 + 6 * 3, 5 * 2 + 7 * 3],
        ]
        mat_a = [
            ['a11', 'a12'],
            ['a21', 'a22'],
            ['a31', 'a32'],
        ]
        mat_b = [
            ['b11', 'b12', 'b13', 'b14'],
            ['b21', 'b22', 'b23', 'b24'],
        ]
        mat_c = [
            ['b11*a11 + b21*a12', 'b12*a11 + b22*a12', 'b13*a11 + b23*a12', 'b14*a11 + b24*a12'],
            ['b11*a21 + b21*a22', 'b12*a21 + b22*a22', 'b13*a21 + b23*a22', 'b14*a21 + b24*a22'],
            ['b11*a31 + b21*a32', 'b12*a31 + b22*a32', 'b13*a31 + b23*a32', 'b14*a31 + b24*a32'],
        ]
        A = [
            [0, 1, 2],
            [3, 4, 5],
        ]
        B = [
            [6, 7, 8, 9],
            [10, 11, 12, 13],
            [14, 15, 16, 17],
        ]
        C = [
            [6 * 0 + 10 * 1 + 14 * 2, 7 * 0 + 11 * 1 + 15 * 2, 8 * 0 + 12 * 1 + 16 * 2, 9 * 0 + 13 * 1 + 17 * 2],
            [6 * 3 + 10 * 4 + 14 * 5, 7 * 3 + 11 * 4 + 15 * 5, 8 * 3 + 12 * 4 + 16 * 5, 9 * 3 + 13 * 4 + 17 * 5],
        ]
        variables = [
            (lib.matrix_multiply, (A_xform_2, B_xform_1)),
            (lib.matrix_multiply, (mat_a, mat_b)),
            (lib.matrix_multiply, (A, B)),
        ]
        controls = [
            C_xform,
            mat_c,
            C,
        ]
        self.assert_null_hypothesis(variables, controls)


if __name__ == '__main__':
    tc = TestCase()
    tc.setUp()

    try:
        tc.test_case_0()
        tc.test_case_1()
        tc.test_case_2()
        tc.test_case_3()
        tc.test_case_4()
    finally:
        tc.tearDown()
