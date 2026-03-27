#!/usr/bin/env python
# -*- coding: utf-8 -*-
r'''
Author:         Chris Carl
Email:          chrisbcarl@outlook.com
Date:           2026-03-26
Description:

chriscarl.core.math.probability unit test.

pytest --cov=chriscarl.core.math.probability tests/chriscarl/core/math/test_probability.py --cov-report term-missing

Updates:
    2026-03-26 - tests.chriscarl.core.math.probability - initial commit
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
import chriscarl.core.math.probability as lib

SCRIPT_RELPATH = 'tests/chriscarl/core/math/test_probability.py'
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
            (lib.binomial_pdf, (5, 10, 0.5)),  # exactly 5 heads
            (lib.binomial_pdf, (300, 1000, 0.28)),  # exactly 300 failures
            (lib.binomial_cdf, (4, 10, 0.5)),  # phrased as P(X < 5) heads
            (lib.binomial_exact_test, (300, 1000, 0.28)),  # phrased as P(X > 300) failures
        ]
        controls = [
            0.2461,
            0.0103,
            0.3770,
            1 - 0.0751,
        ]
        self.assert_null_hypothesis(variables, controls)


if __name__ == '__main__':
    tc = TestCase()
    tc.setUp()

    try:
        tc.test_case_0()
    finally:
        tc.tearDown()
