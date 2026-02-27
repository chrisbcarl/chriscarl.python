#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
Author:         Chris Carl
Email:          chrisbcarl@outlook.com
Date:           2026-02-15
Description:

core.data_structures.doubly_linked_list is... TODO: lorem ipsum
core are modules that define the bedrock from which other things do import. non-self-referential, low-import, etc.

Updates:
    2026-02-15 - core.data_structures.doubly_linked_list - initial commit
'''

# stdlib imports
from __future__ import absolute_import, print_function, division, with_statement  # , unicode_literals
import os
import sys
import logging
from typing import Optional, Any, Generator, Tuple, List

# third party imports

# project imports
from chriscarl.core.data_structures.node import Node
from chriscarl.core.data_structures.singly_linked_list import SllNode, SinglyLinkedList, count, to_list

SCRIPT_RELPATH = 'chriscarl/core/data_structures/doubly_linked_list.py'
if not hasattr(sys, '_MEIPASS'):
    SCRIPT_FILEPATH = os.path.abspath(__file__)
else:
    SCRIPT_FILEPATH = os.path.abspath(os.path.join(sys._MEIPASS, SCRIPT_RELPATH))  # pylint: disable=no-member
SCRIPT_DIRPATH = os.path.dirname(SCRIPT_FILEPATH)
SCRIPT_NAME = os.path.splitext(os.path.basename(__file__))[0]
THIS_MODULE = sys.modules[__name__]
LOGGER = logging.getLogger(__name__)
LOGGER.addHandler(logging.NullHandler())


class DllNode(SllNode):
    neighbors = []  # type: List[Optional[DllNode]]

    def __init__(self, data, next=None, prev=None):
        super().__init__(data, next=next)
        self.neighbors.append(prev)

    @property
    def prev(self):
        # type: () -> Optional[Node]
        return self.neighbors[1]

    @prev.setter
    def prev(self, value):
        # type: (DllNode|Any) -> None
        self.neighbors[1] = self.new(value)


class DoublyLinkedList(SinglyLinkedList):
    head = DllNode(0)  # type: DllNode
    size = 0

    def __init__(self, node_or_data):
        if isinstance(node_or_data, DllNode):
            self.head = node_or_data
        else:
            self.head = DllNode(node_or_data)
        self.size = count(self.head)

    def to_list(self):
        # type: () -> List[Any]
        return to_list(self.head)

    @classmethod
    def from_list(cls, lst):
        # type: (List[Any]) -> SinglyLinkedList
        head = from_list(lst)
        return SinglyLinkedList(head)

    def append_tail(self, value):
        # type: (SllNode|Any) -> None
        append(self.head, value)
        self.size = count(self.head)


def from_list(lst):
    # type: (List[Any]) -> Optional[SllNode]
    if not lst:
        return None
    ptr = head = SllNode(lst[0])
    for i in range(1, len(lst)):
        n = SllNode(lst[i])
        ptr.next = n
        ptr = n
    return head
