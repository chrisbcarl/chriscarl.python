#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
Author:         Chris Carl
Email:          chrisbcarl@outlook.com
Date:           2026-01-25
Description:

core.functors.parse.bibtex is funcs that deal with text that is hopefully bibtex...
core.functor are modules that functions that are usually defined as lambdas, but i like to hold onto them as named funcs. non-self-referential, low-import, etc.

Updates:
    2026-01-25 - core.functors.parse.bibtex - initial commit
'''

# stdlib imports
from __future__ import absolute_import, print_function, division, with_statement  # , unicode_literals
import os
import sys
import logging
import re
from typing import Dict

# third party imports

# project imports

SCRIPT_RELPATH = 'chriscarl/core/functors/parse/bibtex.py'
if not hasattr(sys, '_MEIPASS'):
    SCRIPT_FILEPATH = os.path.abspath(__file__)
else:
    SCRIPT_FILEPATH = os.path.abspath(os.path.join(sys._MEIPASS, SCRIPT_RELPATH))  # pylint: disable=no-member
SCRIPT_DIRPATH = os.path.dirname(SCRIPT_FILEPATH)
SCRIPT_NAME = os.path.splitext(os.path.basename(__file__))[0]
THIS_MODULE = sys.modules[__name__]
LOGGER = logging.getLogger(__name__)
LOGGER.addHandler(logging.NullHandler())

REGEX_BIBTEX_CITATION_KEY = re.compile(r'@(?P<type>[a-zA-z_-]+)\{(?P<label>[A-Za-z0-9_-]+)?,?')


def get_labels(text, raise_on_null=True):
    # type: (str, bool) -> Dict[str, str]
    '''
    Description:
        given any text, find bibtex citation label
    Arguments:
        raise_on_null: bool
            default True
            raise ValueError if a label is missing in a citation
    Returns:
        Dict[str, str]
            label, citation type
    '''
    dick = {}
    for mo in REGEX_BIBTEX_CITATION_KEY.finditer(text):
        groups = mo.groupdict()
        typ, label = groups['type'], groups['label']
        if raise_on_null and not label:
            raise ValueError(f'could not determine label for {text[mo.start():mo.end()]!r}')
        dick[label] = typ
    return dick


def extract_from(text):
    # type: (str) -> str
    '''
    Description:
        given ANY text, find the relevant bibtex inside it.
    Returns:
        str
    '''
    tex = []
    idx = 0
    while idx < len(text):
        mo = REGEX_BIBTEX_CITATION_KEY.search(text, idx)
        if not mo:
            break
        idx = mo.start()
        while text[idx] != '{':
            idx += 1
        stack = ['{']
        idx += 1
        while stack:
            char = text[idx]
            if char == '{':
                stack.insert(0, char)
            elif char == '}':
                stack.pop(0)
            idx += 1

        tex.append(text[mo.start():idx])
    return '\n'.join(tex)
