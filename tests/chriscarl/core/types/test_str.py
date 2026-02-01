#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
Author:         Chris Carl
Email:          chrisbcarl@outlook.com
Date:           2024-11-26
Description:

chriscarl.core.types.string unit test.

Updates:
    2024-11-26 - tests.chriscarl.core.types.string - initial commit
'''

# stdlib imports (expected to work)
from __future__ import absolute_import, print_function, division, with_statement  # , unicode_literals
import os
import sys
import logging
import unittest

# third party imports

# project imports (expected to work)
from chriscarl.core.lib.stdlib.unittest import UnitTest

# test imports
import chriscarl.core.types.str as lib

SCRIPT_RELPATH = 'tests/chriscarl/core/types/test_str.py'
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

    def test_case_0_find_index(self):
        variables = [
            (lib.find_index, ('abc', 'abcabcabc')),
            (lib.find_index, ('abc', 'abbcabccabc')),
        ]
        controls = [
            [0, 3, 6],
            [4, 8],
        ]
        self.assert_null_hypothesis(variables, controls)

    def test_case_1_size_to_bytes(self):
        variables = [
            (lib.size_to_bytes, '1024 b'),
            (lib.size_to_bytes, '1 Mb'),
            (lib.size_to_bytes, '1Gb'),
            (lib.size_to_bytes, '1024'),
            (lib.size_to_bytes, '1024b'),
            (lib.size_to_bytes, '1M'),
            (lib.size_to_bytes, '1 M'),
            (lib.size_to_bytes, '1G'),
            (lib.size_to_bytes, '1 G'),
            (lib.size_to_bytes, '1tb', dict(into='g')),
            (lib.size_to_bytes, '1tb', dict(into='m')),
            (lib.size_to_bytes, '1tb', dict(into='k')),
            (lib.size_to_bytes, '1tb', dict(into='b')),
        ]
        controls = [
            1024**1,
            1024**2,
            1024**3,
            2**10,
            2**10,
            2**20,
            2**20,
            2**30,
            2**30,
            1024**1,
            1024**2,
            1024**3,
            1024**4,
        ]
        self.assert_null_hypothesis(variables, controls)

    def test_case_2_unicode(self):
        variables = [
            (lib.strip_unicode, '\u0026'),
            (lib.strip_unicode, '\x26'),
        ]
        controls = [
            '&',
            '&',
        ]
        self.assert_null_hypothesis(variables, controls)

    def test_case_3_contains(self):
        variables = [
            (lib.contains_insensitive, ('abc123', 'A')),
            (lib.contains_all_insensitive, ('abc123', ['A', 'B', 'C', 1, 2, 3])),
            (lib.contains_any_insensitive, ('abc123', ['A', None])),
            (lib.contains_any_insensitive, ('abc123', None)),
        ]
        controls = [
            True,
            True,
            True,
            False,
        ]
        self.assert_null_hypothesis(variables, controls)

    def test_case_4(self):
        variables = [
            (lib.indent, ('abc\n123', )),
        ]
        controls = [
            '    abc\n    123',
        ]
        self.assert_null_hypothesis(variables, controls)


if __name__ == '__main__':
    tc = TestCase()
    tc.setUp()

    try:
        tc.test_case_0_find_index()
        tc.test_case_1_size_to_bytes()
        tc.test_case_2_unicode()
        tc.test_case_3_contains()
        tc.test_case_4()
    finally:
        tc.tearDown()
