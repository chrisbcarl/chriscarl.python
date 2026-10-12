#!/usr/bin/env python
# -*- coding: utf-8 -*-
r'''
Author:         Chris Carl
Email:          chrisbcarl@outlook.com
Date:           2026-10-11
Description:

chriscarl.core.math.linear_algebra_2 unit test.

pytest --cov=chriscarl.core.math.linear_algebra_2 tests/chriscarl/core/math/test_linear_algebra_2.py --cov-report term-missing

Updates:
    2026-10-11 - tests.chriscarl.core.math.linear_algebra_2 - initial commit
'''

# stdlib imports (expected to work)
from __future__ import absolute_import, print_function, division, with_statement  # , unicode_literals
import os
import sys
import logging
import unittest
from typing import Any

# third party imports

# project imports (expected to work)
from chriscarl.core import constants
from chriscarl.core.lib.stdlib.os import abspath
from chriscarl.core.lib.stdlib.unittest import UnitTest

# test imports
import chriscarl.core.math.linear_algebra_2 as lib

SCRIPT_RELPATH = 'tests/chriscarl/core/math/test_linear_algebra_2.py'
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
        super().setUp()
        # do other set ups (set up super first)
        self.A = [
            [1, 2, 3],
            [4, 5, 6],
            [7, 8, 9],
        ]
        self.B = [
            [1, 2],
            [3, 4],
            [5, 6],
        ]
        self.ge_A = [
            [2, 1, -1],
            [-3, -1, 2],
            [-2, 1, 2],
        ]
        self.ge_b = [
            [8],
            [-11],
            [-3],
        ]
        self.v = [
            [1],
            [2],
            [3],
        ]
        self.A_latex = r'''\begin{bmatrix}
    1 & 2 & 3 \\
    4 & 5 & 6 \\
    7 & 8 & 9 \\
\end{bmatrix}'''

    def tearDown(self):
        # do other tear downs (tear down super after)
        super().tearDown()

    def test_case_0(self):
        variables = [
            (lib.is_vector, self.v),
            (lib.is_matrix, self.A),
            (lib.is_matrix, (self.v, self.A)),
            (lib.is_matrix, ([1, 2, 3], )),  # row vector not a real boy
            (lib.to_matrix, self.A_latex),
            (lib.to_latex, self.A),
            (lib.to_str, self.A),
            (lib.create, (3, 3), dict(val=69)),
            (lib.create, (3, 3), dict(val=lambda m, n: m * n)),
            (lib.dimensions, self.v),
            (lib.dimensions, self.A),
            (lib.is_addable, (self.v, self.v)),
            (lib.is_addable, (self.v, self.A)),
            (lib.is_multipliable, (self.v, self.v)),  # nope, 3x1 * 3x1
            (lib.is_multipliable, (self.A, self.A)),
            (lib.is_multipliable, (self.A, self.B)),
            (lib.is_multipliable, (self.v, self.A)),  # nope, 3x1 * 3x3
            (lib.is_multipliable, (self.A, self.B)),  # a linear combination, 3x3 * 3*1 = 3x3
        ]
        controls = [
            True,
            True,
            True,
            False,
            self.A,
            self.A_latex,
            '''1 2 3
4 5 6
7 8 9''',
            [
                [69, 69, 69],
                [69, 69, 69],
                [69, 69, 69],
            ],
            [
                [1, 2, 3],
                [2, 4, 6],
                [3, 6, 9],
            ],
            (3, 1),
            (3, 3),
            True,
            False,
            False,
            True,
            True,
            False,
            True,
        ]
        self.assert_null_hypothesis(variables, controls)

        print(lib.to_str(self.A))
        P, L, U, rref, A_inverse, ops_string = lib.gaussian_elimination(self.ge_A, floating=True)
        print(ops_string)


if __name__ == '__main__':
    tc = TestCase()
    tc.setUp()

    try:
        tc.test_case_0()
    finally:
        tc.tearDown()
