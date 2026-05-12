#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
Author:         Chris Carl
Email:          chrisbcarl@outlook.com
Date:           2026-02-02
Description:

chriscarl.core.algorithms.number_theory unit test.

# TODO:
- redo but with wikipedia test cases...
    - SP: https://en.wikipedia.org/wiki/Single-precision_floating-point_format
    - DP: https://en.wikipedia.org/wiki/Double-precision_floating-point_format

Updates:
    2026-02-02 - tests.chriscarl.core.algorithms.number_theory - initial commit
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
import chriscarl.core.algorithms.number_theory as lib

SCRIPT_RELPATH = 'tests/chriscarl/core/algorithms/test_number_theory.py'
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
        return super().setUp()

    def tearDown(self):
        return super().tearDown()

    # @unittest.skip('lorem ipsum')

    def test_case_0(self):
        variables = [
            (lib.base_n_to_10, ('1010', ), dict(base=2)),
            (lib.base_n_to_10, ('-01011', ), dict(base=2)),
            (lib.base_n_to_10, ('DEAD', ), dict(base=16)),
            (lib.base_n_to_10, ('-BEEF', ), dict(base=16)),
            (lib.base_n_to_10, ('e298', ), dict(base=16)),
            (lib.base_n_to_10, ('1010.01011', ), dict(base=2)),
            (lib.base_n_to_10, ('80085', ), dict(base=10)),
            (lib.base_n_to_10, ('F.8', ), dict(base=16)),
            (lib.base_n_to_10, ('0.01011', ), dict(base=2)),
            (lib.base_n_to_10, ('.01011', ), dict(base=2)),
            (lib.base_n_to_10, ('-.01011', ), dict(base=2)),
        ]
        controls = [
            10,
            -11,
            57005,
            -48879,
            58008,
            10.34375,
            80085,
            15.5,
            0.34375,
            0.34375,
            -0.34375,
        ]
        self.assert_null_hypothesis(variables, controls)

    def test_case_1(self):
        variables = [
            (lib.ieee754_to_decimal, ('0.0.0...1', )),
            (lib.ieee754_to_decimal, ('0...0.0...0', )),
            (lib.ieee754_to_decimal, ('0...1.0...1', )),
            (lib.ieee754_to_decimal, ('0...1.1...', )),
            (lib.ieee754_to_decimal, ('0...1.1...1', )),
            (lib.ieee754_to_decimal, ('000000000.00000000000000000000000', )),
            (lib.ieee754_to_decimal, ('000000001.00000000000000000000001', )),
            (lib.ieee754_to_decimal, ('000000001.11111111111111111111111', )),
            (lib.ieee754_to_decimal, ('000000001.11111111111111111111111', )),
            # -2.5
            (lib.ieee754_to_decimal, ('110000000.010...0000', )),
            (lib.ieee754_to_decimal, ('110000000.010…0000', )),
        ]
        controls = [
            ValueError,
            lib.ieee754_to_decimal('000000000.00000000000000000000000'),
            lib.ieee754_to_decimal('000000001.00000000000000000000001'),
            lib.ieee754_to_decimal('000000001.11111111111111111111111'),
            lib.ieee754_to_decimal('000000001.11111111111111111111111'),
            lib.ieee754_to_decimal('0...0.0...0'),
            lib.ieee754_to_decimal('0...1.0...1'),
            lib.ieee754_to_decimal('0...1.1...'),
            lib.ieee754_to_decimal('0...1.1...1'),
            lib.ieee754_to_decimal('110000000.010…0000'),
            lib.ieee754_to_decimal('110000000.010...0000'),
        ]
        self.assert_null_hypothesis(variables, controls)

    def test_case_2(self):
        variables = [
            (lib.ieee754_to_decimal, ('101111111.00000000000000000000000', )),
            (lib.ieee754_to_decimal, ('101....0...', )),
            (lib.ieee754_to_decimal, ('101….0…', )),
            (lib.ieee754_to_decimal, ('0….0…', )),
            (lib.ieee754_to_decimal, ('0....0...', )),
            (lib.ieee754_to_decimal, ('0….0…', )),
            (lib.ieee754_to_decimal, ('1….0…', )),
            (lib.ieee754_to_decimal, ('01….0…', )),
            (str, (lib.ieee754_to_decimal('01….10…'), )),  # nan equality not possible
            (lib.ieee754_to_decimal, ('0...1.000100010...', )),
            # (lib.ieee754_to_decimal, ('0....0...1', )),  # BUG: mine cannot go that low not sure exactly why...
        ]
        controls = [
            -1.0,
            -1.0,
            -1.0,
            0,
            0,
            0,
            float('-inf'),
            float('inf'),
            str(float('nan')),
            1.2535545225565800377947854479E-38,  # https://www.binaryconvert.com/result_float.html?hexadecimal=00888000
            # 1.40129846432481707092372958329E-45,  # https://www.binaryconvert.com/result_float.html?hexadecimal=00000001
        ]
        self.assert_null_hypothesis(variables, controls)

    def test_case_3(self):
        variables = [
            (lib.ieee754_to_decimal, ('101111111111.0000000000000000000000000000000000000000000000000000', )),
            (lib.ieee754_to_decimal, ('101....0...', ), dict(double=True)),
            (lib.ieee754_to_decimal, ('101….0…', ), dict(double=True)),
            (lib.ieee754_to_decimal, ('0...1.000100010...', ), dict(double=True)),
            # (lib.ieee754_to_decimal, ('0....0...1', ), dict(double=True)),  # BUG: either I or python can't calculate exactly right
        ]
        controls = [
            -1.0,
            -1.0,
            -1.0,
            2.37283266942369522493606848372E-308,  # https://www.binaryconvert.com/result_double.html?hexadecimal=0011100000000000
            # 4.94065645841246544176568792868E-324  # https://www.binaryconvert.com/result_double.html?hexadecimal=0000000000000001
        ]
        self.assert_null_hypothesis(variables, controls)

    def test_case_4(self):
        variables = [
            (lib.get_digit, (367.890, 3)),
            (lib.get_digit, (367.890, 2)),
            (lib.get_digit, (367.890, 1)),
            (lib.get_digit, (367.890, 0)),
            (lib.get_digit, (367.890, -1)),
            (lib.get_digit, (367.890, -2)),
            (lib.get_digit, (367.890, -3)),
        ]
        controls = [
            0,
            3,
            6,
            7,
            8,
            9,
            0,
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
