#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
Author:         Chris Carl
Email:          chrisbcarl@outlook.com
Date:           2026-02-15
Description:

core.data_structures.doubly_linked_list is a somewhat overkill class that gets the singly linked list accomplished.
core are modules that define the bedrock from which other things do import. non-self-referential, low-import, etc.

Updates:
    2026-02-26 - core.data_structures.doubly_linked_list - decent bit of code reuse from singly linked list, test is an exact ripoff of SLL
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
from chriscarl.core.data_structures.singly_linked_list import SllNode, SinglyLinkedList, count, to_list, index_and_prev, index

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

    def __init__(self, data, next=None, prev=None):
        super().__init__(data, next=next)
        self.neighbors.append(prev)

    @property
    def prev(self):
        # type: () -> Optional[DllNode]
        return self.neighbors[1]

    @prev.setter
    def prev(self, value):
        # type: (DllNode|Any) -> None
        if value is not None:
            self.neighbors[1] = value if isinstance(value, DllNode) else DllNode(value)
        else:
            self.neighbors[1] = None


class DoublyLinkedList(SinglyLinkedList):
    head = DllNode(0)  # type: DllNode
    size = 0

    def __init__(self, node_or_data):
        if isinstance(node_or_data, DllNode):
            self.head = node_or_data
        else:
            self.head = DllNode(node_or_data)
        self.size = count(self.head)

    def __str__(self):
        return to_str(self.head)

    def at(self, idx):
        # type: (int) -> Any
        return index(self.head, idx)

    def __getitem__(self, key):
        # type: (int) -> Any
        return self.at(key)

    def to_list(self):
        # type: () -> List[Any]
        return to_list(self.head)

    @classmethod
    def from_list(cls, lst):
        # type: (List[Any]) -> DoublyLinkedList
        head = from_list(lst)
        return DoublyLinkedList(head)

    def append(self, value):
        # type: (DllNode|Any) -> DllNode
        new = append(self.head, value)
        self.size = count(self.head)
        return new

    def insert(self, idx, value):
        # type: (int, Any) -> DllNode
        new = insert(self.head, idx, value)
        if idx == 0:
            self.head = new
        self.size = count(self.head)
        return new

    def emplace(self, idx, value):
        # type: (int, Any) -> DllNode
        new = emplace(self.head, idx, value)
        if idx == 0:
            self.head = new
        return new

    def remove(self, idx):
        # type: (int) -> None
        remove(self.head, idx)
        if idx == 0:
            self.head = self.head.next
        self.size = count(self.head)

    @property
    def tail(self):
        # type: () -> DllNode
        return tail(self.head)


def from_list(lst):
    # type: (List[Any]) -> Optional[DllNode]
    if not lst:
        return None
    prev = None
    ptr = head = DllNode(lst[0])
    for i in range(1, len(lst)):
        n = DllNode(lst[i])
        ptr.next = n
        ptr.prev = prev
        prev = ptr
        ptr = n
    return head


def append(head, value):
    # type: (DllNode, DllNode|Any) -> DllNode
    new = value if isinstance(value, DllNode) else DllNode(value)
    ptr = head
    while ptr.next:
        ptr = ptr.next
    ptr.next = new
    new.prev = ptr
    return new


def to_str(head):
    # type: (Optional[DllNode]) -> str
    if not head:
        return ''
    tokens = to_list(head)
    return ' <-> '.join(str(token) for token in tokens)


def emplace(head, idx, value):
    # type: (DllNode|None, int, Any) -> DllNode
    head, prev = index_and_prev(head, idx)

    # head is at index, 3 cases:
    new = DllNode(value)
    if not head:  # we're at the end of the list, so this is just append
        prev.next = new
        new.prev = prev
    else:
        if prev is None:  # beginning of list
            new.next = head.next  # old head still attached
        else:  # middle of the list
            new.next = head.next  # old middle still attached
            prev.next = new
            new.prev = prev
    return new


def insert(head, idx, value):
    # type: (DllNode|None, int, Any) -> DllNode
    '''4, 5, 6 insert(4, 1, 1) -> 4156 insert: "insert at"'''
    head, prev = index_and_prev(head, idx)

    # head is at index, 3 cases:
    new = DllNode(value)
    if head is None:  # we're at the end of the list, so this is just append
        prev.next = new
        new.prev = prev
    else:
        if prev is None:  # beginning of list
            new.next = head
        else:  # middle of the list
            prev.next = new
            new.next = head
            new.prev = prev
    return new


def remove(head, idx):
    # type: (DllNode|None, int) -> DllNode
    '''0,1,2.remove(1) = 0,2
    NOTE: does NOT remove links from the popped node
    '''
    head, prev = index_and_prev(head, idx)

    # head is at index, 3 cases:
    if not head:  # end of list, this is an error, nothing to pop
        raise IndexError(f'idx {idx} does not exist')
    else:
        if prev is None:  # start of list, telling to pop the head...
            return head
        else:  # middle of list, need to reassign ptrs
            head.prev = prev
            prev.next = head.next
            return head


def tail(head):
    # type: (DllNode) -> DllNode
    while head.next is not None:
        head = head.next
    return head
