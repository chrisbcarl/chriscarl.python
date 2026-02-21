#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
Author:         Chris Carl
Email:          chrisbcarl@outlook.com
Date:           2026-02-20
Description:

core.types.bool is mostly bool conversion
core.types are modules that pertain to data structures, algorithms, conversions. non-self-referential, low-import, etc.

Updates:
    2026-02-20 - core.types.bool - initial commit
'''

# stdlib imports
from __future__ import absolute_import, print_function, division, with_statement  # , unicode_literals
import os
import sys
import logging
from typing import Any

# third party imports

# project imports

SCRIPT_RELPATH = 'chriscarl/core/types/bool.py'
if not hasattr(sys, '_MEIPASS'):
    SCRIPT_FILEPATH = os.path.abspath(__file__)
else:
    SCRIPT_FILEPATH = os.path.abspath(os.path.join(sys._MEIPASS, SCRIPT_RELPATH))  # pylint: disable=no-member
SCRIPT_DIRPATH = os.path.dirname(SCRIPT_FILEPATH)
SCRIPT_NAME = os.path.splitext(os.path.basename(__file__))[0]
THIS_MODULE = sys.modules[__name__]
LOGGER = logging.getLogger(__name__)
LOGGER.addHandler(logging.NullHandler())

TRUTHY = {'1', 'yes', 'y', 'true', 't', 'positive'}
FALSEY = {'0', 'no', 'n', 'false', 'f', 'negative'}


def boolean(txt):
    # type: (Any) -> bool
    text = str(txt).lower()
    if text in TRUTHY:
        return True
    elif text in FALSEY:
        return False
    else:
        if any(text.startswith(token) for token in FALSEY):
            return False
        elif any(text.startswith(token) for token in TRUTHY):
            return True
        return bool(txt)
