#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
Author:         Chris Carl
Email:          chrisbcarl@outlook.com
Date:           2026-02-15
Description:

chriscarl.core.data_structures.tree unit test.

Updates:
    2026-02-15 - tests.chriscarl.core.data_structures.tree - initial commit
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
import chriscarl.core.data_structures.tree as lib

SCRIPT_RELPATH = 'tests/core/data_structures/test_tree.py'
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
        one = lib.TreeNode(69)

        tree = lib.TreeNode(50)
        left = tree.add_left(25)
        right = tree.add_right(75)
        left_left = left.add_left(10)
        left_right = left.add_right(35)
        left_left.add_left(5)
        left_left.add_right(15)

        variables = [
            (lib.height, one),
            (lib.height, tree),
            (lib.count, one),
            (lib.count, tree),
            (tree.__eq__, 50),
            (tree.right.__eq__, 75),
            (tree.right.__eq__, right),
            (tree.left.__eq__, 25),
            (tree.left.right.__eq__, 35),
            (tree.left.right.__eq__, left_right),
            (lib.to_str, tree),
            (lib.inorder, tree),
            (lib.preorder, tree),
            (lib.postorder, tree),
            (lib.levelorder, tree),
        ]
        controls = [
            0,  # leaves do not count, so a 1-node tree has height 0
            3,
            1,
            7,
            True,
            True,
            True,
            True,
            True,
            True,
            '''
              50
      25              75
  10      35      -       -
5   15  -   -   -   -   -   -'''[1:],  # string display correct, skip newline in test
            [5, 10, 15, 25, 35, 50, 75],  # inorder
            [50, 25, 10, 5, 15, 35, 75],  # preorder
            [5, 15, 10, 35, 25, 75, 50],  # postorder
            [50, 25, 75, 10, 35, 5, 15],  # levelorder
        ]
        self.assert_null_hypothesis(variables, controls)


if __name__ == '__main__':
    tc = TestCase()
    tc.setUp()

    try:
        tc.test_case_0()
    finally:
        tc.tearDown()
