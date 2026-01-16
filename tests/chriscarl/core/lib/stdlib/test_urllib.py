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
import subprocess
import urllib.error

# third party imports

# project imports (expected to work)
from chriscarl.core import constants
from chriscarl.core.lib.stdlib.os import abspath, as_posix
from chriscarl.core.lib.stdlib.unittest import UnitTest

# test imports
import chriscarl.core.lib.stdlib.urllib as lib
from chriscarl.core.lib.stdlib.io import read_text_file
from chriscarl.core.lib.stdlib.subprocess import kill
from chriscarl.core.lib.stdlib import http

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

        self.server = subprocess.Popen([sys.executable, '-m', http.__name__])
        self.server_url = f'http://{http.HOSTNAME}:{http.PORT}'
        return super().setUp()

    def tearDown(self):
        self.server.kill()
        kill(self.server.pid)
        return super().tearDown()

    # @unittest.skip('lorem ipsum')
    def test_case_0(self):
        variables = [
            (lib.create_internet_shortcut, (self.site_url0, ), dict(dirpath='/temp')),
            (lib.create_internet_shortcut, (self.site_url1, ), dict(dirpath='/temp')),
            (lib.create_internet_shortcut, (self.site_url2, ), dict(dirpath='/temp')),
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
            (lib.get_filepath, (self.site_url0, ), dict(dirpath='/temp', flat=True)),
            (lib.get_filepath, (self.site_url1, ), dict(dirpath='/temp', flat=True)),
            (lib.get_filepath, (self.site_url2, ), dict(dirpath='/temp', flat=True)),
            (lib.get_filepath, (self.site_url0, ), dict(dirpath='/temp', flat=False)),
            (lib.get_filepath, (self.site_url1, ), dict(dirpath='/temp', flat=False)),
            (lib.get_filepath, (self.site_url2, ), dict(dirpath='/temp', flat=False)),
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
        tpl0 = lib.download(self.file_url0, dirpath='/temp', flat=False)
        tpl1 = lib.download(self.file_url1, dirpath='/temp', flat=False)
        variables = [
            (lambda x: x[0], (tpl0, )),
            (lambda x: x[0], (tpl1, )),
        ]
        controls = [
            abspath('/temp/samplefile.com/static/samples/document/txt/txt_sample_file_1MB.txt'),
            abspath('/temp/google.com'),
        ]
        self.assert_null_hypothesis(variables, controls)

        res, failures = lib.download_pool([self.file_url0, self.file_url1], dirpath='/temp', flat=False)
        variables = [
            (set, res),
            (int, failures),
        ]
        controls = [
            set(controls),
            0,
        ]
        self.assert_null_hypothesis(variables, controls)

        variables = [
            (lib.download_pool, ([self.file_url2], ), dict(dirpath='/temp', flat=True)),
        ]
        controls = [
            ([abspath('/temp/Cityvarvet_January_2022_10.jpg')], 0),  # 0 failures
        ]
        self.assert_null_hypothesis(variables, controls)

        this_file_uri = f'file:///{__file__}'
        this_file_content = read_text_file(__file__)
        variables = [
            (lib.download, (this_file_uri, ), dict(flat=True, as_body=True)),
        ]
        controls = [
            (this_file_content, this_file_uri),
        ]
        self.assert_null_hypothesis(variables, controls)

    def test_case_3(self):
        res = lib.download(self.server_url, as_body=True)
        variables = [
            (lambda x: x[0], (res, )),
        ]
        controls = [
            '<p>hello, world!</p>',
        ]
        self.assert_null_hypothesis(variables, controls)

        # all return same response
        args = (self.server_url, {'hello': 'world'})
        kwargs = dict(headers={'hello': 'world'}, context=lib.SSL_BASIC_CTX)
        response_post = lib.post(*args, **kwargs)
        response_put = lib.put(*args, **kwargs)
        response_delete = lib.delete(*args, **kwargs)

        self.assertEqual(response_post.json['payload'], response_post.json['payload'])
        self.assertEqual(response_post.json['payload'], response_put.json['payload'])
        self.assertEqual(response_post.json['payload'], response_delete.json['payload'])

        # not the same response
        args = (self.server_url, {'hello': 'world'})
        kwargs = dict(headers={'hello': 'world'})
        response_options = lib.options(*args, **kwargs)
        self.assertTrue(response_post != response_options)

        # all not implemented - code 501
        self.assertRaises(urllib.error.HTTPError, lib.patch, *args, **kwargs)
        self.assertRaises(urllib.error.HTTPError, lib.head, *args, **kwargs)


if __name__ == '__main__':
    tc = TestCase()
    tc.setUp()

    # tc.test_case_0()
    # tc.test_case_1()
    # tc.test_case_2()
    tc.test_case_3()

    tc.tearDown()
