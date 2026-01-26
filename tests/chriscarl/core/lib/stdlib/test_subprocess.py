#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
Author:         Chris Carl
Email:          chrisbcarl@outlook.com
Date:           2024-11-25
Description:

chriscarl.core.lib.stdlib.subprocess unit test.

Updates:
    2024-11-25 - tests.chriscarl.core.lib.stdlib.subprocess - initial commit
'''

# stdlib imports (expected to work)
from __future__ import absolute_import, print_function, division, with_statement  # , unicode_literals
import os
import sys
import logging
import unittest
import subprocess

# third party imports

# project imports (expected to work)
from chriscarl.core.lib.stdlib.unittest import UnitTest

# test imports
import chriscarl.core.lib.stdlib.subprocess as lib

SCRIPT_RELPATH = 'tests/chriscarl/core/lib/stdlib/test_subprocess.py'
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

    def test_case_0_run(self):
        variables = [
            (lib.run, 'echo hello world'),
            (lib.run, ['echo', 'hello', 'world']),
        ]
        controls = [
            (0, 'hello world\n'),
            (0, 'hello world\n'),
        ]
        self.assert_null_hypothesis(variables, controls)

    def test_case_1_launch_filepath(self):
        lib.launch_editor(__file__)

    def test_case_2_kill(self):
        popen = subprocess.Popen([sys.executable])
        variables = [
            (lib.kill, (popen.pid, )),
        ]
        controls = [
            0,
        ]
        self.assert_null_hypothesis(variables, controls)

    def test_case_3(self):
        variables = [
            (lib.which, ('python', )),
        ]
        controls = [
            sys.executable,
        ]
        self.assert_null_hypothesis(variables, controls)


if __name__ == '__main__':
    tc = TestCase()
    tc.setUp()

    tc.test_case_0_run()
    tc.test_case_1_launch_filepath()
    tc.test_case_2_kill()
    tc.test_case_3()

    tc.tearDown()
