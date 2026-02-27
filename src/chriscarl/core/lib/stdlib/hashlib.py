#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
Author:         Chris Carl
Email:          chrisbcarl@outlook.com
Date:           2026-02-27
Description:

core.lib.stdlib.hashlib is thin wrappers around hashing stuff
core.lib are modules that contain code that is about (but does not modify) the library. somewhat referential to core.functor and core.types.

Updates:
    2026-02-27 - core.lib.stdlib.hashlib - initial commit
'''

# stdlib imports
from __future__ import absolute_import, print_function, division, with_statement  # , unicode_literals
import os
import sys
import logging
import hashlib

# third party imports

# project imports
from chriscarl.core.lib.stdlib.os import is_file
from chriscarl.core.lib.stdlib.io import read_text_file

SCRIPT_RELPATH = 'chriscarl/core/lib/stdlib/hashlib.py'
if not hasattr(sys, '_MEIPASS'):
    SCRIPT_FILEPATH = os.path.abspath(__file__)
else:
    SCRIPT_FILEPATH = os.path.abspath(os.path.join(sys._MEIPASS, SCRIPT_RELPATH))  # pylint: disable=no-member
SCRIPT_DIRPATH = os.path.dirname(SCRIPT_FILEPATH)
SCRIPT_NAME = os.path.splitext(os.path.basename(__file__))[0]
THIS_MODULE = sys.modules[__name__]
LOGGER = logging.getLogger(__name__)
LOGGER.addHandler(logging.NullHandler())


def md5(content):
    # type: (str) -> str
    if is_file(content):
        content = read_text_file(content)
    ciphertext = hashlib.md5(content.encode())
    return ciphertext.hexdigest()
