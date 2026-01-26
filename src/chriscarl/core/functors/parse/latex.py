#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
Author:         Chris Carl
Email:          chrisbcarl@outlook.com
Date:           2026-01-25
Description:

core.functors.parse.latex is... TODO: lorem ipsum
core.functor are modules that functions that are usually defined as lambdas, but i like to hold onto them as named funcs. non-self-referential, low-import, etc.

Updates:
    2026-01-25 - core.functors.parse.latex - initial commit
'''

# stdlib imports
from __future__ import absolute_import, print_function, division, with_statement  # , unicode_literals
import os
import sys
import logging
import re

# third party imports

# project imports

SCRIPT_RELPATH = 'chriscarl/core/functors/parse/latex.py'
if not hasattr(sys, '_MEIPASS'):
    SCRIPT_FILEPATH = os.path.abspath(__file__)
else:
    SCRIPT_FILEPATH = os.path.abspath(os.path.join(sys._MEIPASS, SCRIPT_RELPATH))  # pylint: disable=no-member
SCRIPT_DIRPATH = os.path.dirname(SCRIPT_FILEPATH)
SCRIPT_NAME = os.path.splitext(os.path.basename(__file__))[0]
THIS_MODULE = sys.modules[__name__]
LOGGER = logging.getLogger(__name__)
LOGGER.addHandler(logging.NullHandler())

REGEX_LATEX_NEEDS_ESCAPE = re.compile(r'([^\\])([$#%&~_^{}])')


def latex_escape(substr, regex=REGEX_LATEX_NEEDS_ESCAPE):
    # type: (str, re.Pattern) -> str
    # find characters that are NOT escaped, and escape them...
    # catch characters in a row like _____
    regex_comp = re.compile(regex)
    while regex_comp.search(substr):
        # {} within just causes problems.
        substr = regex_comp.sub(r'\1\\\2', substr)
    return substr
