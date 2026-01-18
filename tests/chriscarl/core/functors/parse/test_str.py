#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
Author:         Chris Carl
Email:          chrisbcarl@outlook.com
Date:           2026-01-09
Description:

chriscarl.core.functors.parse.str unit test.

Updates:
    2026-01-09 - tests.chriscarl.core.functors.parse.str - initial commit
'''

# stdlib imports (expected to work)
from __future__ import absolute_import, print_function, division, with_statement  # , unicode_literals
import os
import sys
import logging
import unittest
import json

# third party imports

# project imports (expected to work)
from chriscarl.core import constants
from chriscarl.core.lib.stdlib.os import abspath
from chriscarl.core.lib.stdlib.unittest import UnitTest

# test imports
import chriscarl.core.functors.parse.str as lib

SCRIPT_RELPATH = 'tests/chriscarl/core/functors/parse/test_str.py'
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

    # @unittest.skip('lorem ipsum')
    def test_case_0_parenthesis_extract(self):
        dicts = '''
            {'a': 1},
            {'b': 2},
            {'c': 3},
        '''
        enclose = f'[{dicts}]'
        large = f'''({enclose})
        '''
        variables = [
            (lib.parenthesis_extract, ('what is (beauty)?', ), dict(open_char='(', close_char=')')),
            (lib.parenthesis_extract, ('[{"a": {{"b": True}}}]', ), dict(open_char='{', close_char='}')),
            (lib.parenthesis_extract, (large, ), dict(open_char='[', close_char=']')),
        ]
        controls = [
            '(beauty)',
            '{"a": {{"b": True}}}',
            enclose,
        ]
        self.assert_null_hypothesis(variables, controls)

    def test_case_1_lines_to_dict(self):
        lines0 = '''
hello
world
        '''
        lines1 = '''
:authority
www.instagram.com
:method
GET
:path
/reels/DMnok06McaT/
        '''
        lines2 = '''
:scheme
https
accept
text/html
accept-encoding
gzip, deflate, br, zstd
        '''
        variables = [
            (lib.lines_to_dict, lines0),
            (lib.lines_to_headers, lines1),
            (lib.lines_to_headers, lines2),
        ]
        controls = [
            {
                'hello': 'world'
            },
            {},
            {
                'accept': 'text/html',
                'accept-encoding': 'gzip, deflate, br, zstd'
            },
        ]
        self.assert_null_hypothesis(variables, controls)

    def test_case_2_get_dict_value_by_text_key(self):
        dick = {
            'a': {
                'b': [
                    {
                        'c': 1
                    },
                    {
                        'c': 2
                    },
                ]
            }
        }
        text = json.dumps(dick)

        variables = [
            (lib.get_dict_value_by_text_key, ('a', dick)),
            (lib.get_dict_value_by_text_key, ('a', text)),
            (lib.get_dict_value_by_text_key, ('b', text)),
            (lib.get_dict_value_by_text_key, ('c', text)),
        ]
        controls = [
            TypeError,
            dick['a'],
            dick['a']['b'],
            1,
        ]
        self.assert_null_hypothesis(variables, controls)

        variables = [
            (lib.get_dict_values_by_text_key, ('c', text)),
        ]
        controls = [
            [1, 2],
        ]
        self.assert_null_hypothesis(variables, controls)


if __name__ == '__main__':
    tc = TestCase()
    tc.setUp()

    tc.test_case_0_parenthesis_extract()
    tc.test_case_1_lines_to_dict()
    tc.test_case_2_get_dict_value_by_text_key()

    tc.tearDown()
