#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
Author:         Chris Carl
Email:          chrisbcarl@outlook.com
Date:           2026-02-15
Description:

chriscarl.core.data_structures.node unit test.

Updates:
    2026-02-15 - tests.chriscarl.core.data_structures.node - initial commit
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
import chriscarl.core.data_structures.node as lib

SCRIPT_RELPATH = 'tests/core/data_structures/test_node.py'
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
        n0 = lib.Node(0)
        n1 = lib.Node(1)
        n0.add_edge(n1)
        n0.add_edge(3)
        n0.add_edge(5)
        n2 = lib.Node(1)
        repr(n2)
        variables = [
            (lambda x, y: x == y, (n0, n0)),
            (lambda x, y: x == y, (n0, n1)),
            (lambda x, y: x < y, (n0, n0)),
            (lambda x, y: x < y, (n0, n1)),
            (str, n0),
            (repr, n0),
            (repr, n2),
            (n0.__eq__, 0),
            (n0.__ne__, "0"),
        ]
        controls = [
            True,
            False,
            False,
            True,
            'Node[0]',
            'Node[0, 3E]',
            'Node[1, 0E]',
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
