#!/usr/bin/env python
# -*- coding: utf-8 -*-
r'''
Author:         Chris Carl
Email:          chrisbcarl@outlook.com
Date:           2026-03-15
Description:

chriscarl.core.math.simple_linear_regression unit test.

pytest --cov=chriscarl.core.math.simple_linear_regression tests/chriscarl/core/math/test_simple_linear_regression.py --cov-report term-missing

Updates:
    2026-03-15 - tests.chriscarl.core.math.simple_linear_regression - initial commit
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
from chriscarl.core.lib.stdlib.io import read_text_file

# test imports
import chriscarl.core.math.simple_linear_regression as lib

SCRIPT_RELPATH = 'tests/chriscarl/core/math/test_simple_linear_regression.py'
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
        trout = read_text_file(abspath(constants.TESTS_COLLATERAL_DIRPATH, 'trout.txt'))
        # {@trout}
        self.X = [float(line.split('\t')[0]) for line in trout.splitlines()[1:]]
        self.Y = [float(line.split('\t')[1]) for line in trout.splitlines()[1:]]

    def tearDown(self):
        # do other tear downs (tear down super after)
        super().tearDown()

    # @unittest.skip('lorem ipsum')
    def test_case_0(self):
        variables = [
            (lib.least_squares, ([0, 1, 2], [0, 1])),
            (lib.least_squares, (list(range(10)), list(range(0, 20, 2)))),
            (lib.least_squares, (self.X, self.Y)),  # PCB = -1.451944 + 1.5577705*Age
        ]
        controls = [
            ValueError,
            (0, 2.0),
            (-1.4519, 1.5578),
        ]
        self.assert_null_hypothesis(variables, controls)


if __name__ == '__main__':
    tc = TestCase()
    tc.setUp()

    try:
        tc.test_case_0()
    finally:
        tc.tearDown()
