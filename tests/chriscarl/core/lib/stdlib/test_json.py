#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
Author:         Chris Carl
Email:          chrisbcarl@outlook.com
Date:           2024-11-26
Description:

chriscarl.core.lib.stdlib.json unit test.

Updates:
    2024-11-26 - tests.chriscarl.core.lib.stdlib.json - initial commit
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
import chriscarl.core.lib.stdlib.json as lib

SCRIPT_RELPATH = 'tests/chriscarl/core/lib/stdlib/test_json.py'
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
        super().setUp()
        self.dict = {
            'str': 'str',
            'int': 1,
            'float': 3.14,
            'bool': False,
            'list': [1, 2, 3],
            'dict': {
                'key': 'value'
            },
        }

    def tearDown(self):
        super().tearDown()

    def test_case_0_write_read(self):
        os.remove(self.tempfile)  # NOTE: at this point, self.tempfile is empty, so it would badly, might as well remove
        with lib.ReadWriteJson(self.tempfile) as rwj:
            rwj.body = {'a': True}
        variables = [
            (lib.read_json, (self.tempfile)),
            (lib.write_json, (self.tempfile, self.dict)),
            (lib.read_json, (self.tempfile)),
            (lib.read_json_list, (self.tempfile)),  # non list and list are the same, its just a type hint
        ]
        controls = [
            {
                'a': True
            },
            None,
            self.dict,
            self.dict,
        ]
        self.assert_null_hypothesis(variables, controls)

    def test_case_1_dict_to_string(self):
        variables = [
            (lib.dict_to_string, {}, dict(indent=None)),
            (lib.dict_to_string, {
                1: 1
            }, dict(indent=None)),
            (lib.dict_to_string, {
                '1': '1'
            }, dict(indent=None)),
        ]
        controls = [
            r'{}',
            r'{"1": 1}',
            r'{"1": "1"}',
        ]
        self.assert_null_hypothesis(variables, controls)


if __name__ == '__main__':
    tc = TestCase()
    tc.setUp()

    try:
        tc.test_case_0_write_read()
        tc.test_case_1_dict_to_string()
    finally:
        tc.tearDown()
