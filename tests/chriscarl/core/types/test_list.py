#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
Author:         Chris Carl
Email:          chrisbcarl@outlook.com
Date:           2024-11-25
Description:

chriscarl.core.types.list unit test.

Updates:
    2024-11-25 - tests.chriscarl.core.types.list - initial commit
'''

# stdlib imports (expected to work)
from __future__ import absolute_import, print_function, division, with_statement  # , unicode_literals
import os
import sys
import logging
import unittest
from typing import List

# third party imports

# project imports (expected to work)
from chriscarl.core.lib.stdlib.unittest import UnitTest

# test imports
import chriscarl.core.types.list as lib

SCRIPT_RELPATH = 'tests/chriscarl/core/types/test_list.py'
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
        self.num_list = [1, 2, 2, 3, 3, 3]
        self.ten = list(range(10))
        return super().setUp()

    def tearDown(self):
        return super().tearDown()

    def test_case_0_dedupe(self):
        variables = [
            (lib.dedupe, self.num_list),
        ]
        controls = [
            [1, 2, 3],
        ]
        self.assert_null_hypothesis(variables, controls)

    def test_case_1_find_index(self):
        variables = [
            (lib.find_index, (lambda x: x > 0, self.num_list)),
            (lib.find_index, (lambda x: x > 1, self.num_list)),
            (lib.find_index, (lambda x: x > 2, self.num_list)),
        ]
        controls = [
            [i for i, ele in enumerate(self.num_list) if ele > 0],
            [i for i, ele in enumerate(self.num_list) if ele > 1],
            [i for i, ele in enumerate(self.num_list) if ele > 2],
        ]
        self.assert_null_hypothesis(variables, controls)

    def test_case_2_sorted_list_by_frequency(self):
        variables = [
            (lib.sorted_list_by_frequency, self.num_list, dict(ascending=True)),
            (lib.sorted_list_by_frequency, self.num_list, dict(ascending=False)),
        ]
        controls = [
            [1, 2, 3],
            [3, 2, 1],
        ]
        self.assert_null_hypothesis(variables, controls)

    def test_case_3_as_list(self):
        variables = [
            (lib.as_list, ([1], List[int])),
            (lib.as_list, (1, List[int])),
        ]
        controls = [
            [1],
            [1],
        ]
        self.assert_null_hypothesis(variables, controls)

    def test_case_4_n_sized_chunks(self):
        variables = [
            (lib.n_sized_chunks, (self.ten, 0)),
            (lib.n_sized_chunks, (self.ten, 1)),
            (lib.n_sized_chunks, (self.ten, 2)),
            (lib.n_sized_chunks, (self.ten, 3)),
            (lib.n_sized_chunks, (self.ten, 4)),
        ]
        controls = [
            ValueError,
            [[i] for i in self.ten],
            [[0, 1], [2, 3], [4, 5], [6, 7], [8, 9]],
            [[0, 1, 2], [3, 4, 5], [6, 7, 8], [9]],
            [[0, 1, 2, 3], [4, 5, 6, 7], [8, 9]],
        ]
        self.assert_null_hypothesis(variables, controls)

    def test_case_5_n_chunks(self):
        variables = [
            (lib.n_chunks, (self.ten, 0)),
            (lib.n_chunks, (self.ten, 1)),
            (lib.n_chunks, (self.ten, 2)),
            (lib.n_chunks, (self.ten, 3)),
            (lib.n_chunks, (self.ten, 4)),
        ]
        controls = [
            ValueError,
            [self.ten],  # since that's how it'll be evaluated
            [[0, 1, 2, 3, 4], [5, 6, 7, 8, 9]],
            [[0, 1, 2, 3], [4, 5, 6], [7, 8, 9]],
            [[0, 1, 2], [3, 4, 5], [6, 7], [8, 9]],
        ]
        self.assert_null_hypothesis(variables, controls)

    def test_case_6(self):
        rows = [
            {'a': None},
            {'b': [1, 2, 3]},
        ]
        variables = [
            (lib.rows_to_str_rows, ([{'a': {}}], )),
            (lib.rows_to_str_rows, (rows, ), dict(on_list=lambda s: str(s))),
        ]
        controls = [
            NotImplementedError,
            (
                [
                    {'a': ''},
                    {'b': '[1, 2, 3]'},
                ],  # converted rows to strings only
                ['a', 'b'],  # list of headers
                9  # max string length
            ),
        ]
        self.assert_null_hypothesis(variables, controls)


if __name__ == '__main__':
    tc = TestCase()
    tc.setUp()

    try:
        # tc.test_case_0_dedupe()
        # tc.test_case_1_find_index()
        # tc.test_case_2_sorted_list_by_frequency()
        # tc.test_case_3_as_list()
        # tc.test_case_4_n_sized_chunks()
        # tc.test_case_5_n_chunks()
        tc.test_case_6()
    finally:
        tc.tearDown()
