#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
Author:         Chris Carl
Email:          chrisbcarl@outlook.com
Date:           2024-11-24
Description:

files.manifest is literally what it says on the tin
files are modules that elevate files so they can be used in python, either registering the path name or actually interacting with them like data cabinets.

Updates:
    2024-11-24 - files.manifest - initial commit
'''

# stdlib imports
from __future__ import absolute_import, print_function, division, with_statement  # , unicode_literals
import os
import sys
import logging

# third party imports

# project imports

SCRIPT_RELPATH = 'chriscarl/files/manifest.py'
if not hasattr(sys, '_MEIPASS'):
    SCRIPT_FILEPATH = os.path.abspath(__file__)
else:
    SCRIPT_FILEPATH = os.path.abspath(os.path.join(sys._MEIPASS, SCRIPT_RELPATH))  # pylint: disable=no-member
SCRIPT_DIRPATH = os.path.dirname(SCRIPT_FILEPATH)
SCRIPT_NAME = os.path.splitext(os.path.basename(__file__))[0]
THIS_MODULE = sys.modules[__name__]
LOGGER = logging.getLogger(__name__)
LOGGER.addHandler(logging.NullHandler())

# ###

# ./
DIRPATH_ROOT = SCRIPT_DIRPATH
FILEPATH_DEFAULT_DESCRIPTIONS_JSON = os.path.join(DIRPATH_ROOT, 'default-descriptions.json')
FILEPATH_MANIFEST_PY = os.path.join(DIRPATH_ROOT, 'manifest.py')

# ./templates
DIRPATH_TEMPLATES = os.path.join(SCRIPT_DIRPATH, './templates')
FILEPATH_MOD_LIB_TEMPLATE = os.path.join(DIRPATH_TEMPLATES, 'mod.lib.template')
FILEPATH_TEMPLATE = os.path.join(DIRPATH_TEMPLATES, 'template')
FILEPATH_TEST_TEMPLATE = os.path.join(DIRPATH_TEMPLATES, 'test.template')
FILEPATH_TOOL_TEMPLATE = os.path.join(DIRPATH_TEMPLATES, 'tool.template')

# ./templates/git
DIRPATH_GIT = os.path.join(SCRIPT_DIRPATH, './templates/git')
FILEPATH_CHANGELOG_MD = os.path.join(DIRPATH_GIT, 'CHANGELOG.md')
FILEPATH_PYPROJECT_TOML = os.path.join(DIRPATH_GIT, 'pyproject.toml')
FILEPATH_README_MD = os.path.join(DIRPATH_GIT, 'README.md')

# ###