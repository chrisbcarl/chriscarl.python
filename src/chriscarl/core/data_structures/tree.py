#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
Author:         Chris Carl
Email:          chrisbcarl@outlook.com
Date:           2026-02-15
Description:

core.data_structures.tree is as thoughroughly capturing trees as much as I can, the printing is especially nice
core are modules that define the bedrock from which other things do import. non-self-referential, low-import, etc.

Updates:
    2026-02-27 - core.data_structures.tree - order printing works correctly, overall very nice, NOT THOUGHROUGHLY TESTED
    2026-02-15 - core.data_structures.tree - initial commit
'''

# stdlib imports
from __future__ import absolute_import, print_function, division, with_statement  # , unicode_literals
import os
import sys
import logging
import math
from typing import Optional, Any, Generator, Tuple, List

# third party imports

# project imports
from chriscarl.core.data_structures.node import Node
from chriscarl.core.data_structures.doubly_linked_list import DllNode

SCRIPT_RELPATH = 'chriscarl/core/data_structures/tree.py'
if not hasattr(sys, '_MEIPASS'):
    SCRIPT_FILEPATH = os.path.abspath(__file__)
else:
    SCRIPT_FILEPATH = os.path.abspath(os.path.join(sys._MEIPASS, SCRIPT_RELPATH))  # pylint: disable=no-member
SCRIPT_DIRPATH = os.path.dirname(SCRIPT_FILEPATH)
SCRIPT_NAME = os.path.splitext(os.path.basename(__file__))[0]
THIS_MODULE = sys.modules[__name__]
LOGGER = logging.getLogger(__name__)
LOGGER.addHandler(logging.NullHandler())


class TreeNode(DllNode):
    neighbors = []  # type: List[Optional[TreeNode]]

    def __init__(self, data, left=None, right=None):
        super().__init__(data, prev=left, next=right)

    @property
    def left(self):
        # type: () -> Optional[TreeNode]
        return self.prev

    @left.setter
    def left(self, value):
        # type: (Node|Any) -> None
        self.prev = value

    @property
    def right(self):
        # type: () -> Optional[TreeNode]
        return self.next

    @right.setter
    def right(self, value):
        # type: (Node|Any) -> None
        self.next = value

    def add_left(self, data):
        # type: (Any) -> Node
        n = data if isinstance(data, TreeNode) else TreeNode(data)
        ptr = self
        while ptr and ptr.left:
            ptr = ptr.left
        ptr.left = n
        return n

    def add_right(self, data):
        # type: (Any) -> Node
        n = data if isinstance(data, TreeNode) else TreeNode(data)
        ptr = self
        while ptr and ptr.right:
            ptr = ptr.right
        ptr.right = n
        return n

    def insert(self, data, balanced=False):
        # TODO: complete (left-right...)
        if balanced:
            count_l, count_r = count(self.left), count(self.right)
            if count_l == count_r:
                # if they're 0 first, then start left
                if not self.left:
                    return self.add_left(data)
                else:
                    return self.left.insert(data, balanced=balanced)
            else:
                # imbalanced? balance right
                if not self.right:
                    return self.add_right(data)
                else:
                    return self.right.insert(data, balanced=balanced)

        if data < self.data:
            if self.left:
                self.left.insert(data)
            else:
                self.add_left(data)
        else:
            if self.right:
                self.right.insert(data)
            else:
                self.add_right(data)
        return self

    def count(self):
        total = 0
        if self.left:
            total += self.left.count()
        total += 1
        if self.right:
            total += self.right.count()
        return total

    def to_list(self, include_none=False):
        # NOTE: BFS results in heap list
        lst = []
        queue = [self]  # type: List[Node|None]
        while queue:
            node = queue.pop(0)  # must be fifo, pop front, insert back
            if node is None:
                lst.append(None)
            else:
                lst.append(node.data)
                if include_none:
                    # for some reason its good to have empty slots represented in list
                    queue.append(node.left)
                    queue.append(node.right)
                else:
                    if node.left:
                        queue.append(node.left)
                    if node.right:
                        queue.append(node.right)
        return lst

    @classmethod
    def from_list(cls, lst, balanced=False):
        if len(lst) == 0:
            raise ValueError()
        root = Node(lst[0])
        for idx in range(1, len(lst)):
            root.insert(lst[idx], balanced=balanced)
        return root


def inorder(node, i=1, null=False):
    # type: (Optional[TreeNode], int, bool) -> Generator[TreeNode, None, None]
    if node:
        for n in inorder(node.left, i=i + 1, null=null):
            yield n
        yield node
        for n in inorder(node.right, i=i + 2, null=null):
            yield n
    elif null:
        yield None


def preorder(node, i=1, null=False):
    # type: (Optional[TreeNode], int, bool) -> Generator[TreeNode, None, None]
    if node:
        yield node
        for n in preorder(node.left, i=i + 1, null=null):
            yield n
        for n in preorder(node.right, i=i + 2, null=null):
            yield n
    elif null:
        yield None


def postorder(node, i=1, null=False):
    # type: (Optional[TreeNode], int, bool) -> Generator[TreeNode, None, None]
    if node:
        for n in postorder(node.left, i=i + 1, null=null):
            yield n
        for n in postorder(node.right, i=i + 2, null=null):
            yield n
        yield node
    elif null:
        yield None


def levelorder(node):
    # type: (Optional[TreeNode]) -> Generator[TreeNode, None, None]
    fifo = [node]
    while fifo:
        n = fifo.pop(0)  # python pip is FILO
        if n is None:
            continue

        if n.left:
            fifo.append(n.left)
        if n.right:
            fifo.append(n.right)
        yield n


def insert(node, data):
    # type: (Node, Any) -> Node
    if data < node.data:
        if node.left:
            n = insert(node.left, data)
        else:
            n = Node(data)
            node.left = n
    else:
        if node.right:
            n = insert(node.right, data)
        else:
            n = Node(data)
            node.right = n
    return n


def count(node):
    # type: (Optional[TreeNode]) -> int
    if not node:
        return 0
    return 1 + count(node.left) + count(node.right)


def height(node):
    # type: (Optional[TreeNode]) -> int
    if not node:
        return -1  # a leaf does not count as a depth
    return max([height(node.left) + 1, height(node.right) + 1])


def node_str_len(node):
    # type: (Optional[TreeNode]) -> int
    if not node:
        return 0
    return max([len(str(node.data)), node_str_len(node.left), node_str_len(node.right)])


def to_str(root):
    # type: (TreeNode) -> str
    '''
    Algorithm is level-order:
        height 0 (leaf level doesnt count toward height, contains 1 leaf)
            x 00 01 02 03 04 05 06 07 08 09 10 11 12 13 14
            0 01                                            - start at 00, 1st element offset by 0, every other separate by 1

        height 1, 2^1 = 2
            x 00 01 02 03 04 05 06 07 08 09 10 11 12 13 14
            0    01                                         - start at 00, 1st element offset by 1, every other separate by 3
            1 02    03                                      - start at 00, 1st element offset by 0, every other separate by 1

        height 2, 2^2 = 4
            x 00 01 02 03 04 05 06 07 08 09 10 11 12 13 14
            0          01                                   - start at 00, 1st element offset by 3, every other separate by 7
            1    02          03                             - start at 00, 1st element offset by 1, every other separate by 3
            2 04    05    06    07                          - start at 00, 1st element offset by 0, every other separate by 1

        height 3, 2^3 = 8
            x 00 01 02 03 04 05 06 07 08 09 10 11 12 13 14
            0                      01                       - start at 00, 1st element offset by 7, every other separate by 15
            1          02                      03           - start at 00, 1st element offset by 3, every other separate by 7
            2    04          05          06          07     - start at 00, 1st element offset by 1, every other separate by 3
            3 08    09    10    11    12    13    14    15  - start at 00, 1st element offset by 0, every other separate by 1

        lines = []
        line = []
        depth_current = -1
        height = height(tree)
        for node i in tree level-order, 1-indexed
            depth = floor(log2(i))
            offset = 2^(height - depth) - 1
            if depth_current != depth:
                depth_current = depth
                if line:
                    for o in offset:
                        line.push(padding)
                    lines.append(line)
                    line.clear()

            separate = 2^(height + 1 - depth) - 1
            line.append(i)
            for s in separate:
                line.append(padding)

    '''
    lines = []
    line = []
    h = height(root)
    length = node_str_len(root)
    fmt = f'{{:^{length}s}}'
    dummy = fmt.format('-')
    padding = fmt.format(' ')
    depth_current = -1
    queue = [root]  # type: List[Node|None]
    i = 1  # 1-indexed node counting
    while queue:
        node = queue.pop(0)  # must be fifo, pop front, insert back
        depth = math.floor(math.log2(i))
        offset = int(2**(h - depth) - 1)
        separate = int(2**(h + 1 - depth) - 1)
        # print(f'i: {i}; node: {node}; height: {height}; depth: {depth}; offset: {offset}; separate: {separate}')
        if depth_current != depth:
            depth_current = depth
            if line:
                lines.append(''.join(line).rstrip())
                line.clear()
            for _ in range(offset):
                line.insert(0, padding)

        str_node = fmt.format(str(node.data) if node is not None else dummy)
        line.append(str_node)
        for _ in range(separate):
            line.append(padding)

        if node:
            if node.left:
                queue.append(node.left)
            else:
                if depth < h:
                    queue.append(None)

            if node.right:
                queue.append(node.right)
            else:
                if depth < h:
                    queue.append(None)
        else:
            if depth < h:
                queue.append(None)
                queue.append(None)

        i += 1

    if line:
        lines.append(''.join(line).rstrip())
        line.clear()

    return '\n'.join(lines)
