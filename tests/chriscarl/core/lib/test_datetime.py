#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
Author:         Chris Carl
Email:          chrisbcarl@outlook.com
Date:           2026-02-20
Description:

chriscarl.core.lib.stdlib.datetime unit test.

Updates:
    2026-02-20 - tests.chriscarl.core.lib.stdlib.datetime - initial commit
'''

# stdlib imports (expected to work)
from __future__ import absolute_import, print_function, division, with_statement  # , unicode_literals
import os
import sys
import logging
import unittest
import datetime

# third party imports

# project imports (expected to work)
from chriscarl.core import constants
from chriscarl.core.lib.stdlib.os import abspath
from chriscarl.core.lib.stdlib.unittest import UnitTest

# test imports
import chriscarl.core.lib.stdlib.datetime as lib

SCRIPT_RELPATH = 'tests/chriscarl/core/lib/test_datetime.py'
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
        known = datetime.datetime(year=2026, month=2, day=20)
        known_week = datetime.datetime(year=2026, month=2, day=16)
        variables = [
            (lib.get_start_of_week, known),
            (lib.get_start_of_day, known),
            (lib.get_end_of_day, known),
        ]
        controls = [
            known_week,
            known,
            known - datetime.timedelta(microseconds=1) + datetime.timedelta(days=1),
        ]
        self.assert_null_hypothesis(variables, controls)

    def test_case_1(self):
        known0 = datetime.datetime(year=2026, month=2, day=20)
        known1 = datetime.datetime(year=2026, month=2, day=20, hour=6)
        known2 = datetime.datetime(year=2026, month=2, day=20, hour=6, microsecond=9)
        known3 = datetime.datetime(year=2026, month=2, day=20, hour=6, microsecond=9, tzinfo=datetime.timezone.utc)
        variables = [
            (lib.from_str, 'nothing'),
            (lib.from_str, '2026-02-20'),
            (lib.from_str, '2026-02-20 6:00'),
            (lib.from_str, '2026-02-20 06:00'),
            (lib.from_str, '2026-02-20 06:00:00.000009'),
            # TODO:
            # (lib.from_str, '2026-02-20T6:00:00.000009'),
            # (lib.from_str, '2026-02-20T6:00:00.000009 +0000'),
        ]
        controls = [
            None,
            known0,
            known1,
            known1,
            known2,
            # known3,
            # known3,
        ]
        self.assert_null_hypothesis(variables, controls)


if __name__ == '__main__':
    tc = TestCase()
    tc.setUp()

    try:
        tc.test_case_0()
        tc.test_case_1()
    finally:
        tc.tearDown()
