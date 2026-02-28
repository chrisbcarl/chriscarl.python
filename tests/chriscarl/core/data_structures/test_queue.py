#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
Author:         Chris Carl
Email:          chrisbcarl@outlook.com
Date:           2026-02-27
Description:

chriscarl.core.data_structures.queue unit test.

Updates:
    2026-02-27 - tests.chriscarl.core.data_structures.queue - initial commit
'''

# stdlib imports (expected to work)
from __future__ import absolute_import, print_function, division, with_statement  # , unicode_literals
import os
import sys
import logging
import unittest
from typing import Any

# third party imports

# project imports (expected to work)
from chriscarl.core import constants
from chriscarl.core.lib.stdlib.os import abspath
from chriscarl.core.lib.stdlib.unittest import UnitTest

# test imports
import chriscarl.core.data_structures.queue as lib

SCRIPT_RELPATH = 'tests/chriscarl/core/data_structures/test_queue.py'
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
        super().setUp()
        # do other set ups (set up super first)

    def tearDown(self):
        # do other tear downs (tear down super after)
        super().tearDown()

    # @unittest.skip('lorem ipsum')
    def test_case_0(self):
        q = lib.Queue(range(3))
        f = lib.FIFO()
        variables = [
            (q.__eq__, [0, 1, 2]),
            (q.push, 3),
            (q.__eq__, [0, 1, 2, 3]),
            (q.pop, ()),
            (f.push, (0)),
            (f.push, (1)),
            (f.push, (2)),
            (f.pop, ()),
            (f.pop, ()),
            (f.pop, ()),
        ]
        controls = [
            True,
            Any,
            True,
            0,  # 0 inserted "first", so first out
            Any,
            Any,
            Any,
            0,  # 0 was inserted "first", so first out
            1,
            2,
        ]
        self.assert_null_hypothesis(variables, controls)


if __name__ == '__main__':
    tc = TestCase()
    tc.setUp()

    try:
        tc.test_case_0()
    finally:
        tc.tearDown()
