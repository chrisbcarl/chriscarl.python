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
    2026-01-19 - core.constants - added MAIN constants to allow other projects to reference collaterals
    2026-01-17 - core.constants - BUG: fixed problems caused by __init__.py and removed circular import issue
    2026-01-13 - core.constants - added fix_constants to deal with namespace development
    2026-01-07 - core.constants - updated to deal with change to namespace rather than regular module.
    2024-11-22 - core.constants - initial commit
'''

# stdlib imports
from __future__ import absolute_import, print_function, division, with_statement  # , unicode_literals
import os
import sys
import logging
import datetime
from types import ModuleType

# third party imports

# project imports
import chriscarl
import chriscarl.core.lib.stdlib

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
CWD = os.getcwd()
MODULE_DIRPATH = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
PYPA_SRC_DIRPATH = os.path.abspath(os.path.join(MODULE_DIRPATH, '../'))
REPO_DIRPATH = os.path.abspath(os.path.join(PYPA_SRC_DIRPATH, '../'))
TESTS_DIRPATH = os.path.abspath(os.path.join(REPO_DIRPATH, 'tests'))
TESTS_COLLATERAL_DIRPATH = os.path.abspath(os.path.join(TESTS_DIRPATH, 'collateral'))
PIP_DEVELOP_MODE = PYPA_SRC_DIRPATH.endswith('src')
MAIN_TESTS_DIRPATH = ''
MAIN_TESTS_COLLATERAL_DIRPATH = ''
CWD = os.getcwd()
NOW = datetime.datetime.now()
DATE = NOW.strftime('%Y-%m-%d')
TIME = NOW.strftime('%H:%M:%S.%f')
SENTINEL = '0cc44c50-5d1e-4529-b8c3-5ee4271aa5a0_338ad6d4-ce81-4e13-9ccc-5a34cf55947b'
NAMESPACED_MODULES = [
    'chriscarl',
    'chriscarl.tools',
    'chriscarl.tools.shed',
    'chriscarl.core',
    'chriscarl.core.lib',
    'chriscarl.core.lib.third',
]

TEMP_DIRPATH = '/temp'
if sys.platform != 'win32':
    TEMP_DIRPATH = '/tmp'


def fix_constants(module):
    # type: (ModuleType) -> None
    '''
    Description:
        If running a test file from a namespaced project, these paths will be wrong,
            so that needs to be fixed depending.
    Arguments:

    Returns:
        None
    '''
    global CWD, PYPA_SRC_DIRPATH, REPO_DIRPATH, TESTS_DIRPATH, TESTS_COLLATERAL_DIRPATH, PIP_DEVELOP_MODE, MAIN_TESTS_DIRPATH, MAIN_TESTS_COLLATERAL_DIRPATH
    if not isinstance(module, ModuleType):
        raise TypeError(f"'module' must be of type {ModuleType}, provided {type(module)}!")
    # isinstance_raise(module, ModuleType)  # NOTE: cannot do this, causes circular imports...
    module_str = module.__name__
    module_tokens = module_str.split('.')
    if len(module_tokens) == 1:
        return
    if module_tokens[0] != chriscarl.__name__:
        return  # nothing to modify, irrelevant

    if not hasattr(module, '__file__'):
        raise RuntimeError(f'{module_str!r} cannot fix_constants on a namespace module that doesnt have a __file__!')

    if not module.__file__:  # namespaced modules trigger this
        return

    if os.path.basename(module.__file__) == '__init__.py':
        module_dirpath = os.path.dirname(module.__file__)
    else:
        module_dirpath = module.__file__
    ups = ['../'] * (len(module_tokens) - 1)
    module_dirpath = os.path.abspath(os.path.join(module_dirpath, *ups))

    CWD = os.getcwd()
    PYPA_SRC_DIRPATH = os.path.abspath(os.path.join(module_dirpath, '../'))
    REPO_DIRPATH = os.path.abspath(os.path.join(PYPA_SRC_DIRPATH, '../'))
    TESTS_DIRPATH = os.path.abspath(os.path.join(REPO_DIRPATH, 'tests'))
    TESTS_COLLATERAL_DIRPATH = os.path.abspath(os.path.join(TESTS_DIRPATH, 'collateral'))
    PIP_DEVELOP_MODE = PYPA_SRC_DIRPATH.endswith('src')
    if PIP_DEVELOP_MODE and not os.path.isdir(TESTS_DIRPATH):
        raise RuntimeError('constants is badly configured, not sure how?')
    if not MAIN_TESTS_DIRPATH:  # populates initially, and then never again.
        MAIN_TESTS_DIRPATH = TESTS_DIRPATH
        MAIN_TESTS_COLLATERAL_DIRPATH = TESTS_COLLATERAL_DIRPATH


fix_constants(chriscarl.core.lib.stdlib)
