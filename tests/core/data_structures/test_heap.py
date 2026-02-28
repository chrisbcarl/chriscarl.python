#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
Author:         Chris Carl
Email:          chrisbcarl@outlook.com
Date:           2026-02-15
Description:

chriscarl.core.algorithms.heap unit test.

pytest --cov=chriscarl.core.data_structures.heap tests/core/data_structures/test_heap.py --cov-report term-missing

Updates:
    2026-02-15 - tests.chriscarl.core.algorithms.heap - initial commit
'''

# stdlib imports (expected to work)
from __future__ import absolute_import, print_function, division, with_statement  # , unicode_literals
import os
import sys
import logging
import unittest
from typing import Any
import random

# third party imports

# project imports (expected to work)
from chriscarl.core import constants
from chriscarl.core.lib.stdlib.os import abspath
from chriscarl.core.lib.stdlib.unittest import UnitTest

# test imports
import chriscarl.core.data_structures.heap as lib

SCRIPT_RELPATH = 'tests/core/algorithms/test_heap.py'
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
            (lib.is_heap, [], dict(max_heap=True)),
            (lib.is_heap, [0], dict(max_heap=True)),
            (lib.is_heap, [1, 0], dict(max_heap=True)),
            (lib.is_heap, [2, 1, 0], dict(max_heap=True)),
            (lib.is_heap, [1, 2, 0], dict(max_heap=True)),
            (lib.is_heap, [], dict(max_heap=False)),
            (lib.is_heap, [0], dict(max_heap=False)),
            (lib.is_heap, [0, 1], dict(max_heap=False)),
            (lib.is_heap, [0, 1, 2], dict(max_heap=False)),
            (lib.is_heap, [2, 1, 0], dict(max_heap=False)),
            (lib.is_heap, [random.randint(0, 100) for _ in range(100)], dict(max_heap=False)),  # nearly impossible
        ]
        controls = [
            True,
            True,
            True,
            True,
            False,
            True,
            True,
            True,
            True,
            False,
            False,
        ]
        self.assert_null_hypothesis(variables, controls)

    # @unittest.skip('lorem ipsum')
    def test_case_1(self):
        upper = 32
        variables = []
        controls = []
        for _ in range(10):
            lst0 = [random.randint(0, random.randint(0, upper)) for _ in range(random.randint(0, upper))]
            lst1 = lst0[:]
            ascending = list(sorted(lst0))
            descending = list(sorted(lst1, reverse=True))
            variables += [
                (lib.heapsort, lst0),
                (lst0.__eq__, ascending),
                (lib.heapsort, lst1, dict(ascending=False)),
                (lst1.__eq__, descending),
            ]
            controls += [
                Any,
                True,
                Any,
                True,
            ]
            self.assert_null_hypothesis(variables, controls)


if __name__ == '__main__':
    tc = TestCase()
    tc.setUp()

    try:
        tc.test_case_0()
        tc.test_case_1()
    finally:
        tc.tearDown()
