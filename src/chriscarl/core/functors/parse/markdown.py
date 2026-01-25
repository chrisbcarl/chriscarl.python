#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
Author:         Chris Carl
Email:          chrisbcarl@outlook.com
Date:           2026-01-24
Description:

core.functors.parse.markdown is functors that can work with markdown text directly rather than relying on something external.
core.functor are modules that functions that are usually defined as lambdas, but i like to hold onto them as named funcs. non-self-referential, low-import, etc.

Updates:
    2026-01-24 - core.functors.parse.markdown - initial commit
'''

# stdlib imports
from __future__ import absolute_import, print_function, division, with_statement  # , unicode_literals
import os
import sys
import logging

# third party imports

# project imports

SCRIPT_RELPATH = 'chriscarl/core/functors/parse/markdown.py'
if not hasattr(sys, '_MEIPASS'):
    SCRIPT_FILEPATH = os.path.abspath(__file__)
else:
    SCRIPT_FILEPATH = os.path.abspath(os.path.join(sys._MEIPASS, SCRIPT_RELPATH))  # pylint: disable=no-member
SCRIPT_DIRPATH = os.path.dirname(SCRIPT_FILEPATH)
SCRIPT_NAME = os.path.splitext(os.path.basename(__file__))[0]
THIS_MODULE = sys.modules[__name__]
LOGGER = logging.getLogger(__name__)
LOGGER.addHandler(logging.NullHandler())


def table_prettify(table_text):
    # type: (str) -> str
    table_text = table_text.strip()
    if not table_text.startswith('|') or not table_text.endswith('|'):
        raise ValueError('probably invalid markdown table! could not detect either the start pipe or end pipe!')

    rows = []
    maxlen = -1
    lines = table_text.splitlines()
    for line in lines:
        row = []
        for col in line.strip()[1:-1].split('|'):  # avoid the end pipes, split on the mid pipes
            col = col.strip()
            row.append(col)
            maxlen = max([maxlen, len(col)])
        rows.append(row)

    fmt = '{:%ss}' % maxlen
    out = '\n'.join(f'|{"|".join(fmt.format(r) for r in row)}|' for row in rows)
    return out
