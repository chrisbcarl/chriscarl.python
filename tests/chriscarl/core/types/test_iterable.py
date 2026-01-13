#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
Author:         Chris Carl
Email:          chrisbcarl@outlook.com
Date:           2024-12-09
Description:

chriscarl.core.types.iterable unit test.

Updates:
    2024-12-09 - tests.chriscarl.core.types.iterable - initial commit
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
import chriscarl.core.types.iterable as lib

SCRIPT_RELPATH = 'tests/chriscarl/core/types/test_iterable.py'
if not hasattr(sys, '_MEIPASS'):
    SCRIPT_FILEPATH = os.path.abspath(__file__)
else:
    SCRIPT_FILEPATH = os.path.abspath(os.path.join(sys._MEIPASS, SCRIPT_RELPATH))  # pylint: disable=no-member
SCRIPT_DIRPATH = os.path.dirname(SCRIPT_FILEPATH)
SCRIPT_NAME = os.path.splitext(os.path.basename(__file__))[0]
THIS_MODULE = sys.modules[__name__]
LOGGER = logging.getLogger(__name__)
LOGGER.addHandler(logging.NullHandler())

NESTED_LIST = [
    0,
    [1, 2, 3],
    {4, 5, 6},
    {
        7: 8,
        9: 10
    },
]
NESTED_DICT = {
    0: 1,
    2: [3, 4, 5],
    6: {7, 8, 9},
    10: {
        11: 12,
        13: 14
    },
}
NESTED_NESTED_DICT = {
    'a': 'b',
    'c': {
        'd': 'e',
    },
    'f': {
        'g': {
            'h': 'i'
        },
    },
}


class TestCase(UnitTest):

    def setUp(self):
        self.num_list = [1, 2, 2, 3, 3, 3]
        self.num_dict = {k: k for k in range(1, 4)}
        return super().setUp()

    def tearDown(self):
        return super().tearDown()

    def test_case_0_get(self):
        variables = [
            (lib.get, (0, NESTED_LIST)),
            (lib.get, (1, NESTED_LIST)),
            (lib.get, ('1.0', NESTED_LIST)),
            (lib.get, ('3.7', NESTED_LIST)),
            (lib.get, ('f.g.h', NESTED_NESTED_DICT)),
            (lib.get, ('0', NESTED_DICT)),
            (lib.get, ('f.g.h.i', NESTED_NESTED_DICT)),
        ]
        controls = [
            NESTED_LIST[0],
            NESTED_LIST[1],
            NESTED_LIST[1][0],
            NESTED_LIST[3][7],
            NESTED_NESTED_DICT['f']['g']['h'],
            NESTED_DICT[0],
            KeyError,
        ]
        self.assert_null_hypothesis(variables, controls)

    def test_case_1_flatten_iterable(self):
        # yapf: disable
        dicks = [
            1,
            {'a': 0, 'b': [1, 2]},
            {'a': 0, 'b': {'c': 1}, 'd': []},
            {'a': [0, {'b': 1}, 2]},
            [0, 1, 2],
            [
                [0, 1, 2],
                [3, 4, 5],
                [6, 7, 8]
            ],
            # no prepend
        ]
        variables = [
            (lib.flatten_iterable, dicks[0]),
            (lib.flatten_iterable, dicks[1]),
            (lib.flatten_iterable, dicks[2]),
            (lib.flatten_iterable, dicks[3]),
            (lib.flatten_iterable, dicks[4]),
            (lib.flatten_iterable, dicks[5]),
            # prepend
            (lib.flatten_iterable, dicks[2], dict(prepend='d')),
            (lib.flatten_iterable, dicks[3], dict(prepend='d')),
        ]
        controls = [
            1,
            {'a': 0, 'b.0': 1, 'b.1': 2},
            {'a': 0, 'b.c': 1, 'd': []},
            {'a.0': 0, 'a.1.b': 1, 'a.2': 2},
            {'0': 0, '1': 1, '2': 2},
            {'0.0': 0, '0.1': 1, '0.2': 2, '1.0': 3, '1.1': 4, '1.2': 5, '2.0': 6, '2.1': 7, '2.2': 8},
            # prepend
            {'d.a': 0, 'd.b.c': 1, 'd.d': []},
            {'d.a.0': 0, 'd.a.1.b': 1, 'd.a.2': 2},
        ]
        self.assert_null_hypothesis(variables, controls)

        variables = [(lib.unflatten_iterable, controls[i]) for i in range(6)]
        controls = [dicks[i] for i in range(6)]
        self.assert_null_hypothesis(variables, controls)

    def test_case_2_keys_isleaf(self):
        lst = [0, 1]
        dct = {'a': 0, 'b': 1}
        variables = [
            (lib.keys, lst),
            (lib.keys, dct),
            (lib.keys, NESTED_DICT),
            (lib.keys, 1),
        ]
        controls = [
            ['0', '1'],
            ['a', 'b'],
            ['0', '2', '2.0', '2.1', '2.2', '6', '6.0', '6.1', '6.2', '10', '10.11', '10.13'],
            [],
        ]
        self.assert_null_hypothesis(variables, controls)

        for i, data in enumerate([lst, dct, NESTED_DICT]):
            keys = controls[i]
            flat = list(lib.flatten_iterable(data).values())
            got = list(lib.get(key, data) for key in keys)
            got = [ele for ele in got if lib.isleaf(ele)]
            self.assertEqual(got, flat, 'failed equality on data {}...'.format(i))

    def test_case_3_contains(self):
        variables = [
            (lib.contains, (self.num_list, None)),
            (lib.contains, (self.num_list, None), dict(exc=True)),
            (lib.contains, (self.num_list, 1)),
            (lib.contains, (self.num_list, 2)),
            (lib.contains, (self.num_list, 3)),
            (lib.contains_all, (self.num_list, [1, 2, 3])),
            (lib.contains_any, (self.num_dict, 1)),
            (lib.contains_any, (self.num_dict, 2)),
            (lib.contains_any, (self.num_dict, 3)),
            (lib.contains_all, (self.num_dict, [1, 2, 3])),
            (lib.contains_all, ('abcd', 'a')),
            (lib.contains_all, ('abcd', 'bc')),
            (lib.contains_all, ('abcd', ['b', 'c'])),
            (lib.contains, (self.num_list, [4]), dict(func=any)),
            (lib.contains, (self.num_dict, [4]), dict(func=any)),
            (lib.contains, ('abcd', [4]), dict(func=any)),
            (lib.contains_any, (self.num_list, [1, 2, 3, 4])),
            (lib.contains_any, (self.num_dict, [1, 2, 3, 4])),
            (lib.contains_any, ('abcd', ['b', 'c', 4])),
        ]
        controls = [
            False,
            ValueError,
            True,
            True,
            True,
            True,
            True,
            True,
            True,
            True,
            True,
            True,
            True,
            False,
            False,
            False,
            True,
            True,
            True,
        ]
        self.assert_null_hypothesis(variables, controls)

if __name__ == '__main__':
    tc = TestCase()
    tc.setUp()

    tc.test_case_0_get()
    tc.test_case_1_flatten_iterable()
    tc.test_case_2_keys_isleaf()
    tc.test_case_3_contains()

    tc.tearDown()
