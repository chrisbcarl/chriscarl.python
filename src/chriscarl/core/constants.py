#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
Author:         Chris Carl
Email:          chrisbcarl@outlook.com
Date:           2024-11-22
Description:

core.constants are useful to have actual constants
core are modules that define the bedrock from which other things do import. non-self-referential, low-import, etc.

Updates:
    2026-01-07 - core.constants - updated to deal with change to namespace rather than regular module.
    2024-11-22 - core.constants - initial commit
'''

# stdlib imports
from __future__ import absolute_import, print_function, division, with_statement  # , unicode_literals
import os
import sys
import logging
import datetime

# third party imports

# project imports

SCRIPT_RELPATH = 'chriscarl/core/constants.py'
if not hasattr(sys, '_MEIPASS'):
    SCRIPT_FILEPATH = os.path.abspath(__file__)
else:
    SCRIPT_FILEPATH = os.path.abspath(os.path.join(sys._MEIPASS, SCRIPT_RELPATH))  # pylint: disable=no-member
SCRIPT_DIRPATH = os.path.dirname(SCRIPT_FILEPATH)
SCRIPT_NAME = os.path.splitext(os.path.basename(__file__))[0]
THIS_MODULE = sys.modules[__name__]
LOGGER = logging.getLogger(__name__)
LOGGER.addHandler(logging.NullHandler())

# MODULE_DIRPATH = os.path.abspath(os.path.dirname(chriscarl.__file__))
# cannot do this because chriscarl is now a namespace, not a regular module
MODULE_DIRPATH = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
PYPA_SRC_DIRPATH = os.path.join(MODULE_DIRPATH, '../')
REPO_DIRPATH = os.path.join(PYPA_SRC_DIRPATH, '../')
TESTS_DIRPATH = os.path.join(REPO_DIRPATH, 'tests')
TEST_COLLATERAL_DIRPATH = os.path.join(TESTS_DIRPATH, 'collateral')
CWD = os.getcwd()
NOW = datetime.datetime.now()
DATE = NOW.strftime('%Y-%m-%d')
TIME = NOW.strftime('%H:%M:%S.%f')
SENTINEL = '0cc44c50-5d1e-4529-b8c3-5ee4271aa5a0_338ad6d4-ce81-4e13-9ccc-5a34cf55947b'

TEMP_DIRPATH = '/temp'
if sys.platform != 'win32':
    TEMP_DIRPATH = '/tmp'
