#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
Author:         Chris Carl
Email:          chrisbcarl@outlook.com
Date:           2024-12-29
Description:

chriscarl.core.lib.stdlib.fnmatch unit test.

Updates:
    2024-12-29 - tests.chriscarl.core.lib.stdlib.fnmatch - initial commit
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
from chriscarl.core.lib.stdlib.os import abspath, walk
from chriscarl.core.lib.stdlib.unittest import UnitTest
from chriscarl.core.lib.stdlib.io import write_text_file

# test imports
import chriscarl.core.lib.stdlib.fnmatch as lib

SCRIPT_RELPATH = 'tests/chriscarl/core/lib/stdlib/test_fnmatch.py'
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
        ret = super().setUp()
        self.gitignore = abspath(self.tempdir, '.gitignore')
        write_text_file(self.gitignore, '**\n__pycache__/')
        return ret

    def tearDown(self):
        return super().tearDown()

    def test_case_0_argument_to_fnmatchs(self):
        variables = [
            (lib.argument_to_fnmatchs, []),
            (lib.argument_to_fnmatchs, '**'),
            (lib.argument_to_fnmatchs, '**\n__pycache__/'),
            (lib.argument_to_fnmatchs, self.gitignore),
        ]
        controls = [
            [],
            ['**'],
            ['**', '__pycache__/'],
            ['**', '__pycache__/'],
        ]
        self.assert_null_hypothesis(variables, controls)

    def test_case_1_walk_equivalent(self):
        only_pys = list(walk(SCRIPT_DIRPATH, extensions=['.py']))
        only_pycs = list(walk(SCRIPT_DIRPATH, extensions=['.pyc']))
        everything_bname = list(walk(SCRIPT_DIRPATH, basename=True))
        everything_rel = list(walk(SCRIPT_DIRPATH, relpath=True))
        variables = [
            (lib.walk, (SCRIPT_DIRPATH, ), dict(include='*.py')),
            (lib.walk, (SCRIPT_DIRPATH, ), dict(exclude='*.py')),
            (lib.walk, (SCRIPT_DIRPATH, ), dict(include='*.pyc')),
            (lib.walk, (SCRIPT_DIRPATH, ), dict(exclude='*.pyc')),
            (lib.walk, (SCRIPT_DIRPATH, ), dict(basename=True)),
            (lib.walk, (SCRIPT_DIRPATH, ), dict(relpath=True)),
        ]
        controls = [
            only_pys,
            only_pycs,
            only_pycs,
            only_pys,
            everything_bname,
            everything_rel,
        ]
        self.assert_null_hypothesis(variables, controls)


if __name__ == '__main__':
    tc = TestCase()
    tc.setUp()

    tc.test_case_0_argument_to_fnmatchs()
    tc.test_case_1_walk_equivalent()

    tc.tearDown()
