#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
Author:         Chris Carl
Email:          chrisbcarl@outlook.com
Date:           2024-12-09
Description:

chriscarl.core.types.dict unit test.

Updates:
    2024-12-09 - tests.chriscarl.core.types.dict - initial commit
'''

# stdlib imports (expected to work)
from __future__ import absolute_import, print_function, division, with_statement  # , unicode_literals
import os
import sys
import logging
import unittest
import copy

# third party imports

# project imports (expected to work)
from chriscarl.core import constants
from chriscarl.core.lib.stdlib.os import abspath
from chriscarl.core.lib.stdlib.unittest import UnitTest

# test imports
import chriscarl.core.types.dict as lib

SCRIPT_RELPATH = 'tests/chriscarl/core/types/test_dict.py'
if not hasattr(sys, '_MEIPASS'):
    SCRIPT_FILEPATH = os.path.abspath(__file__)
else:
    SCRIPT_FILEPATH = os.path.abspath(os.path.join(sys._MEIPASS, SCRIPT_RELPATH))  # pylint: disable=no-member
SCRIPT_DIRPATH = os.path.dirname(SCRIPT_FILEPATH)
SCRIPT_NAME = os.path.splitext(os.path.basename(__file__))[0]
THIS_MODULE = sys.modules[__name__]
LOGGER = logging.getLogger(__name__)
LOGGER.addHandler(logging.NullHandler())

NESTED_EASY = dict(
    i=16,
    j=[
        '17',
        (
            dict(
                k=18,
                l=(),
                m=[],
                n=set([69, 70, 71]),
            ),
            None,
        ),
    ],
)
NESTED_EASY_EXPECTED_KEYS = [
    'i',
    'j',
    'j.0',
    'j.1',
    'j.1.0',
    'j.1.0.k',
    'j.1.0.l',
    'j.1.0.m',
    'j.1.0.n',
    'j.1.0.n.0',
    'j.1.0.n.1',
    'j.1.0.n.2',
    'j.1.1',
]
NESTED_HARD = dict(
    a=1,
    b=[
        '2',
        (
            3,
            set([
                '4',
                5,
                '6',
            ]),
        ),
    ],
    c=dict(
        d=8,
        e=[
            '9',
            (dict(
                f=10,
                g=[
                    '11',
                    (
                        12,
                        set([
                            '13',
                            14,
                            False,
                            '15',
                        ]),
                    ),
                ],
                h=copy.deepcopy(NESTED_EASY),
            ), ),
        ],
    ),
    d={},
)


class TestCase(UnitTest):

    def setUp(self):
        return super().setUp()

    def tearDown(self):
        return super().tearDown()

    @unittest.skip('lorem ipsum')
    def test_case_0(self):
        variables = [
            (sum, [0, 1, 2, 3]),
            (sum, [0, 1, 2, 3]),
        ]
        controls = [
            6,
            6,
        ]
        self.assert_null_hypothesis(variables, controls)

    def shit_test_walk(self):
        # dict-walk tests
        d = {'a': [0, {'b': 1}, 2]}
        expected_keys = ['a', 'a.0', 'a.1', 'a.1.b', 'a.2']
        assert dict_walk(d) == expected_keys, 'dict_walk documentation wrong'

        got_keys = dict_walk(NESTED_EASY)
        assert set(NESTED_EASY_EXPECTED_KEYS) == set(got_keys), 'dict_walk failed'

        # dict-access tests returns one thing
        assert dict_access('2', [0, 1, 2, 3]) == 2, 'dict_access failed for arrays'
        assert dict_access('j.1.0.k', NESTED_EASY) == NESTED_EASY['j'][1][0]['k'], 'dict_access for dicts'

        # dict-access glob tests returns dict of things
        d = [[0, 1, 2], [3, 4, 5], [6, 7, 8]]
        vs = dict_access('*.2', d)
        # LOGGER.debug(vs)
        assert len(vs) == 3, 'dict_access failed for glob doc example'
        assert dict(vs) == {'0.2': 2, '1.2': 5, '2.2': 8}, 'dict_access failed for glob doc example'

        # glob-like tests
        sub_expected_keys = [
            'j.1.0',
            'j.1.0.k',
            'j.1.0.l',
            'j.1.0.m',
            'j.1.0.n',
            'j.1.0.n.0',
            'j.1.0.n.1',
            'j.1.0.n.2',
            'j.1.1',
        ]
        got_keys = dict_glob_key_to_keys('j.1.*', NESTED_EASY)
        assert set(got_keys) == set(sub_expected_keys), 'glob doesnt return what is expected'


if __name__ == '__main__':
    tc = TestCase()
    tc.setUp()

    tc.test_case_0()

    tc.tearDown()
