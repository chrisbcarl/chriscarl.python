#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
Author:         Chris Carl
Email:          chrisbcarl@outlook.com
Date:           2026-01-06
Description:

chriscarl.core.lib.stdlib.urllib unit test.

Updates:
    2026-01-06 - tests.chriscarl.core.lib.stdlib.urllib - initial commit
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
import chriscarl.core.lib.stdlib.urllib as lib

SCRIPT_RELPATH = 'tests/chriscarl/core/lib/stdlib/test_urllib.py'
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
        self.site_url0 = 'https://www.google.com'
        self.site_url1 = 'https://www.google.com/search'
        self.site_url2 = 'https://www.google.com/search/query?param1=value'

        self.file_url0 = 'https://samplefile.com/static/samples/document/txt/txt_sample_file_1MB.txt'
        self.file_url1 = 'https://google.com'
        self.file_url2 = 'https://upload.wikimedia.org/wikipedia/commons/a/ae/Cityvarvet_January_2022_10.jpg'
        return super().setUp()

    def tearDown(self):
        return super().tearDown()

    # @unittest.skip('lorem ipsum')
    def test_case_0(self):
        variables = [
            (lib.create_internet_shortcut, (self.site_url0, '/temp')),
            (lib.create_internet_shortcut, (self.site_url1, '/temp')),
            (lib.create_internet_shortcut, (self.site_url2, '/temp')),
        ]
        controls = [
            abspath('/temp/google.com.url'),
            abspath('/temp/search.url'),
            abspath('/temp/query.url'),
        ]
        self.assert_null_hypothesis(variables, controls)

    def test_case_1(self):
        variables = [
            (lib.get_basename, (self.site_url0)),
            (lib.get_basename, (self.site_url1)),
            (lib.get_basename, (self.site_url2)),
            (lib.get_filepath, (self.site_url0, '/temp'), dict(flat=True)),
            (lib.get_filepath, (self.site_url1, '/temp'), dict(flat=True)),
            (lib.get_filepath, (self.site_url2, '/temp'), dict(flat=True)),
            (lib.get_filepath, (self.site_url0, '/temp'), dict(flat=False)),
            (lib.get_filepath, (self.site_url1, '/temp'), dict(flat=False)),
            (lib.get_filepath, (self.site_url2, '/temp'), dict(flat=False)),
        ]
        controls = [
            'google.com',
            'search',
            'query',
            abspath('/temp/google.com'),
            abspath('/temp/search'),
            abspath('/temp/query'),
            abspath('/temp/google.com'),
            abspath('/temp/google.com/search'),
            abspath('/temp/google.com/search/query'),
        ]
        self.assert_null_hypothesis(variables, controls)

    def test_case_2(self):
        variables = [
            (lib.download, (self.file_url0, '/temp'), dict(flat=False)),
            (lib.download, (self.file_url1, '/temp'), dict(flat=False)),
        ]
        controls = [
            abspath('/temp/samplefile.com/static/samples/document/txt/txt_sample_file_1MB.txt'),
            abspath('/temp/google.com'),
        ]
        self.assert_null_hypothesis(variables, controls)

        res = lib.download_pool([self.file_url0, self.file_url1], '/temp', flat=False)
        variables = [
            (set, res),
        ]
        controls = [
            set(controls),
        ]
        self.assert_null_hypothesis(variables, controls)

        variables = [
            (lib.download_pool, ([self.file_url2], '/temp'), dict(flat=True)),
        ]
        controls = [
            [abspath('/temp/Cityvarvet_January_2022_10.jpg')],
        ]
        self.assert_null_hypothesis(variables, controls)


if __name__ == '__main__':
    tc = TestCase()
    tc.setUp()

    tc.test_case_0()
    tc.test_case_1()
    tc.test_case_2()

    tc.tearDown()
