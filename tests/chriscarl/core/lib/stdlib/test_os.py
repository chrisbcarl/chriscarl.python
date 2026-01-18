#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
Author:         Chris Carl
Email:          chrisbcarl@outlook.com
Date:           2024-11-26
Description:

chriscarl.core.lib.stdlib.os unit test.

Updates:
    2026-01-06 - tests.chriscarl.core.lib.stdlib.os - added is_file, is_dir
    2024-11-26 - tests.chriscarl.core.lib.stdlib.os - initial commit
'''

# stdlib imports (expected to work)
from __future__ import absolute_import, print_function, division, with_statement  # , unicode_literals
import os
import sys
import logging

# third party imports

# project imports (expected to work)
from chriscarl.core.lib.stdlib.unittest import UnitTest

# test imports
import chriscarl.core.lib.stdlib.os as lib

SCRIPT_RELPATH = 'tests/chriscarl/core/lib/stdlib/test_os.py'
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
        setUp = super().setUp()
        from chriscarl.core.lib.stdlib.io import write_text_file
        write_text_file('{}/a.txt'.format(self.tempdir), '')
        write_text_file('{}/a/b.txt'.format(self.tempdir), '')
        write_text_file('{}/a/b/c.txt'.format(self.tempdir), '')
        write_text_file('{}/a/b/c/d.txt'.format(self.tempdir), '')
        self.relpaths = [
            'a.txt',
            'a/b.txt',
            'a/b/c.txt',
            'a/b/c/d.txt',
        ]
        return setUp

    def tearDown(self):
        return super().tearDown()

    def test_case_0_abspath(self):
        variables = [
            (lib.abspath, ('/tmp', 'hello', 'world')),
            (lib.abspath, ('~/tmp', 'hello', 'world')),
        ]
        controls = [
            os.path.abspath('/tmp/hello/world'),
            os.path.abspath(os.path.expanduser('~/tmp/hello/world')),
        ]
        self.assert_null_hypothesis(variables, controls)

    def test_case_1_chdir(self):
        variables = [
            (lib.abspath, ('/tmp', 'hello', 'world')),
            (lib.abspath, ('~/tmp', 'hello', 'world')),
        ]
        controls = [
            os.path.abspath('/tmp/hello/world'),
            os.path.abspath(os.path.expanduser('~/tmp/hello/world')),
        ]
        self.assert_null_hypothesis(variables, controls)

    def test_case_2_walk(self):
        abspaths = [lib.abspath(self.tempdir, relfile) for relfile in self.relpaths]
        basenames = [os.path.basename(relfile) for relfile in self.relpaths]
        ignore_dirs = ['docs', 'ignoreme', 'node_modules', '.git', '__pycache__', 'build', 'dist', 'venv', '.venv', '.pytest_cache']
        extensions = ['.py']

        ignore = list(lib.walk('./', extensions=extensions, ignore=ignore_dirs, include=None))
        include = list(lib.walk('./', extensions=extensions, ignore=ignore_dirs, include=['src/', 'tests/']))

        variables = [
            (lib.walk, (self.tempdir, ), dict(extensions=['.txt'], relpath=True)),
            (lib.walk, (self.tempdir, ), dict(extensions=['.txt'], basename=True)),
            (lib.walk, (self.tempdir, ), dict(extensions=['.txt'])),
            (lib.walk, ('./', ), dict(extensions=extensions, ignore=ignore_dirs, include=None)),
            (lib.walk, ('./', ), dict(extensions=extensions, ignore=ignore_dirs, include=['src/', 'tests/'])),
        ]
        controls = [
            self.relpaths,
            basenames,
            abspaths,
            include,
            ignore,
        ]
        self.assert_null_hypothesis(variables, controls)

    def test_case_3_drives(self):
        if sys.platform == 'win32':
            drives = lib.drives()
            current_drive = lib.current_drive()
            self.assertIn('c', drives)
            self.assertIn(current_drive, drives)

    def test_case_4_as_posix(self):
        variables = [
            (lib.as_posix, ('/temp', ), dict(wsl=False)),
        ]
        controls = [
            '/temp',
        ]
        if sys.platform == 'win32':
            variables += [
                (lib.as_posix, ('C:\\temp', ), dict(wsl=False)),
                (lib.as_posix, ('C:\\temp', ), dict(wsl=True)),
            ]
            controls += [
                '/temp',
                '/mnt/c/temp',
            ]
        self.assert_null_hypothesis(variables, controls)

    def test_case_5_as_posix_win32(self):
        if sys.platform == 'win32':
            drives = lib.drives()
            current_drive = lib.current_drive()
            other_drives = [drive for drive in drives if drive != current_drive]
            with lib.chdir('/'):
                for other_drive in other_drives:
                    try:
                        os.chdir('{}:'.format(other_drive))
                    except OSError:
                        continue
                    variables = [
                        (lib.as_posix, ('C:\\temp', ), dict(wsl=False)),
                        (lib.as_posix, ('\\temp', ), dict(wsl=True)),
                    ]
                    controls = [
                        'C:/temp',
                        '/mnt/{}/temp'.format(other_drive),
                    ]
                    self.assert_null_hypothesis(variables, controls)

    def test_case_6_easy(self):
        if sys.platform == 'win32':
            variables = [
                (lib.is_file, (__file__), dict()),
                (lib.is_dir, (SCRIPT_DIRPATH), dict()),
                (lib.is_file, (__file__ + 'X'), dict()),
                (lib.is_dir, (SCRIPT_DIRPATH + 'X'), dict()),
            ]
            controls = [
                True,
                True,
                False,
                False,
            ]
        self.assert_null_hypothesis(variables, controls)


if __name__ == '__main__':
    tc = TestCase()
    tc.setUp()

    tc.test_case_0_abspath()
    tc.test_case_1_chdir()
    tc.test_case_2_walk()
    tc.test_case_3_drives()
    tc.test_case_4_as_posix()
    tc.test_case_5_as_posix_win32()
    tc.test_case_6_easy()

    tc.tearDown()
