#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
Author:         Chris Carl
Email:          chrisbcarl@outlook.com
Date:           2026-02-27
Description:

core.data_structures.stack is just quickly explaining a stack in terms of python list (unmodified, pop -1)
core are modules that define the bedrock from which other things do import. non-self-referential, low-import, etc.

Updates:
    2026-02-27 - core.data_structures.stack - initial commit
'''

# stdlib imports
from __future__ import absolute_import, print_function, division, with_statement  # , unicode_literals
import os
import sys
import logging
from typing import Any, SupportsIndex

# third party imports

# project imports

SCRIPT_RELPATH = 'chriscarl/core/data_structures/stack.py'
if not hasattr(sys, '_MEIPASS'):
    SCRIPT_FILEPATH = os.path.abspath(__file__)
else:
    SCRIPT_FILEPATH = os.path.abspath(os.path.join(sys._MEIPASS, SCRIPT_RELPATH))  # pylint: disable=no-member
SCRIPT_DIRPATH = os.path.dirname(SCRIPT_FILEPATH)
SCRIPT_NAME = os.path.splitext(os.path.basename(__file__))[0]
THIS_MODULE = sys.modules[__name__]
LOGGER = logging.getLogger(__name__)
LOGGER.addHandler(logging.NullHandler())


class Stack(list):
    '''
    Description:
        UNMODIFIED python list!
    '''

    def push(self, object: Any) -> None:
        return self.append(object)

    def pop(self, index: SupportsIndex = -1) -> Any:
        return super().pop(index)


class LIFO(Stack):
    '''
    Description:
        push 1, push 2, push 3, pop == 3, the last inserted is first out
        [1, 2, 3].pop(-1) == 3
    '''
    pass
