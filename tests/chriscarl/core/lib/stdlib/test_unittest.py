#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
Author:         Chris Carl
Email:          chrisbcarl@chriscarl.com
Date:           2024-11-23
Description:

chriscarl.core.lib.stdlib.unittest unit test.

Updates:
    2024-11-23 - tests.chriscarl.core.lib.stdlib.unittest - initial commit
'''

# stdlib imports (expected to work)
from __future__ import absolute_import, print_function, division, with_statement  # , unicode_literals
import os
import sys
import time
import logging
import unittest

# third party imports

# project imports (expected to work)
from chriscarl.core.lib.stdlib.unittest import UnitTest

# test imports
import chriscarl.core.lib.stdlib.unittest as lib

SCRIPT_RELPATH = 'tests/chriscarl/core/lib/stdlib/test_unittest.py'
if not hasattr(sys, '_MEIPASS'):
    SCRIPT_FILEPATH = os.path.abspath(__file__)
else:
    SCRIPT_FILEPATH = os.path.abspath(os.path.join(sys._MEIPASS, SCRIPT_RELPATH))  # pylint: disable=no-member
SCRIPT_DIRPATH = os.path.dirname(SCRIPT_FILEPATH)
SCRIPT_NAME = os.path.splitext(os.path.basename(__file__))[0]
THIS_MODULE = sys.modules[__name__]
LOGGER = logging.getLogger(__name__)
LOGGER.addHandler(logging.NullHandler())


class TestCase(UnitTest):

    def setUp(self):
        return super().setUp()

    def tearDown(self):
        return super().tearDown()

    def test_case_0_assert_null_hypothesis(self):
        variables = [
            (print),
            (print, ''),
            (sum, ([1, 2, 3], ), {}),
            (len, ([1, 2, 3]), {}),
            (len, 1),
            (lambda: 'this is true'),
            (lambda: ''),  # this is false
        ]
        controls = [
            None,
            None,
            6,
            3,
            TypeError,
            True,
            False,
        ]
        self.assert_null_hypothesis(variables, controls)

    def test_case_1_assert_subset(self):
        variables = [
            (lib.UnitTest.assert_subset, ([1, 2, 3], [1, 2, 3, 4])),
            (lib.UnitTest.assert_subset, ('abc', 'dcba')),
            (lib.UnitTest.assert_subset, ('abc', ['a', 'b', 'c'])),
        ]
        controls = [
            True,
            True,
            AssertionError,
        ]
        self.assert_null_hypothesis(variables, controls)

    def test_case_2_infrastructure(self):
        bad_length_variables = [
            (print),
        ]
        bad_length_controls = [
            None,
            None,
        ]
        self.assertRaises(ValueError, lib.UnitTest.assert_null_hypothesis, bad_length_variables, bad_length_controls)

        bad_exceptions_variables = [
            (print),
        ]
        bad_exceptions_controls = [
            Exception,
        ]
        self.assertRaises(AssertionError, lib.UnitTest.assert_null_hypothesis, bad_exceptions_variables, bad_exceptions_controls)

        def asserts():
            assert 1 == 2

        good_assertion_variables = [
            asserts,
        ]
        good_assertion_controls = [
            False,
        ]
        self.assertRaises(AssertionError, lib.UnitTest.assert_null_hypothesis, good_assertion_variables, good_assertion_controls)


if __name__ == '__main__':
    tc = TestCase()
    tc.setUp()

    tc.test_case_0_assert_null_hypothesis()
    tc.test_case_1_assert_subset()
    tc.test_case_2_infrastructure()

    tc.tearDown()
