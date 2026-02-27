#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
Author:         Chris Carl
Email:          chrisbcarl@outlook.com
Date:           2026-02-15
Description:

core.data_structures.singly_linked_list is a somewhat overkill class that gets the singly linked list accomplished.
core are modules that define the bedrock from which other things do import. non-self-referential, low-import, etc.

Updates:
    2026-02-26 - core.data_structures.singly_linked_list - finally added all the modification funcs
    2026-02-15 - core.data_structures.singly_linked_list - initial commit
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

SCRIPT_RELPATH = 'chriscarl/core/data_structures/singly_linked_list.py'
if not hasattr(sys, '_MEIPASS'):
    SCRIPT_FILEPATH = os.path.abspath(__file__)
else:
    SCRIPT_FILEPATH = os.path.abspath(os.path.join(sys._MEIPASS, SCRIPT_RELPATH))  # pylint: disable=no-member
SCRIPT_DIRPATH = os.path.dirname(SCRIPT_FILEPATH)
SCRIPT_NAME = os.path.splitext(os.path.basename(__file__))[0]
THIS_MODULE = sys.modules[__name__]
LOGGER = logging.getLogger(__name__)
LOGGER.addHandler(logging.NullHandler())


class SllNode(Node):
    neighbors = []  # type: List[Optional[SllNode]]

    def __init__(self, data, next=None):
        super().__init__(data)
        self.neighbors = [next]

    @property
    def next(self):
        # type: () -> Optional[SllNode]
        return self.neighbors[0]

    @next.setter
    def next(self, value):
        # type: (SllNode|Any) -> None
        if value is not None:
            self.neighbors[0] = value if isinstance(value, SllNode) else SllNode(value)
        else:
            self.neighbors[0] = None


class SinglyLinkedList():
    head = SllNode(0)  # type: SllNode
    size = 0

    def __init__(self, node_or_data):
        if isinstance(node_or_data, SllNode):
            self.head = node_or_data
        else:
            self.head = SllNode(node_or_data)
        self.size = count(self.head)

    def __str__(self):
        return to_str(self.head)

    def __len__(self):
        return self.size

    def __eq__(self, other):
        if not isinstance(other, SinglyLinkedList):
            return False
        if self.size == other.size:
            ptr_self = self.head
            ptr_oth = other.head
            while ptr_self:
                if ptr_self != ptr_oth:
                    return False
                ptr_self = ptr_self.next
                ptr_oth = ptr_oth.next
            return True
        return False

    def to_list(self):
        # type: () -> List[Any]
        return to_list(self.head)

    @classmethod
    def from_list(cls, lst):
        # type: (List[Any]) -> SinglyLinkedList
        head = from_list(lst)
        return SinglyLinkedList(head)

    def append(self, value):
        # type: (SllNode|Any) -> SllNode
        new = append(self.head, value)
        self.size = count(self.head)
        return new

    def insert(self, idx, value):
        # type: (int, Any) -> SllNode
        new = insert(self.head, idx, value)
        if idx == 0:
            self.head = new
        self.size = count(self.head)
        return new

    def emplace(self, idx, value):
        # type: (int, Any) -> SllNode
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
        # type: () -> SllNode
        return tail(self.head)


def to_list(head):
    # type: (Optional[SllNode]) -> List[Any]
    lst = []
    ptr = head
    while ptr:
        lst.append(ptr.data)
        ptr = ptr.next
    return lst


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


def count(head):
    # type: (Optional[SllNode]) -> int
    cnt = 0
    ptr = head
    while ptr:
        cnt += 1
        ptr = ptr.next
    return cnt


def append(head, value):
    # type: (SllNode, SllNode|Any) -> SllNode
    new = value if isinstance(value, SllNode) else SllNode(value)
    ptr = head
    while ptr.next:
        ptr = ptr.next
    ptr.next = new
    return new


def to_str(head):
    # type: (Optional[SllNode]) -> str
    if not head:
        return ''
    tokens = to_list(head)
    return ' -> '.join(str(token) for token in tokens)


def index_and_prev(head, idx):
    # type: (SllNode|None, int) -> Tuple[SllNode|None, SllNode|None]
    if idx < 0:
        raise IndexError(f'idx {idx} does not exist')
    prev = None  # type: SllNode|None
    while idx > 0:
        if head is None:
            raise IndexError(f'idx {idx} does not exist')

        prev = head
        head = head.next
        idx -= 1
    return head, prev


def index(head, idx):
    # type: (SllNode|None, int) -> SllNode|None
    head, _ = index_and_prev(head, idx)
    return head


def emplace(head, idx, value):
    # type: (SllNode|None, int, Any) -> SllNode
    head, prev = index_and_prev(head, idx)

    # head is at index, 3 cases:
    new = SllNode(value)
    if not head:  # we're at the end of the list, so this is just append
        prev.next = new
    else:
        if prev is None:  # beginning of list
            new.next = head.next  # old head still attached
        else:  # middle of the list
            new.next = head.next  # old middle still attached
            prev.next = new
    return new


def insert(head, idx, value):
    # type: (SllNode|None, int, Any) -> SllNode
    '''4, 5, 6 insert(4, 1, 1) -> 4156 insert: "insert at"'''
    head, prev = index_and_prev(head, idx)

    # head is at index, 3 cases:
    new = SllNode(value)
    if head is None:  # we're at the end of the list, so this is just append
        prev.next = new
    else:
        if prev is None:  # beginning of list
            new.next = head
        else:  # middle of the list
            prev.next = new
            new.next = head
    return new


def remove(head, idx):
    # type: (SllNode|None, int) -> SllNode
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
            prev.next = head.next
            return head


def tail(head):
    # type: (SllNode) -> SllNode
    while head.next is not None:
        head = head.next
    return head
