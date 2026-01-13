#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
Author:         Chris Carl
Email:          chrisbcarl@outlook.com
Date:           2024-12-09
Description:

chriscarl.core.lib.stdlib.ast unit test.

Updates:
    2024-12-09 - tests.chriscarl.core.lib.stdlib.ast - initial commit
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
import chriscarl.core.lib.stdlib.ast as lib

SCRIPT_RELPATH = 'tests/chriscarl/core/lib/stdlib/test_ast.py'
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

    def test_case_0_get_function_graph(self):
        code = '''class A:
    def B(self):
        def C(self):
            pass
        pass
def D():
    pass
        '''
        variables = [
            (lib.get_function_graph, code),
            (lib.get_function_graph, 1),
        ]
        controls = [
            {
                'A': {
                    'B': {
                        'C': {}
                    },
                },
                'D': {}
            },
            TypeError,
        ]
        self.assert_null_hypothesis(variables, controls)

    def test_case_1_visit(self):
        variables = [
            (lib.merge_python, ('a = 1', 'b =2')),
            (lib.merge_python, ('def puff(): puff()', 'def pass_(): bitch()')),
            (lib.merge_python, ('class A():\n  def B(): pass', 'class A():\n  def C(): pass')),
        ]
        ab = 'a = 1\nb = 2'
        puff_puff_pass_bitch = 'def puff():\n    puff()\n\ndef pass_():\n    bitch()'
        class_ab = 'class A:\n\n    def B():\n        pass\n\n    def C():\n        pass'
        controls = [
            ab,
            puff_puff_pass_bitch,
            class_ab,
        ]
        python_l = '''__all__ = ['CONST_1', 'A', 'C']
CONST_1 = 1
class A:
    def B(self):
        pass
def C():
    pass
'''
        python_r = '''class A:
    def D(self):
        pass
def E():
    pass
CONST_2 = 2
'''
        # unparsing tends to insert more lines in weird spots, whatever.
        python_m = '''__all__ = ['CONST_1', 'A', 'C', 'E', 'CONST_2']
CONST_1 = 1

class A:

    def B(self):
        pass

    def D(self):
        pass

def C():
    pass

def E():
    pass
CONST_2 = 2'''
        variables += [
            (lib.merge_python, (python_l, python_r)),
        ]
        controls += [
            python_m,
        ]
        self.assert_null_hypothesis(variables, controls)

        variables = [
            (lib.get__all__, ab),
            (lib.get__all__, puff_puff_pass_bitch),
            (lib.get__all__, class_ab),
        ]
        controls = [
            ['a', 'b'],
            ['puff', 'pass_'],
            ['A'],
        ]
        self.assert_null_hypothesis(variables, controls)

    def test_case_2_diff_python_strings(self):
        old = '''class A():
    def b():
        pass

def c():
    pass'''
        new = '''XYZ = 0

class A():
        def b():
            # comment
            1+1
        def d():
            pass

def e():
    pass'''
        variables = [
            (lib.diff_python_strings, (old, new)),
        ]
        controls = [
            (['A.d', 'e'], ['c'], ['A.b']),  # added, removed, changed
        ]
        self.assert_null_hypothesis(variables, controls)

    def test_case_3_is_python(self):
        variables = [
            (lib.is_python, ('')),
            (lib.is_python, ('A')),  # A could be some constant
            (lib.is_python, ('1')),
            (lib.is_python, ('A = 1')),
            (lib.is_python, ('A is 1')),
            (lib.is_python, ('A is one')),  # syntactically fine because one COULD be a container
            (lib.is_python, ('A is one hell of a tricky bastard')),  # aint no way
        ]
        controls = [
            True,
            True,
            True,
            True,
            True,
            True,
            False,
        ]
        self.assert_null_hypothesis(variables, controls)


if __name__ == '__main__':
    tc = TestCase()
    tc.setUp()

    tc.test_case_0_get_function_graph()
    tc.test_case_1_visit()
    tc.test_case_2_diff_python_strings()
    tc.test_case_3_is_python()

    tc.tearDown()
