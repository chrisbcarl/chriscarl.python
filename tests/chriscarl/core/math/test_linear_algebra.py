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
        A_vecs = [
            [
                [0],
                [3],
            ],
            [
                [1],
                [4],
            ],
            [
                [2],
                [5],
            ],
        ]
        variables = [
            (lib.is_addable, (self.A_mat, self.A_mat)),
            (lib.is_addable, (self.A_mat, self.B_mat)),
            (lib.add, (self.A_mat, self.A_mat)),
            (lib.scalar_multiply, (1, self.A_mat)),
            (lib.scalar_multiply, (-2, self.A_mat)),
            (lib.matrix_to_vectors, self.C_vec),  # generator
            (lib.matrix_to_vectors, self.A_mat),
            (lib.matrix_to_vectors, [1, 2, 3]),
        ]
        controls = [True, False, pos2, self.A_mat, neg2, [self.C_vec], A_vecs, ValueError]
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
        variables = [
            (lib.vector_multiply, (self.A_mat, self.C_vec)),
            (lib.vector_multiply, (self.B_mat, self.C_vec)),
        ]
        controls = [
            AxC,
            BxC,
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
    finally:
        tc.tearDown()
