#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
Author:         Chris Carl
Email:          chrisbcarl@outlook.com
Date:           2024-12-04
Description:

chriscarl.core.types.version unit test.

Updates:
    2024-12-04 - tests.chriscarl.core.types.version - initial commit
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
import chriscarl.core.types.version as lib

SCRIPT_RELPATH = 'tests/chriscarl/core/types/test_version.py'
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

    def test_case_0_version_parse(self):
        variables = [
            (lib.Version.parse, '1.2.NOPE'),
            (lib.Version.parse, '1.-2.-3-alpha'),
        ]
        controls = [
            ValueError,
            ValueError,
        ]
        self.assert_null_hypothesis(variables, controls)

    def test_case_1_cmp(self):
        variables = [
            (lib.Version.__eq__, (lib.Version.parse('0.0.0'), '0.0.0')),
            (lib.Version.__ne__, (lib.Version.parse('0.0.0'), '0.0.1')),
            (lib.Version.__lt__, (lib.Version.parse('1.0.0'), '1.0.1')),
            (lib.Version.__lt__, (lib.Version.parse('1.0.0'), '1.1.0')),
            (lib.Version.__eq__, (lib.Version.parse('1.0.1'), '1.0.1')),
            (lib.Version.__ge__, (lib.Version.parse('1.0.1'), '1.0.1')),
            # label (labels are greater than the base version)
            (lib.Version.__gt__, (lib.Version.parse('1.0.0-beta'), '1.0.0-alpha')),
            (lib.Version.__gt__, (lib.Version.parse('3.0.25-beta'), '3.0.25-alpha')),
            (lib.Version.__eq__, (lib.Version.parse('0.0.0-label'), '0.0.0-label')),
            (lib.Version.__lt__, (lib.Version.parse('0.5.9-rc69'), '0.5.9')),
            # prerelease (prerelease are less than the base version)
            (lib.Version.__eq__, (lib.Version.parse('0.0.0a1'), '0.0.0a1')),
            (lib.Version.__le__, (lib.Version.parse('0.0.0a1'), '0.0.0b1')),
            (lib.Version.__ge__, (lib.Version.parse('0.0.0a6'), '0.0.0a1')),
            (lib.Version.__gt__, (lib.Version.parse('1.0.0'), '1.0.0a1')),
        ]
        controls = [True for _ in variables]
        self.assert_null_hypothesis(variables, controls)

    def test_case_2_update(self):
        variables = [
            (lib.Version.__eq__, (lib.Version.parse('1.0.1').update('major', 1), '2.0.0')),
            (lib.Version.__eq__, (lib.Version.parse('1.0.1').update('minor', 1), '1.1.0')),
            (lib.Version.__eq__, (lib.Version.parse('1.0.1').update('patch', 1), '1.0.2')),
            # label (labels are greater than the base version)
            (lib.Version.__eq__, (lib.Version.parse('0.5.9-rc69').update('label', None), '0.5.9')),
            # prerelease (prerelease are less than the base version)
            (lib.Version.__eq__, (lib.Version.parse('1.0.1').update('prerelease', 'a2'), '1.0.1a2')),
            (lib.Version.__ne__, (lib.Version.parse('1.0.1').update('prerelease', 'a6'), '1.0.1a2')),
            (lib.Version.__eq__, (lib.Version.parse('1.0.1a2').update('prerelease', None), '1.0.1')),
        ]
        controls = [True for _ in variables]
        self.assert_null_hypothesis(variables, controls)


if __name__ == '__main__':
    tc = TestCase()
    tc.setUp()

    tc.test_case_0_version_parse()
    tc.test_case_1_cmp()
    tc.test_case_2_update()

    tc.tearDown()
