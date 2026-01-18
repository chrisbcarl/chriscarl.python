#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
Author:         Chris Carl
Email:          chrisbcarl@chriscarl.com
Date:           2024-11-24
Description:

core.lib.stdlib.io is all about basic input/output operations
core.lib are modules that contain code that is about (but does not modify) the library. somewhat referential to core.functor and core.types.

Updates:
    2026-01-17 - core.lib.stdlib.io - BUG: fixed write_text_file to always use LF by default
    2026-01-07 - core.lib.stdlib.io - added read_text_file_try
    2024-11-24 - core.lib.stdlib.io - initial commit
'''

# stdlib imports
from __future__ import absolute_import, print_function, division, with_statement  # , unicode_literals
import os
import sys
import logging
import locale
from typing import List

# third party imports

# project imports
from chriscarl.core.lib.stdlib.os import make_file_dirpath

SCRIPT_RELPATH = 'chriscarl/core/lib/stdlib/io.py'
if not hasattr(sys, '_MEIPASS'):
    SCRIPT_FILEPATH = os.path.abspath(__file__)
else:
    SCRIPT_FILEPATH = os.path.abspath(os.path.join(sys._MEIPASS, SCRIPT_RELPATH))  # pylint: disable=no-member
SCRIPT_DIRPATH = os.path.dirname(SCRIPT_FILEPATH)
SCRIPT_NAME = os.path.splitext(os.path.basename(__file__))[0]
THIS_MODULE = sys.modules[__name__]
LOGGER = logging.getLogger(__name__)
LOGGER.addHandler(logging.NullHandler())

MODES = ['r', 'w', 'a', 'rb', 'wb', 'ab']
MODES += ['{}+'.format(__mode) for __mode in MODES]
ENCODINGS_TYPICAL = [sys.getfilesystemencoding(), locale.getpreferredencoding(), 'iso-8859-1']  # utf-8, cp1252, latin-1


def read_text_file(filepath, encoding='utf-8'):
    # type: (str, str) -> str
    try:
        with open(filepath, 'r', encoding=encoding) as r:
            return r.read()
    except UnicodeDecodeError as ude:
        raise UnicodeDecodeError(ude.encoding, ude.object, ude.start, ude.end, '"{}" reason: {}'.format(filepath, ude.reason)) from ude


def read_text_file_try(filepath, encodings=ENCODINGS_TYPICAL):
    # type: (str, List[str]) -> str
    # https://stackoverflow.com/a/36316351
    for e, encoding in enumerate(encodings):
        try:
            with open(filepath, 'r', encoding=encoding) as r:
                return r.read()
        except UnicodeDecodeError as ude:
            if e + 1 == len(encodings):
                raise UnicodeDecodeError(ude.encoding, ude.object, ude.start, ude.end, '"{}" reason: {}'.format(filepath, ude.reason)) from ude
    return ''


def read_bytes_file(filepath):
    # type: (str) -> bytes
    with open(filepath, 'rb') as rb:
        return rb.read()


def write_text_file(filepath, content, encoding='utf-8', newline='\n'):
    # type: (str, str, str, str) -> int
    make_file_dirpath(filepath)
    with open(filepath, 'w', encoding=encoding, newline=newline) as w:
        return w.write(content)


def write_bytes_file(filepath, content):
    # type: (str, bytes) -> int
    make_file_dirpath(filepath)
    with open(filepath, 'wb') as wb:
        return wb.write(content)
