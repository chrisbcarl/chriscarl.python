#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
Author:         Chris Carl
Email:          chrisbcarl@outlook.com
Date:           2026-02-15
Description:

chriscarl.core.data_structures.singly_linked_list unit test.

Updates:
    2026-02-15 - tests.chriscarl.core.data_structures.singly_linked_list - initial commit
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
import chriscarl.core.data_structures.singly_linked_list as lib

SCRIPT_RELPATH = 'tests/chriscarl/core/test_singly_linked_list.py'
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
        lst = list(range(5))
        sll = lib.SinglyLinkedList.from_list(lst)
        sll2 = lib.SinglyLinkedList.from_list(lst)
        sll3 = lib.SinglyLinkedList(5)
        variables = [
            (sll.to_list),
            (str, sll),
            (lib.count, sll.head),
            (len, sll),
            (sll.__eq__, sll2),
            (sll.__ne__, sll3),
        ]
        controls = [
            lst,
            '0 -> 1 -> 2 -> 3 -> 4',
            5,
            5,
            True,
            True,
        ]
        self.assert_null_hypothesis(variables, controls)

    def test_case_1(self):
        sll = lib.SinglyLinkedList.from_list(list(range(3)))
        variables = [
            (sll.__str__, ()),
            (sll.insert, (-1, -1)),
            (sll.insert, (10, 10)),
            (sll.insert, (0, 999)),
            (sll.__str__, ()),
            (sll.insert, (4, 4)),
            (sll.__str__, ()),
            (sll.insert, (2, 222)),
            (sll.__str__, ()),
            # end of inserts
            (sll.emplace, (-1, -1)),
            (sll.emplace, (10, -1)),
            (sll.emplace, (0, -1)),
            (sll.__str__, ()),
            (sll.emplace, (5, 5)),
            (sll.__str__, ()),
            (sll.emplace, (2, 69)),
            (sll.__str__, ()),
        ]
        controls = [
            '0 -> 1 -> 2',
            IndexError,
            IndexError,
            Any,
            '999 -> 0 -> 1 -> 2',
            Any,
            '999 -> 0 -> 1 -> 2 -> 4',
            Any,
            '999 -> 0 -> 222 -> 1 -> 2 -> 4',
            # end of inserts
            IndexError,
            IndexError,
            Any,
            '-1 -> 0 -> 222 -> 1 -> 2 -> 4',
            Any,
            '-1 -> 0 -> 222 -> 1 -> 2 -> 5',
            Any,
            '-1 -> 0 -> 69 -> 1 -> 2 -> 5',
        ]
        self.assert_null_hypothesis(variables, controls)

    def test_case_2(self):
        sll = lib.SinglyLinkedList.from_list(list(range(4)))
        tail = sll.append(4)
        variables = [
            (getattr, (sll, 'tail')),
            (sll.__str__, ()),
            (sll.remove, (-1, )),
            (sll.remove, (0, )),
            (sll.__str__, ()),
            (sll.remove, (2, )),
            (sll.__str__, ()),
            (sll.remove, (3, )),
            (sll.remove, (2, )),
            (sll.__str__, ()),
        ]
        controls = [
            tail,
            '0 -> 1 -> 2 -> 3 -> 4',
            IndexError,
            Any,
            '1 -> 2 -> 3 -> 4',
            Any,
            '1 -> 2 -> 4',
            IndexError,
            Any,
            '1 -> 2',
        ]
        self.assert_null_hypothesis(variables, controls)


if __name__ == '__main__':
    tc = TestCase()
    tc.setUp()

    try:
        tc.test_case_0()
        tc.test_case_1()
        tc.test_case_2()
    finally:
        tc.tearDown()
