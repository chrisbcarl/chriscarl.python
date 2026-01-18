#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
Author:         Chris Carl
Email:          chrisbcarl@outlook.com
Date:           2024-11-26
Description:

chriscarl.core.lib.stdlib.inspect unit test.

Updates:
    2024-11-26 - tests.chriscarl.core.lib.stdlib.inspect - initial commit
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
import chriscarl.core.lib.stdlib.inspect as lib

SCRIPT_RELPATH = 'tests/chriscarl/core/lib/stdlib/test_inspect.py'
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

    def test_case_0_get_variable_names_linenos(self):
        a = 69
        plz_for_the_love_of_god = 1089
        variables = [
            (lib.get_variable_name_lineno, a),
            (lib.get_variable_name_lineno, 1089),
        ]
        controls = [
            ('a', 61),  # since the call occurs on 61
            ('plz_for_the_love_of_god', 61),  # since the call occurs on 61
        ]
        self.assert_null_hypothesis(variables, controls)

    def test_case_1_FunctionSpecification(self):
        variables = [
            (lib.FunctionSpecification.get, 1),
        ]
        controls = [
            ValueError,
        ]
        self.assert_null_hypothesis(variables, controls)

        def positional(a, b):
            pass

        def optional(c=True, d=False):
            pass

        def positional_varargs(a, b, *args):
            pass

        def optional_varkwargs(c=True, d=False, **kwargs):
            pass

        def varargs_varkwargs(*args, **kwargs):
            pass

        def positional_varargs_optional(a, b, *args, c=True, d=False):
            pass

        def positional_optional_kwargs(a, b, c=True, d=False, **kwargs):
            pass

        def positional_varargs_optional_varkwargs(a, b, *args, c=True, d=False, **kwargs):
            pass

        funcs = [
            positional,
            optional,
            positional_varargs,
            optional_varkwargs,
            varargs_varkwargs,
            positional_varargs_optional,
            positional_optional_kwargs,
            positional_varargs_optional_varkwargs,
        ]
        fses = [lib.FunctionSpecification.get(func) for func in funcs]

        variables = [fs.to_invocation_string for fs in fses]
        controls = [
            'positional(a, b)',
            'optional(c=True, d=False)',
            'positional_varargs(a, b, *args)',
            'optional_varkwargs(c=True, d=False, **kwargs)',
            'varargs_varkwargs(*args, **kwargs)',
            'positional_varargs_optional(a, b, *args, c=True, d=False)',
            'positional_optional_kwargs(a, b, c=True, d=False, **kwargs)',
            'positional_varargs_optional_varkwargs(a, b, *args, c=True, d=False, **kwargs)',
        ]
        self.assert_null_hypothesis(variables, controls)

        variables = [(str(fs).startswith, 'FunctionSpecification') for fs in fses]
        controls = [True for _ in variables]
        self.assert_null_hypothesis(variables, controls)

    def test_case_2_linenos(self):

        def run():
            return lib.get_caller_file_lineno()[1]

        self.assertEqual(lib.get_this_file_lineno()[1], 130)
        self.assertEqual(run(), 131)


if __name__ == '__main__':
    tc = TestCase()
    tc.setUp()

    tc.test_case_0_get_variable_names_linenos()
    tc.test_case_1_FunctionSpecification()
    tc.test_case_2_linenos()

    tc.tearDown()
