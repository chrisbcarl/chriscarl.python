#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
Author:         Chris Carl
Email:          chrisbcarl@outlook.com
Date:           2026-01-24
Description:

chriscarl.core.functors.parse.markdown unit test.

Updates:
    2026-01-24 - tests.chriscarl.core.functors.parse.markdown - initial commit
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
import chriscarl.core.functors.parse.markdown as lib

SCRIPT_RELPATH = 'tests/chriscarl/core/functors/parse/test_markdown.py'
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
        table_bad = '''
|a|b|
|--|---|
|hel|world|
'''
        table_pretty = '''|a  |b    |
|-- |---  |
|hel|world|'''

        variables = [
            (lib.table_prettify, (table_bad,)),
        ]
        controls = [
            table_pretty,
        ]
        self.assert_null_hypothesis(variables, controls)

    def test_case_1(self):
        table_bad = '''|col|col|col|
|---|---|---|
|a  |b  |a,b|'''
        table_pretty = '''|col|col|col|
|---|---|---|
|a  |b  |<ul><li>a</li><li>b</li></ul>|'''

        variables = [
            (lib.table_listified, (table_bad,)),
        ]
        controls = [
            table_pretty,
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
