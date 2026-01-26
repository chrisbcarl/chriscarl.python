#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
Author:         Chris Carl
Email:          chrisbcarl@outlook.com
Date:           2026-01-09
Description:

core.functors.parse.str is general string parsing
core.functor are modules that functions that are usually defined as lambdas, but i like to hold onto them as named funcs. non-self-referential, low-import, etc.

Updates:
    2026-01-25 - core.functors.parse.str - added unicode_replace
    2026-01-09 - core.functors.parse.str - initial commit
'''

# stdlib imports
from __future__ import absolute_import, print_function, division, with_statement  # , unicode_literals
import os
import sys
import logging
import re
import json
from typing import Generator, Any, Dict

# third party imports

# project imports
from chriscarl.core.lib.stdlib.typing import isinstance_raise

SCRIPT_RELPATH = 'chriscarl/core/functors/parse/str.py'
if not hasattr(sys, '_MEIPASS'):
    SCRIPT_FILEPATH = os.path.abspath(__file__)
else:
    SCRIPT_FILEPATH = os.path.abspath(os.path.join(sys._MEIPASS, SCRIPT_RELPATH))  # pylint: disable=no-member
SCRIPT_DIRPATH = os.path.dirname(SCRIPT_FILEPATH)
SCRIPT_NAME = os.path.splitext(os.path.basename(__file__))[0]
THIS_MODULE = sys.modules[__name__]
LOGGER = logging.getLogger(__name__)
LOGGER.addHandler(logging.NullHandler())


def parenthesis_extract(text, open_char='{', close_char='}'):
    # type: (str, str, str) -> str
    '''
    Description:
        classic DSA problem involving a stack to solve
        >>> parentehsis_extract('what is (beauty)?', open_char='(', close_char=')')
        ... '(beauty)'

    Arguments:
        text: str
        open_char: str
        close_char: str

    Returns:
        str
            whatever is in between the open and closed chars (inclusive)
    '''
    start = end = text.find(open_char)
    stack = [text[end]]
    end += 1
    while stack:
        char = text[end]
        if char == open_char:  # '{'
            stack.insert(0, char)
        elif char == close_char:  # '}'
            stack.pop(0)
        end += 1
    return text[start:end]


def lines_to_dict(text):
    # type: (str) -> Dict[str, str]
    '''
    Description:
        Take text that looks like
            hello
            world
        And get back
            {'hello': 'world'}

    Arguments:
        text: str

    Returns:
        dict
    '''
    key = None
    value = None
    dick = {}
    key_or_value = True  # False is key, True is value
    for line in text.splitlines():
        line = line.strip()
        if line:
            key_or_value ^= True  # flip it
            if key_or_value:  # its a value
                value = line
            else:
                key = line
        if key_or_value and key and value:
            dick[key] = value
            key = None
            value = None

    return dick


def lines_to_headers(text):
    # type: (str) -> Dict[str, str]
    '''
    Description:
        Edge and Chrome do this thing where you have to copy headers as new lines. Really annoying.

    Arguments:
        text: str

    Returns:
        dict
    '''
    headers = lines_to_dict(text)
    delme = [key for key in headers if key.startswith(':')]
    for key in delme:
        del headers[key]
    return headers


def get_dict_values_by_text_key(key, text):
    # type: (str, str) -> Generator[Any, None, None]
    '''
    Description:
        Say you have a deeply nested dict, or that it changes
        "data": {
            "xdt_api__v1__clips__home__connection_v2": {
                "edges": [
                    {
                        "node": {
                            "media": {
                                "__typename": "XDTMediaDict",
                                "code": "DSXE9dOif6E",
                                "friendship_status": {
                                    "following": false,
                                    "is_feed_favorite": false
                                },

        wouldnt it be nice to just ask for "friendship_status"?
        Always returns a list since we could find multiple keys.

    Arguments:
        key: str
        text: str
            the actual text .json or whatever, not the object

    Returns:
        Generator[Any, None, None]
    '''

    isinstance_raise(text, str)
    for mo in re.finditer(rf'"{key}":\s+', text):
        res = parenthesis_extract('{' + text[mo.start():], open_char='{', close_char='}')
        data = json.loads(res)
        yield data[key]


def get_dict_value_by_text_key(key, text, default=None):
    # type: (str, str, Any) -> Any
    for value in get_dict_values_by_text_key(key, text):
        return value
    return default


UNICODES = {
    '​': '',
    '’': "'",
    '–': '--',
    '−': '-',  # this is actually distinct from the one directly above...
}


def unicode_replace(content):
    # type: (str) -> str
    for uni, ascii in UNICODES.items():
        content = content.replace(uni, ascii)
    return content
