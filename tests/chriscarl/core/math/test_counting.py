#!/usr/bin/env python
# -*- coding: utf-8 -*-
r'''
Author:         Chris Carl
Email:          chrisbcarl@outlook.com
Date:           2026-03-26
Description:

chriscarl.core.math.counting unit test.

pytest --cov=chriscarl.core.math.counting tests/chriscarl/core/math/test_counting.py --cov-report term-missing

Updates:
    2026-03-26 - tests.chriscarl.core.math.counting - initial commit
'''

# stdlib imports (expected to work)
from __future__ import absolute_import, print_function, division, with_statement  # , unicode_literals
import os
import sys
import logging
import unittest
from typing import Any
import math

# third party imports

# project imports (expected to work)
from chriscarl.core import constants
from chriscarl.core.lib.stdlib.os import abspath
from chriscarl.core.lib.stdlib.unittest import UnitTest

# test imports
import chriscarl.core.math.counting as lib

SCRIPT_RELPATH = 'tests/chriscarl/core/math/test_counting.py'
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

    def tearDown(self):
        # do other tear downs (tear down super after)
        super().tearDown()

    # @unittest.skip('lorem ipsum')
    def test_case_0(self):
        variables = [
            (lib.factorial, -1),
            (lib.factorial, 0),
            (lib.factorial, 1),
            (lib.factorial, 5),
        ]
        controls = [
            ValueError,
            1,
            1,
            120,
        ]
        self.assert_null_hypothesis(variables, controls)

    def test_case_1(self):
        variables = [
            (lib.permutation, (-1, -1)),
            (lib.permutation, (-1, 1)),
            (lib.permutation, (1, -1)),
            (lib.permutation, (5, 10)),
            (lib.permutation, (10, 10)),
            (lib.permutation, (10, 5)),
            (lib.permutation, (10, 1)),
            (lib.permutation, (10, 0)),
        ]
        controls = [
            ValueError,
            ValueError,
            ValueError,
            0,
            10 * 9 * 8 * 7 * 6 * 5 * 4 * 3 * 2 * 1,  # 10! ways to arrange 10 objects in 10 slots
            10 * 9 * 8 * 7 * 6,  # 5 slots, each used slot reduces the amount remaining to pick from
            10,  # 1 slot, only 10 ways to "fill" 1 slot
            1,  # no picks? only 1 way to fulfill no picks--pick nothing...
        ]
        self.assert_null_hypothesis(variables, controls)

    def test_case_2(self):
        variables = [
            (lib.combination, (-1, -1)),
            (lib.combination, (-1, 1)),
            (lib.combination, (1, -1)),
            (lib.combination, (5, 10)),
            (lib.combination, (10, 10)),
            (lib.combination, (10, 5)),
            (lib.combination, (10, 1)),
            (lib.combination, (10, 0)),
        ]
        controls = [
            ValueError,
            ValueError,
            ValueError,
            math.comb(5, 10),
            math.comb(10, 10),
            math.comb(10, 5),
            math.comb(10, 1),
            math.comb(10, 0),
        ]
        self.assert_null_hypothesis(variables, controls)


if __name__ == '__main__':
    tc = TestCase()
    tc.setUp()

    try:
        tc.test_case_0()
        tc.test_case_1()
        tc.test_case_2()
    finally:
        tc.tearDown()
