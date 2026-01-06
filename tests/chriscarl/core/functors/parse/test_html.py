#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
Author:         Chris Carl
Email:          chrisbcarl@outlook.com
Date:           2026-01-06
Description:

chriscarl.core.functors.parse.html unit test.

Updates:
    2026-01-06 - tests.chriscarl.core.functors.parse.html - initial commit
'''

# stdlib imports (expected to work)
from __future__ import absolute_import, print_function, division, with_statement  # , unicode_literals
import os
import sys
import logging
import unittest

# third party imports

# project imports (expected to work)
from chriscarl.core.constants import TEST_COLLATERAL_DIRPATH
from chriscarl.core.lib.stdlib.os import abspath
from chriscarl.core.lib.stdlib.unittest import UnitTest

# test imports
import chriscarl.core.functors.parse.html as lib

SCRIPT_RELPATH = 'tests/chriscarl/core/functors/parse/test_html.py'
if not hasattr(sys, '_MEIPASS'):
    SCRIPT_FILEPATH = os.path.abspath(__file__)
else:
    SCRIPT_FILEPATH = os.path.abspath(os.path.join(sys._MEIPASS, SCRIPT_RELPATH))  # pylint: disable=no-member
SCRIPT_DIRPATH = os.path.dirname(SCRIPT_FILEPATH)
SCRIPT_NAME = os.path.splitext(os.path.basename(__file__))[0]
THIS_MODULE = sys.modules[__name__]
LOGGER = logging.getLogger(__name__)
LOGGER.addHandler(logging.NullHandler())


class TestCase(UnitTest):

    def setUp(self):
        self.flat_filepath = abspath(TEST_COLLATERAL_DIRPATH, 'flat.html')
        self.index_filepath = abspath(TEST_COLLATERAL_DIRPATH, 'index.html')

        with open(self.flat_filepath, 'r', encoding='utf-8') as r:
            self.flat = r.read()
        with open(self.index_filepath, 'r', encoding='utf-8') as r:
            self.index = r.read()
        return super().setUp()

    def tearDown(self):
        return super().tearDown()

    # @unittest.skip('lorem ipsum')
    def test_case_0_parse_ez(self):
        variables = [
            (isinstance, (lib.html_to_dom(self.flat_filepath).to_string(), str)),
            (isinstance, (lib.html_to_dom(self.flat_filepath), lib.Dom)),
            (isinstance, (lib.html_to_dom(self.flat), lib.Dom)),
            (isinstance, (lib.html_to_dom(self.index_filepath), lib.Dom)),
            (isinstance, (lib.html_to_dom(self.index), lib.Dom)),
        ]
        controls = [
            True,
            True,
            True,
            True,
            True,
        ]
        self.assert_null_hypothesis(variables, controls)

    def test_case_1_parse_flat(self):
        parser = lib.HtmlNestedParser()
        dom = parser.feed(self.flat)
        ele = dom.get_element_by_tag('li')

        variables = [
            (isinstance, (dom, lib.Dom)),
            (isinstance, (ele, lib.Node)),
            (len, dom.tags),
            (set, dom.tags),
        ]
        controls = [
            True,
            1,
            5,
            set(['h1', 'plz', 'p', 'a', 'li']),
        ]
        self.assert_null_hypothesis(variables, controls)

    def test_case_2_parse_flat(self):
        parser = lib.HtmlNestedParser()
        dom = parser.feed(self.index)
        ided = dom.get_element_by_id('id1')
        anchor = dom.get_element_by_tag('a')
        anchors = dom.get_elements_by_tag('a')
        list_items = dom.get_elements_by_tag('li')
        hidden_one = dom.get_element_by_class('hidden')
        hiddens = dom.get_elements_by_class('hidden')

        variables = [
            (isinstance, (ided, lib.Node)),
            (isinstance, (anchor, lib.Node)),
            (isinstance, (anchors, list)),
            (isinstance, (str(ided), str)),
            (len, anchors),
            (len, list_items),
            (isinstance, (hidden_one, lib.Node)),
            (len, hiddens),
            (dom.get_element_by_class, ('not-a-class'), dict(default=-1)),
            (dom.get_element_by_tag, ('not-a-tag'), dict(default=-1)),
        ]
        controls = [
            True,
            True,
            True,
            True,
            1,
            4,
            True,
            2,
            -1,
            -1,
        ]
        self.assert_null_hypothesis(variables, controls)


if __name__ == '__main__':
    tc = TestCase()
    tc.setUp()

    tc.test_case_0_parse_ez()
    tc.test_case_1_parse_flat()
    tc.test_case_2_parse_flat()

    tc.tearDown()
