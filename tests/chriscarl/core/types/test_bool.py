#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
Author:         Chris Carl
Email:          chrisbcarl@outlook.com
Date:           2026-02-20
Description:

chriscarl.core.types.bool unit test.

Updates:
    2026-02-20 - tests.chriscarl.core.types.bool - initial commit
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
import chriscarl.core.types.bool as lib

SCRIPT_RELPATH = 'tests/chriscarl/core/test_bool.py'
if not hasattr(sys, '_MEIPASS'):
    SCRIPT_FILEPATH = os.path.abspath(__file__)
else:
    SCRIPT_FILEPATH = os.path.abspath(os.path.join(sys._MEIPASS, SCRIPT_RELPATH))  # pylint: disable=no-member
SCRIPT_DIRPATH = os.path.dirname(SCRIPT_FILEPATH)
SCRIPT_NAME = os.path.splitext(os.path.basename(__file__))[0]
THIS_MODULE = sys.modules[__name__]
LOGGER = logging.getLogger(__name__)
LOGGER.addHandler(logging.NullHandler())

constants.fix_constants(lib)  # deal with namespace sharding the files across directories


class TestCase(UnitTest):

    def setUp(self):
        return super().setUp()

    def tearDown(self):
        return super().tearDown()

    # @unittest.skip('lorem ipsum')
    def test_case_0(self):
        variables = [
            (lib.boolean, 0),
            (lib.boolean, []),
            (lib.boolean, 'no'),
            (lib.boolean, 'n'),
            (lib.boolean, 1),
            (lib.boolean, [1]),
            (lib.boolean, 'yes'),
            (lib.boolean, 'y'),
        ]
        controls = [
            False,
            False,
            False,
            False,
            True,
            True,
            True,
            True,
        ]
        self.assert_null_hypothesis(variables, controls)


if __name__ == '__main__':
    tc = TestCase()
    tc.setUp()

    try:
        tc.test_case_0()
    finally:
        tc.tearDown()
