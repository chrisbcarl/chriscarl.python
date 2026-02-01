#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
Author:         Chris Carl
Email:          chrisbcarl@outlook.com
Date:           2026-01-06
Description:

core.functors.parse.html is all about parsing html
core.functor are modules that functions that are usually defined as lambdas, but i like to hold onto them as named funcs. non-self-referential, low-import, etc.

Updates:
    2026-01-31 - core.functors.parse.html - added html5
    2026-01-29 - core.functors.parse.html - added list_to_html
                 core.functors.parse.html - surprised the tests didnt pick it up, i'll need to get more summarized rather than verbosified
    2026-01-24 - core.functors.parse.html - annotations were still wrong?
    2026-01-19 - core.functors.parse.html - much needed type annotations
    2026-01-07 - core.functors.parse.html - quality of life functions added to classes, get_attr
    2026-01-06 - core.functors.parse.html - BUG: fixed where it would omit large portions of the html, turns out the logic was missing the sibling, the else was important
    2026-01-06 - core.functors.parse.html - initial commit
'''

# stdlib imports
from __future__ import absolute_import, print_function, division, with_statement  # , unicode_literals
import os
import sys
import logging
from html.parser import HTMLParser as _HTMLParser
# from html.entities import name2codepoint
from typing import Callable, Optional, List, Dict, Any
import functools

# third party imports

# project imports
from chriscarl.core.lib.stdlib.io import read_text_file_try
from chriscarl.core.lib.stdlib.os import is_file
from chriscarl.core.lib.stdlib.typing import isinstance_raise
from chriscarl.core.types.list import rows_to_str_rows

SCRIPT_RELPATH = 'chriscarl/core/functors/parse/html.py'
if not hasattr(sys, '_MEIPASS'):
    SCRIPT_FILEPATH = os.path.abspath(__file__)
else:
    SCRIPT_FILEPATH = os.path.abspath(os.path.join(sys._MEIPASS, SCRIPT_RELPATH))  # pylint: disable=no-member
SCRIPT_DIRPATH = os.path.dirname(SCRIPT_FILEPATH)
SCRIPT_NAME = os.path.splitext(os.path.basename(__file__))[0]
THIS_MODULE = sys.modules[__name__]
LOGGER = logging.getLogger(__name__)
LOGGER.addHandler(logging.NullHandler())


class Node():
    '''
    # TODO: a node can have a child embedded inside its own data
        so maybe make data a list, then you can interleave the children inside the data if it makes sense
        <p>Learn more at <a href="whatev">this</a> link</p>
            data: Learn more at  this
    '''
    tag = ''
    attrs = {}
    data = ''
    children = []
    parent = None

    def __init__(self, tag, attrs=None, data='', children=None, parent=None):
        self.tag = tag
        self.attrs = attrs or {}
        self.data = data
        self.children = children or []
        self.parent = parent

    def __repr__(self):
        attrs = ' '.join(f'{k}="{v}"' for k, v in self.attrs.items())
        return f'<{self.tag}{" " + attrs if attrs else ""}>{self.data}</{self.tag}>'

    def __str__(self):
        return repr(self)

    def to_string(self, depth=0):
        tokens = [' ' * depth * 4 + repr(self)]
        for child in self.children:
            tokens.append(child.to_string(depth=depth + 1))
        return '\n'.join(tokens)


class Dom():
    '''
    # FEATURE: html-parser
    '''
    nodes = []  # type: List[Node]
    ids = {}  # type: Dict[str, Node]
    classes = {}  # type: Dict[str, List[Node]]
    tags = {}  # type: Dict[str, List[Node]]

    @classmethod
    def from_html(cls, html):
        # type: (str) -> Dom
        return html_to_dom(html)

    def __init__(self, nodes):
        self.nodes = nodes
        self.ids = {}
        self.classes = {}
        self.tags = {}
        self.discover()

    def to_string(self):
        # type: () -> str
        return '\n'.join(node.to_string(depth=0) for node in self.nodes)

    def iterate_level_order(self, functor):
        # type: (Callable[[Node], None]) -> None
        queue = list(self.nodes)
        while queue:
            node = queue.pop(0)
            functor(node)
            for child in node.children:
                queue.append(child)

    def discover(self):
        # type: () -> None

        def discover_node(node):
            if node.tag not in self.tags:
                self.tags[node.tag] = []
            self.tags[node.tag].append(node)
            if 'id' in node.attrs:
                self.ids[node.attrs['id']] = node
            if 'class' in node.attrs:
                if node.attrs['class'] not in self.classes:
                    self.classes[node.attrs['class']] = []
                self.classes[node.attrs['class']].append(node)
                if ' ' in node.attrs['class']:
                    for classs in node.attrs['class'].split(' '):
                        if classs not in self.classes:
                            self.classes[classs] = []
                        self.classes[classs].append(node)

        self.iterate_level_order(discover_node)

    def get_element_by_id(self, id_, default=None):
        # type: (str, Optional[Any]) -> Node | Any
        return self.ids.get(id_, default)

    def get_element_by_class(self, classs, default=None):
        # type: (str, Optional[Any]) -> Node | Any
        lst = self.classes.get(classs, [])
        if lst:
            return lst[0]
        return default

    def get_element_by_tag(self, tag, default=None):
        # type: (str, Optional[Any]) -> Node | Any
        lst = self.tags.get(tag, [])
        if lst:
            return lst[0]
        return default

    def get_elements_by_class(self, classs):
        # type: (str, Optional[Any]) -> List[Node]
        return self.classes.get(classs, [])

    def get_elements_by_tag(self, tag):
        # type: (str, Optional[Any]) -> List[Node]
        return self.tags.get(tag, [])

    def get_attr(self, attr, default=None):
        # type: (str, Optional[Any]) -> List[str]
        lst = []
        self.iterate_level_order(lambda node: lst.append(node.attrs.get(attr, default)))
        return [ele for ele in lst if ele]


class HtmlNestedParser(_HTMLParser):
    # https://docs.python.org/3/library/html.parser.html
    stack = []
    dom = None  # type: Optional[Dom]

    def parse(self, html):
        # type: (str, str) -> Dom
        return html_to_dom(html)

    def feed(self, data):
        # type: (str) -> None
        stack = self.stack = []
        super().feed(data)
        # import pprint
        # pprint.pprint(stack, indent=4, width=160)
        tag = ''
        root = node = Node(tag='', children=[], attrs={}, data='', parent=None)
        while stack:
            meta, data = stack.pop(-1)
            if meta == 'start':
                new = Node(tag=data, children=[], attrs={}, data='', parent=node)
                if data != tag:
                    # we're nesting
                    node.children.append(new)
                    node = new
                    tag = data
                else:
                    # we're sibling
                    node.parent.children.append(new)
                    node = new
            elif meta == 'attrs':
                node.attrs = data
            elif meta == 'data':
                node.data += data
            elif meta == 'end':
                if node:
                    node = node.parent

        # # remaining node is the root
        self.dom = Dom(root.children)

    def handle_data(self, data):
        '''
        .goahead() order
            handle_data
            starttag
            endtag
            comment
            pi
            htmldec
            charref
            entityref
        '''
        if data.strip():
            self.stack.insert(0, ('data', data))

    def handle_starttag(self, tag, attrs):
        '''
        starttag calls endtag
        '''
        attrs = dict(attrs)
        self.stack.insert(0, ('start', tag))
        self.stack.insert(0, ('attrs', attrs))

    def handle_endtag(self, tag):
        self.stack.insert(0, ('end', tag))

    # TODO: deal and trigger the following
    # def handle_comment(self, data):
    #     self.stack.insert(0, ('comment', data))

    # def handle_entityref(self, name):
    #     c = chr(name2codepoint[name])
    #     print("Named ent:", c)
    #     raise NotImplementedError('entityref')

    # def handle_charref(self, name):
    #     if name.startswith('x'):
    #         c = chr(int(name[1:], 16))
    #     else:
    #         c = chr(int(name))
    #     print("Num ent  :", c)
    #     raise NotImplementedError('charref')

    # def handle_decl(self, data):
    #     # DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 3.2 Final//EN"
    #     # print("Decl     :", data)
    #     # raise NotImplementedError('decl')
    #     pass


def html_to_dom(text):
    # type: (str) -> Dom
    parser = HtmlNestedParser()
    if is_file(text):
        text = read_text_file_try(text)
    parser.feed(text)
    if parser.dom is None:
        raise RuntimeError('could not parse html to Dom!')
    return parser.dom


def list_to_html(lst, ordered=False, minify=True, indent=4):
    # type: (list, bool, bool, int) -> str
    '''
    Description
        ['a', 'b'] => <ul><li>a</li><li>b</li></ul>
    Arguments:
        ordered: bool
            make the lists ordered lists?
        minifiy: bool
            default False
        indent: int
            default 4
    Returns:
        str
    '''
    isinstance_raise(lst, list)
    tokens = ['<ol>' if ordered else '<ul>']
    for ele in lst:
        tokens.append(f'<li>{ele}</li>')
    tokens.append('</ol>' if ordered else '</ul>')
    if minify:
        return ''.join(tokens)

    inner = "\n".join(f"{' ' * indent}{tok}" for tok in tokens[1:-1])
    return f'{tokens[0]}\n{inner}\n{tokens[-1]}'


HTML_TEMPLATE_TH = '        <th scope="col" style="text-align: {aligned};">{cell}</th>'
HTML_TEMPLATE_TR = '''        <tr>
{td}
        </tr>'''
HTML_TEMPLATE_TD = '            <td style="text-align: {aligned};">{cell}</td>'
HTML_TEMPLATE_TABLE = '''<table>
    <thead>
{ths}
    </thead>
    <tbody>
{trs}
    </tbody>
</table>'''

def rows_to_html(rows, aligned='left', ordered=False, minify=True, indent=4):
    # type: (List[dict], str, bool, bool, int) -> str
    '''
    Description
        [{'abcdefg': 'xyz'}] => <table>
            <thead>
                <th scope="col" style="text-align: left;">abcdefg</th>
            </thead>
            <tbody>
                <tr>
                    <td style="text-align: left;">xyz</td>
                </tr>
            </tbody>
        </table>
    Arguments:
        rows: List[dict]
            typical list of dicts
        aligned: str
            default left, right, center
        ordered: bool
            make the lists ordered lists?
        minifiy: bool
            default False
        indent: int
            default 4
    Returns:
        str
    '''
    on_list = functools.partial(list_to_html, ordered=ordered, minify=minify, indent=indent)
    row_strs, headers, _ = rows_to_str_rows(rows, on_list=on_list)

    ths = '\n'.join(HTML_TEMPLATE_TH.format(aligned=aligned, cell=cell) for cell in headers)
    trs = []
    for row_str in row_strs:
        trs.append(HTML_TEMPLATE_TR.format(td="\n".join(HTML_TEMPLATE_TD.format(aligned=aligned, cell=cell) for cell in row_str.values())))

    render = HTML_TEMPLATE_TABLE.format(ths=ths, trs='\n'.join(trs))
    return render

HTML5_TEMPLATE = '''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Document</title>
</head>
<body>
{content}
</body>
</html>'''

def html5(html):
    # type: (str) -> str
    '''
    Description:
        Given a string like '<h1>Header</h1>', wrap it around real html...
    Returns:
        str
    '''
    return HTML5_TEMPLATE.format(content=html)
