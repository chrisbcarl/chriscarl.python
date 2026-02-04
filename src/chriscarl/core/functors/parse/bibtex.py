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
    2026-02-04 - core.functors.parse.bibtex - added extract_from_and_remove, get_label_citation--slight re-work to support extracting non-bibtex and dealing with label duplicates and nulls
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


def get_labels(text, nulls=False):
    # type: (str, bool) -> Dict[str, str]
    '''
    Description:
        given any text, find bibtex citation label
    Arguments:
        nulls: bool
            default False, raise KeyError if a label is missing in a citation
    Returns:
        Dict[str, str]
            label, citation type
    '''
    dick = {}
    for mo in REGEX_BIBTEX_CITATION_KEY.finditer(text):
        groups = mo.groupdict()
        typ, label = groups['type'], groups['label']
        if not nulls and not label:
            raise KeyError(f'could not determine label for {text[mo.start():mo.end()]!r}')
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


def extract_from_and_remove(text, pretty=True, indent=4):
    # type: (str, bool, int) -> Tuple[str, str]
    '''
    Description:
        given ANY text, find the relevant bibtex inside it.
        also return all the text around it without the bibtex
    Returns:
        str
    '''
    non_tex = []
    tex = []
    end = 0
    while end < len(text):
        new_start, new_end = bibtex_find_start_endpoint(text, end)
        if new_start == -1:
            non_tex.append(text[end:])
            break
        else:
            non_tex.append(text[end:new_start])
        end = new_end
        block = text[new_start:end].strip()
        if pretty:
            mo = REGEX_BIBTEX_CITATION_KEY.search(block)
            if not mo:
                raise RuntimeError('this shouldnt be happening ever in extract_from_and_remove!')
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
                equal_tokens = line.split('=')
                if len(equal_tokens) == 2:
                    key, value = equal_tokens
                else:
                    key, value = equal_tokens[0], '='.join(equal_tokens[1:])
                lines.append((key.strip(), value.strip()))
            max_key_len = max(len(tpl[0]) for tpl in lines)
            fmt = '%s{:%ds} = {:}' % (' ' * indent, max_key_len)
            midsection = '\n'.join(fmt.format(key, value) if key else f'{" " * indent}{value}' for key, value in lines)
            block = f'{top_line}\n{midsection}\n{end_line}'  # prettified

        tex.append(block)
    return '\n'.join(tex), ''.join(non_tex)


def extract_from(text, pretty=True, indent=4):
    # type: (str, bool, int) -> str
    '''
    Description:
        given ANY text, find the relevant bibtex inside it.
    Returns:
        str
    '''
    return extract_from_and_remove(text, pretty=pretty, indent=indent)[0]


def get_label_citation(text, parse=True, pretty=True, indent=4, nulls=False, dedupe=False):
    # type: (str, bool, bool, int, bool, bool) -> dict
    '''
    Description:
        given ANY text, get a map of its keys to its citation text
    Arguments:
        parse: bool
            default True, assume not good bibtex at first
        nulls: bool
            default False, raise KeyError if a label is missing in a citation
        dedupe: bool
            default False, throws on duplicates
    Returns:
        dict
            key: bibtex citation
    '''
    if parse:
        text, _ = extract_from_and_remove(text, pretty=pretty, indent=indent)
    dupes = set()
    dick = {}

    prev_label = ''
    prev_start = 0
    mos = list(REGEX_BIBTEX_CITATION_KEY.finditer(text))
    for mo in mos:
        start = mo.start()
        groups = mo.groupdict()
        label = groups['label']  # typ = groups['type']

        if not label and not nulls:
            raise KeyError(f'could not determine label for {text[mo.start():mo.end()]!r}')
        if prev_label:
            if prev_label in dick:
                dupes.add(prev_label)
            dick[prev_label] = text[prev_start:start].rstrip()

        prev_start = start
        prev_label = label

    if prev_label in dick:
        dupes.add(prev_label)
    if dupes and not dedupe:
        raise ValueError(f'{len(dupes)} duplicate labels: {list(sorted(dupes))}')
    dick[prev_label] = text[prev_start:].rstrip()
    return dick
