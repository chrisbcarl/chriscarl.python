#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
Author:         Chris Carl
Email:          chrisbcarl@outlook.com
Date:           2026-01-24
Description:

chriscarl.core.functors.parse.markdown unit test.

Updates:
    2026-01-24 - tests.chriscarl.core.functors.parse.markdown - initial commit
'''

# stdlib imports (expected to work)
from __future__ import absolute_import, print_function, division, with_statement  # , unicode_literals
import os
import sys
import logging
import unittest

# third party imports

# project imports (expected to work)
from chriscarl.core import constants
from chriscarl.core.lib.stdlib.os import abspath
from chriscarl.core.lib.stdlib.unittest import UnitTest
from chriscarl.core.lib.stdlib.io import write_text_file

# test imports
import chriscarl.core.functors.parse.markdown as lib

SCRIPT_RELPATH = 'tests/chriscarl/core/functors/parse/test_markdown.py'
if not hasattr(sys, '_MEIPASS'):
    SCRIPT_FILEPATH = os.path.abspath(__file__)
else:
    SCRIPT_FILEPATH = os.path.abspath(os.path.join(sys._MEIPASS, SCRIPT_RELPATH))  # pylint: disable=no-member
SCRIPT_DIRPATH = os.path.dirname(SCRIPT_FILEPATH)
SCRIPT_NAME = os.path.splitext(os.path.basename(__file__))[0]
THIS_MODULE = sys.modules[__name__]
LOGGER = logging.getLogger(__name__)
LOGGER.addHandler(logging.NullHandler())

constants.fix_constants(lib)  # deal with namespace sharding the files across directories


class TestCase(UnitTest):

    def setUp(self):
        return super().setUp()

    def tearDown(self):
        return super().tearDown()

    # @unittest.skip('lorem ipsum')
    def test_case_0(self):
        table = '''
|a|b|
|--|---|
|hello||
||world|
'''
        variables = [
            (lib.table_to_rows, (table, ), dict(null=True)),
        ]
        controls = [
            [{
                'a': 'hello',
                'b': None
            }, {
                'a': None,
                'b': 'world'
            }],
        ]
        self.assert_null_hypothesis(variables, controls)

    def test_case_1(self):
        table_bad = '''
|a|b|
|--|---|
|hel|world|
'''
        table_pretty = '''|a  |b    |
|-- |---  |
|hel|world|'''

        variables = [
            (lib.table_prettify, (table_bad, )),
        ]
        controls = [
            table_pretty,
        ]
        self.assert_null_hypothesis(variables, controls)

    def test_case_2(self):
        table_bad = '''|col|col|col|
|---|---|---|
|a  |b  |a,b|'''
        table_pretty = '''|col|col|col|
|---|---|---|
|a  |b  |<ul><li>a</li><li>b</li></ul>|'''

        variables = [
            (lib.table_listified, (table_bad, )),
        ]
        controls = [
            table_pretty,
        ]
        self.assert_null_hypothesis(variables, controls)

    def test_case_3(self):
        md = '''![img](https://upload.wikimedia.org/wikipedia/commons/3/36/Chiesa_di_Santa_Maria_della_Pace_altare_Presentazione_al_tempio_Batoni_Brescia.jpg)
![img-local-doesnt-exist](./img.img)
'''

        md_filepath = abspath(self.tempdir, 'md.md')
        write_text_file(md_filepath, md)
        doclets, interdoc_labels, download_url_filepaths, errors, warnings = lib.markdown_to_doclets(md_filepath)
        print(doclets)
        print(interdoc_labels)
        print(download_url_filepaths)
        print(errors)
        print(warnings)

    def test_case_4(self):
        table0 = '''
|a|b|c|d|
|-:|:-|--|---|
|e|f|g|h|
|i|j|k|l|
'''
        pivot0 = '''|a|e|i|
|-:|:-|--|
|b|f|j|
|c|g|k|
|d|h|l|'''

        table1 = '''
|a|b|
|-:|:-|
|c|d|
|e|f|
|g|h|
'''
        pivot1 = '''|a|c|e|g|
|-:|:-|--|--|
|b|d|f|h|'''

        variables = [
            (lib.table_pivot, (table0, ), dict(pretty=False)),
            (lib.table_pivot, (table1, ), dict(pretty=False)),
        ]
        controls = [
            pivot0,
            pivot1,
        ]
        self.assert_null_hypothesis(variables, controls)

    def test_case_5(self):
        table0 = '''
|a|b|c|d|
|-:|:-|--|---|
|e|f|g|h|
|i|j|k|l|'''
        csv0 = '''a,b,c,d
e,f,g,h
i,j,k,l
'''
        table1 = '''
|a|b|
|-:|:-|--|---|
|e,f|g,h|
|i,j|k,l|'''
        csv1 = '''a,b
"e,f","g,h"
"i,j","k,l"
'''
        variables = [
            (lib.table_to_csv, (table0, )),
            (lib.table_to_csv, (table1, )),
        ]
        controls = [
            csv0,
            csv1,
        ]
        self.assert_null_hypothesis(variables, controls)


if __name__ == '__main__':
    tc = TestCase()
    tc.setUp()

    try:
        tc.test_case_0()
        tc.test_case_1()
        tc.test_case_2()
        tc.test_case_3()
        tc.test_case_4()
        tc.test_case_5()
    finally:
        tc.tearDown()
