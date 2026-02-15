#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
Author:         Chris Carl
Email:          chrisbcarl@outlook.com
Date:           2026-02-15
Description:

core.data_structures.node is an overkill superclass node that can be used by lists, trees, graphs, etc.
core are modules that define the bedrock from which other things do import. non-self-referential, low-import, etc.

Updates:
    2026-02-15 - core.data_structures.node - initial commit
'''

# stdlib imports
from __future__ import absolute_import, print_function, division, with_statement  # , unicode_literals
import os
import sys
import logging
from typing import Any

# third party imports

# project imports

SCRIPT_RELPATH = 'chriscarl/core/data_structures/node.py'
if not hasattr(sys, '_MEIPASS'):
    SCRIPT_FILEPATH = os.path.abspath(__file__)
else:
    SCRIPT_FILEPATH = os.path.abspath(os.path.join(sys._MEIPASS, SCRIPT_RELPATH))  # pylint: disable=no-member
SCRIPT_DIRPATH = os.path.dirname(SCRIPT_FILEPATH)
SCRIPT_NAME = os.path.splitext(os.path.basename(__file__))[0]
THIS_MODULE = sys.modules[__name__]
LOGGER = logging.getLogger(__name__)
LOGGER.addHandler(logging.NullHandler())


class Node(object):
    neighbors = []  # type: list
    data = None  # type: Any

    def __init__(self, data):
        self.data = data
        self.neighbors = []

    def __str__(self):
        return f'{self.__class__.__name__}[{self.data}]'

    def __repr__(self):
        return f'{self.__class__.__name__}[{self.data}, {len([neighbor for neighbor in self.neighbors if neighbor])}E]'

    def __eq__(self, other):
        if not isinstance(other, Node):
            return False
        return self.data == other.data

    def __lt__(self, other):
        if not isinstance(other, Node):
            return False
        if self.data is None:
            if other.data is None:
                return False
            else:
                return True
        return self.data < other.data

    def add_edge(self, node):
        # type: (Node|Any) -> Node
        self.neighbors.append(Node(node))
        return node

    @property
    def edges(self):
        return [n for n in self.neighbors]
