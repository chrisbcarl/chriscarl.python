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
    2026-02-01 - core.functors.parse.bibtex - periods work as keys
    2026-01-25 - core.functors.parse.bibtex - initial commit
                 core.functors.parse.bibtex - added prettification
'''

# stdlib imports
from __future__ import absolute_import, print_function, division, with_statement  # , unicode_literals
import os
import sys
import logging
import re
from typing import Dict, Tuple

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

REGEX_BIBTEX_CITATION_KEY = re.compile(r'@(?P<type>[a-zA-z_-]+)\{(?P<label>[A-Za-z0-9_\-\.]+)?,?')


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


def bibtex_find_start_endpoint(text, idx):
    # type: (str, int) -> Tuple[int, int]
    mo = REGEX_BIBTEX_CITATION_KEY.search(text, idx)
    if not mo:
        return -1, -1
    start = idx = mo.start()
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
    return start, idx


def extract_from(text, pretty=True, indent=4):
    # type: (str, bool, int) -> str
    '''
    Description:
        given ANY text, find the relevant bibtex inside it.
    Returns:
        str
    '''
    tex = []
    end = 0
    while end < len(text):
        start, end = bibtex_find_start_endpoint(text, end)
        if start == -1:
            break
        block = text[start:end].strip()
        if pretty:
            mo = REGEX_BIBTEX_CITATION_KEY.search(block)
            if not mo:
                raise RuntimeError('this shouldnt be happening ever!')
            pend = mo.end()
            top_line = block[mo.start():pend]
            end_line = block[-1]
            midsection = block[pend:-1].strip()
            lines = []
            for line in midsection.splitlines():
                line = line.strip()
                if not line:
                    continue
                if line.startswith('%'):
                    lines.append(('', line))
                    continue
                if '=' not in line:
                    raise ValueError(f'bibtex multilines not supported! see line "{line}"')
                key, value = line.split('=')
                lines.append((key.strip(), value.strip()))
            max_key_len = max(len(tpl[0]) for tpl in lines)
            fmt = '%s{:%ds} = {:}' % (' ' * indent, max_key_len)
            midsection = '\n'.join(fmt.format(key, value) if key else f'{" " * indent}{value}' for key, value in lines)
            block = f'{top_line}\n{midsection}\n{end_line}'  # prettified

        tex.append(block)
    return '\n'.join(tex)
