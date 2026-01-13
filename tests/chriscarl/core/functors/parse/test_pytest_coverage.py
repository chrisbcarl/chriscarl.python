#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
Author:         Chris Carl
Email:          chrisbcarl@outlook.com
Date:           2024-11-29
Description:

chriscarl.core.functors.parse unit test.

Updates:
    2024-11-29 - tests.chriscarl.core.functors.parse - initial commit
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
from chriscarl.core.lib.stdlib.unittest import UnitTest
from chriscarl.core.lib.stdlib.io import read_text_file
from chriscarl.core.lib.stdlib.os import abspath

# test imports
import chriscarl.core.functors.parse.pytest_coverage as lib

SCRIPT_RELPATH = 'tests/chriscarl/core/functors/parse/test_pytest_coverage.py'
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

    def test_case_0_PytestCoverage(self):
        pytest_coverage_text = read_text_file(abspath(constants.TEST_COLLATERAL_DIRPATH, 'pytest-coverage.txt'))
        pytest_coverages = lib.PytestCoverage.parse_coverage(pytest_coverage_text)
        for pytest_coverage in pytest_coverages:
            LOGGER.debug(pytest_coverage)
        self.assertGreater(len(pytest_coverages), 0)

        variables = [
            (lib.PytestCoverage.parse_tests, pytest_coverage_text),
        ]
        controls = [
            [
                ('tests\\chriscarl\\tools\\shed\\test_dev.py', 70, 'AssertionError'),
                ('tests\\chriscarl\\tools\\shed\\test_dev.py', 113, 'AssertionError'),
            ],
        ]
        self.assert_null_hypothesis(variables, controls)


if __name__ == '__main__':
    tc = TestCase()
    tc.setUp()

    tc.test_case_0_PytestCoverage()

    tc.tearDown()
