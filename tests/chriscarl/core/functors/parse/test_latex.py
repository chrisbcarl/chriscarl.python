#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
Author:         Chris Carl
Email:          chrisbcarl@outlook.com
Date:           2026-01-25
Description:

chriscarl.core.functors.parse.latex unit test.

Updates:
    2026-01-25 - tests.chriscarl.core.functors.parse.latex - initial commit
'''

# stdlib imports (expected to work)
from __future__ import absolute_import, print_function, division, with_statement  # , unicode_literals
import os
import sys
import logging
import unittest
import re

# third party imports

# project imports (expected to work)
from chriscarl.core import constants
from chriscarl.core.lib.stdlib.os import abspath
from chriscarl.core.lib.stdlib.unittest import UnitTest

# test imports
import chriscarl.core.functors.parse.latex as lib

SCRIPT_RELPATH = 'tests/chriscarl/core/functors/parse/test_latex.py'
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
            (lib.latex_escape, (r'\_#$', )),
            (lib.latex_escape, (r'\_#$', ), dict(regex=r'([^\\])([$%&~_^{}])')),
        ]
        controls = [
            r'\_\#\$',
            r'\_#\$',
        ]
        self.assert_null_hypothesis(variables, controls)

    def test_case_1(self):
        rows = [{'a': 'b'}, {'c': 'd'}]
        output = lib.rows_to_latex(rows, caption='caption', label='label')
        print(output)
        self.assertIn('a & c', output)
        self.assertIn('b ', output)
        self.assertIn('d ', output)
        self.assertIn('\\caption{caption}', output)
        self.assertIn('\\label{label}', output)

if __name__ == '__main__':
    tc = TestCase()
    tc.setUp()

    try:
        tc.test_case_0()
        tc.test_case_1()
    finally:
        tc.tearDown()
