#!/usr/bin/env python
# -*- coding: utf-8 -*-
r'''
Author:         Chris Carl
Email:          chrisbcarl@outlook.com
Date:           2026-04-13
Description:

chriscarl.core.operating_systems.concurrency unit test.

pytest --cov=chriscarl.core.operating_systems.concurrency tests/chriscarl/core/operating_systems/test_concurrency.py --cov-report term-missing

Updates:
    2026-04-13 - tests.chriscarl.core.operating_systems.concurrency - initial commit
'''

# stdlib imports (expected to work)
from __future__ import absolute_import, print_function, division, with_statement  # , unicode_literals
import os
import sys
import logging
import unittest
from typing import Any
import multiprocessing
import time

# third party imports

# project imports (expected to work)
from chriscarl.core import constants
from chriscarl.core.lib.stdlib.os import abspath
from chriscarl.core.lib.stdlib.unittest import UnitTest

# test imports
import chriscarl.core.operating_systems.concurrency as lib

SCRIPT_RELPATH = 'tests/chriscarl/core/operating_systems/test_concurrency.py'
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
        proc = multiprocessing.Process(target=lib.peterson)
        proc.start()
        time.sleep(0.3)
        proc.kill()
        # variables = [
        #     (sum, [0, 1, 2, 3]),
        #     (sum, [0, 1, 2, 3]),
        #     (print, "dont care"),
        # ]
        # controls = [
        #     6,
        #     6,
        #     Any,
        # ]
        # self.assert_null_hypothesis(variables, controls)


if __name__ == '__main__':
    tc = TestCase()
    tc.setUp()

    try:
        tc.test_case_0()
    finally:
        tc.tearDown()
