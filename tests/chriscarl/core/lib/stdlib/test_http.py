#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
Author:         Chris Carl
Email:          chrisbcarl@outlook.com
Date:           2026-01-16
Description:

chriscarl.core.lib.stdlib.http unit test.

Updates:
    2026-01-16 - tests.chriscarl.core.lib.stdlib.http - initial commit
'''

# stdlib imports (expected to work)
from __future__ import absolute_import, print_function, division, with_statement  # , unicode_literals
import os
import sys
import logging
import unittest
import subprocess

# third party imports

# project imports (expected to work)
from chriscarl.core import constants
from chriscarl.core.lib.stdlib.os import abspath
from chriscarl.core.lib.stdlib.unittest import UnitTest

# test imports
import chriscarl.core.lib.stdlib.http as lib
from chriscarl.core.lib.stdlib.subprocess import kill
from chriscarl.core.lib.stdlib.urllib import download

SCRIPT_RELPATH = 'tests/chriscarl/core/lib/stdlib/test_http.py'
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
        self.server = subprocess.Popen([sys.executable, '-m', lib.__name__])
        self.url = f'http://{lib.HOSTNAME}:{lib.PORT}'
        return super().setUp()

    def tearDown(self):
        self.server.kill()
        kill(self.server.pid)
        return super().tearDown()

    # @unittest.skip('lorem ipsum')
    def test_case_0_download_root(self):
        res = download(self.url, as_body=True)
        variables = [
            (lambda x: x[0], (res, )),
        ]
        controls = [
            '<p>hello, world!</p>',
        ]
        self.assert_null_hypothesis(variables, controls)


if __name__ == '__main__':
    tc = TestCase()
    tc.setUp()

    tc.test_case_0_download_root()

    tc.tearDown()
