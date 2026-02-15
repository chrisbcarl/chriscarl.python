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
            (lib.latex_escape_raw, (r'\_#$', )),
            (lib.latex_escape_raw, (r'\_#$', ), dict(regex=r'([^\\])([$%&~_^{}])')),
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

    def test_case_2(self):
        variables = [
            # no change
            (lib.latex_escape, (r'\LaTeX', )),
            (lib.latex_escape, (r'\LaTeX is \(\text{great!}\)', )),
            (lib.latex_escape, (r'``\(\bar{X}\)":', )),
            (lib.latex_escape, (r'just use \lstinline{<>} and If', )),
            (lib.latex_escape, (r'inc so: \cite[pp. 69-99]{CitekeyProceedings}.', )),
            (lib.latex_escape, (r'u want \textbf{\emph{bolded and italicized}}, use ', )),
            # change
            (lib.latex_escape, (r'\LaTeX is 100% \(\text{great!}\)', )),
            (lib.latex_escape, (r'____', )),
        ]
        controls = [
            # no change
            r'\LaTeX',
            r'\LaTeX is \(\text{great!}\)',
            r'``\(\bar{X}\)":',
            r'just use \lstinline{<>} and If',
            r'inc so: \cite[pp. 69-99]{CitekeyProceedings}.',
            r'u want \textbf{\emph{bolded and italicized}}, use ',
            # change
            r'\LaTeX is 100\% \(\text{great!}\)',
            r'\_\_\_\_',
        ]
        self.assert_null_hypothesis(variables, controls)

    def test_case_3(self):
        variables = [
            (lib.latex_replace, (r'you know where that path leads… and you know thats not where you want to be', )),
        ]
        controls = [
            r'you know where that path leads\cdots and you know thats not where you want to be',
        ]
        self.assert_null_hypothesis(variables, controls)

    def test_case_4(self):
        whole = 57
        frac = 0.1875
        variables = [
            (lib.evaluate, (r'1*2^0 + 0*2^1 + 0*2^2 + 1*2^3 + 1*2^4 + 1*2^5', )),
            (lib.evaluate, (r'\frac{0}{2^1} + \frac{0}{2^2} + \frac{1}{2^3} + \frac{1}{2^4}', )),
            (lib.evaluate, (r'\sqrt{\frac{1}{2^2}}', )),
            (lib.evaluate, (r'\sqrt{\frac{1}{4}((50 - 56)^2 + (40 - 56)^2 + (70 - 56)^2 + (75 - 56)^2 + (45 - 56)^2)}', )),
            (lib.evaluate, (r'\frac{56 - 70}{\frac{15.572411502397436}{\sqrt{5}}}', )),
        ]
        controls = [
            whole,
            frac,
            0.5,
            15.572411502397436,
            -2.01,
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
