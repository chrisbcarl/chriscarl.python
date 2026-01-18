#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
Author:         Chris Carl
Email:          chrisbcarl@outlook.com
Date:           2024-11-26
Description:

chriscarl.core.functors.python unit test.

Updates:
    2024-11-26 - tests.chriscarl.core.functors.python - initial commit
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
import chriscarl.core.functors.python as lib

SCRIPT_RELPATH = 'tests/chriscarl/core/functors/test_python.py'
if not hasattr(sys, '_MEIPASS'):
    SCRIPT_FILEPATH = os.path.abspath(__file__)
else:
    SCRIPT_FILEPATH = os.path.abspath(os.path.join(sys._MEIPASS, SCRIPT_RELPATH))  # pylint: disable=no-member
SCRIPT_DIRPATH = os.path.dirname(SCRIPT_FILEPATH)
SCRIPT_NAME = os.path.splitext(os.path.basename(__file__))[0]
THIS_MODULE = sys.modules[__name__]
LOGGER = logging.getLogger(__name__)
LOGGER.addHandler(logging.NullHandler())


class A():
    a = 1
    val = 1

    def __str__(self):
        return 'A<[{}]({})>'.format(self.a, self.val)


class B():
    b = 2
    val = 2

    def __str__(self):
        return 'B<[{}]({})>'.format(self.b, self.val)


class C(A, B):
    c = 3

    def __init__(self, a2val=1, b2val=2):
        super().__init__()
        self.a2 = A()
        self.a2.val = a2val
        self.b2 = B()
        self.b2.val = b2val

    def __str__(self):
        return 'A<[{},{},{}]({})+{}+{}>'.format(self.c, self.b, self.c, self.val, self.a2, self.b2)


class TestCase(UnitTest):

    def setUp(self):
        self.a = A()
        self.b = B()
        self.c = C()
        self.c1 = C()
        self.c2 = C(b2val=3)
        return super().setUp()

    def tearDown(self):
        return super().tearDown()

    def test_case_0_get_func_name(self):
        variables = [
            (lib.get_func_name, self.test_case_0_get_func_name),
        ]
        controls = [
            'test_case_0_get_func_name',
        ]
        self.assert_null_hypothesis(variables, controls)

    def test_case_1_invocation_string(self):

        def shit(a, *b, c=1, **d):
            pass

        variables = [
            (lib.invocation_string, (shit, ), dict(args=(1, 2, 3), kwargs=dict(c=1, d=2, e=3))),
        ]
        controls = [
            'shit(1, 2, 3, c=1, d=2, e=3)',
        ]
        self.assert_null_hypothesis(variables, controls)

    def test_case_2_hasgetset(self):
        variables = [
            (lib.hasattr_cmp, ('whatever', 1)),
            (lib.getattr_cmp, ('whatever', 1)),
            (lib.setattr_deep, (self.a, 'whatever.__class__', 1)),
            (lib.hasattr_deep, (self.a, '__class__.__name__'), {}),
            (lib.hasattr_deep, (self.a, '__class__.__nope__'), {}),
            (lib.hasattr_cmp, ('val', self.a, self.b, self.c), {}),
            (lib.hasattr_cmp, ('a', self.a, self.b, self.c), {}),
            (lib.hasattr_cmp, ('d', self.a, self.b, self.c), {}),
            (lib.hasattr_cmp, ('b', self.a, self.b, self.c), {}),
            (lib.getattr_deep, (self.a, '__class__.__name__'), {}),
            (lib.getattr_deep, (self.a, '__class__.__nope__'), {}),
            (lib.getattr_cmp, ('a', self.c1, self.c2), {}),
            (lib.getattr_cmp, ('b2.val', self.c1, self.c2), {}),
            (lib.setattr_deep, (self, 'c1.a2.a', 4), {}),
            (lib.getattr_deep, (self, 'c1.a2.a'), {}),
            (lib.getattr_deep, (self, 'a.b.c.d.e', 'weird default 3rd argument'), {}),
        ]
        controls = [
            ValueError,
            ValueError,
            AttributeError,
            True,
            False,
            (True, True),  # a has "val", [b, c] does all have "val"
            (True, False),  # a has "a", [b, c] does not all have "a"
            (False, True),  # a does not have "d", [b, c] does not all have "d"
            (False, False),  # a does not have "b", [b, c] does all have "b"
            'A',
            AttributeError,
            True,
            False,
            None,
            4,
            'weird default 3rd argument'
        ]
        self.assert_null_hypothesis(variables, controls)

    def test_case_3_is_legal_python_name(self):
        variables = [
            (lib.is_legal_python_name, 'aa'),
            (lib.is_legal_python_name, 'a1'),
            (lib.is_legal_python_name, 'a_'),
            (lib.is_legal_python_name, '_a'),
            (lib.is_legal_python_name, '1a'),
            (lib.is_legal_python_name, ' '),
            (lib.is_legal_python_name, '-'),
            (lib.is_legal_python_name, '%'),
        ]
        controls = [
            True,
            True,
            True,
            True,
            False,
            False,
            False,
            False,
        ]
        self.assert_null_hypothesis(variables, controls)

    def test_case_4_get_legal_python_name(self):
        variables = [
            (lib.get_legal_python_name, 'aa'),
            (lib.get_legal_python_name, 'a1'),
            (lib.get_legal_python_name, 'a_'),
            (lib.get_legal_python_name, '1a'),
            (lib.get_legal_python_name, '_a'),
            (lib.get_legal_python_name, ' '),
            (lib.get_legal_python_name, '-'),
            (lib.get_legal_python_name, '%'),
        ]
        controls = [
            'aa',
            'a1',
            'a_',
            '_1a',
            '_a',
            '_',
            '_',
            '_',
        ]
        self.assert_null_hypothesis(variables, controls)

    def test_case_5_conform_func_args_kwargs(self):
        variables = [
            (lib.conform_func_args_kwargs, [(print)]),
            (lib.conform_func_args_kwargs, [(print, 'me')]),
            (lib.conform_func_args_kwargs, [(print, 'me', {
                'file': sys.stdout
            })]),
        ]
        controls = [
            [(print, (), {})],
            [(print, ('me', ), {})],
            [(print, ('me', ), {
                'file': sys.stdout
            })],
        ]
        self.assert_null_hypothesis(variables, controls)

    def test_case_6_run_func_args_kwargs(self):
        variables = [
            (lib.run_func_args_kwargs, [(print)]),
            (lib.run_func_args_kwargs, [(print, 'me')]),
            (lib.run_func_args_kwargs, [(print, 'me', {
                'file': sys.stdout
            })]),
        ]
        controls = [
            [None],
            [None],
            [None],
        ]
        self.assert_null_hypothesis(variables, controls)

    def test_case_7_ModuleDocumentation(self):
        md = lib.ModuleDocumentation.parse(lib.__doc__)
        self.assertEqual(md.to_string(), lib.__doc__, 'ModuleDocumentation class parse -> to_string not 1:1!')

    def test_case_8_abbreviate_arg(self):
        variables = [
            (lib.abbreviate_arg, ('abcdefghijklmnop', ), dict(chars=3)),
            (lib.abbreviate_arg, ('abcdefghijklmnop', ), dict(chars=6)),
            (lib.abbreviate_arg, ('abcdefghijklmnop', ), dict(chars=8)),
        ]
        controls = [
            "'...'",
            "'abc...'",
            "'abcde...'",
        ]
        self.assert_null_hypothesis(variables, controls)


if __name__ == '__main__':
    tc = TestCase()
    tc.setUp()

    tc.test_case_0_get_func_name()
    tc.test_case_1_invocation_string()
    tc.test_case_2_hasgetset()
    tc.test_case_3_is_legal_python_name()
    tc.test_case_4_get_legal_python_name()
    tc.test_case_5_conform_func_args_kwargs()
    tc.test_case_6_run_func_args_kwargs()
    tc.test_case_7_ModuleDocumentation()
    tc.test_case_8_abbreviate_arg()

    tc.tearDown()
