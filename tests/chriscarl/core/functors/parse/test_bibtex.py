#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
Author:         Chris Carl
Email:          chrisbcarl@outlook.com
Date:           2026-01-25
Description:

chriscarl.core.functors.parse.bibtex unit test.

Updates:
    2026-01-25 - tests.chriscarl.core.functors.parse.bibtex - initial commit
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

# test imports
import chriscarl.core.functors.parse.bibtex as lib

SCRIPT_RELPATH = 'tests/chriscarl/core/functors/parse/test_bibtex.py'
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
        self.bibtex_good_ugly_key = 'CitekeyArticle'
        self.bibtex_good_ugly = r'''@article{CitekeyArticle,
  author   = "P. J. Cohen",
  title    = "The independence of the continuum hypothesis",
  journal  = "\url{Proceedings of the National Academy of Sciences}",
  year     = 1963,
  volume   = "50",
  number   = "6",
  pages    = "1143--1148",
}'''
        self.bibtex_good_small_key = 'no-idea-what-this-is'
        self.bibtex_good_small = r'''@article{no-idea-what-this-is,
    author = "P. J. Cohen", % inline comment
    year   = 2025,
    % keycomment
}'''
        self.bibtex_null = r'''@article{
  pages    = "1143--1148",
}'''
        return super().setUp()

    def tearDown(self):
        return super().tearDown()

    def test_case_0(self):
        non_bibtex0 = '\nabc\n\n'
        non_bibtex1 = '\n\ndef\n'
        variables = [
            (lib.extract_from_and_remove, (non_bibtex0 + self.bibtex_good_ugly + non_bibtex1, ), dict(pretty=False)),
            (lib.extract_from, (self.bibtex_good_ugly, ), dict(pretty=False)),
            (lib.get_labels, (self.bibtex_good_ugly, )),
            (lib.get_labels, (self.bibtex_null, )),
        ]
        controls = [
            (self.bibtex_good_ugly, non_bibtex0 + non_bibtex1),
            self.bibtex_good_ugly,
            {
                'CitekeyArticle': 'article'
            },
            KeyError,
        ]
        self.assert_null_hypothesis(variables, controls)

    def test_case_1(self):
        bibtex = r'''@article{no-idea-what-this-is,
  author   = "P. J. Cohen", % inline comment
  year = 2025,
  % keycomment
}@book{Different,
  date = "someother", % another inline
  year   = 2026,
  % different key
}
'''
        bibtex_good = r'''@article{no-idea-what-this-is,
    author = "P. J. Cohen", % inline comment
    year   = 2025,
    % keycomment
}
@book{Different,
    date = "someother", % another inline
    year = 2026,
    % different key
}
'''
        variables = [
            (lib.extract_from, (bibtex, ), dict(pretty=True)),
        ]
        controls = [
            bibtex_good.strip(),
        ]
        self.assert_null_hypothesis(variables, controls)

    def test_case_2(self):
        two = f'{self.bibtex_good_ugly}\n{self.bibtex_good_small}'
        duped = f'{self.bibtex_good_small}\n{self.bibtex_good_small}'
        variables = [
            (lib.get_label_citation, (self.bibtex_null, ), dict(pretty=False)),
            (lib.get_label_citation, (two, ), dict(pretty=False)),
            (lib.get_label_citation, (self.bibtex_good_small, ), dict(pretty=False)),
            (lib.get_label_citation, (duped, ), dict(pretty=False)),
            (lib.get_label_citation, (duped, ), dict(pretty=False, dedupe=True)),
        ]
        controls = [
            KeyError,
            {
                self.bibtex_good_ugly_key: self.bibtex_good_ugly,
                self.bibtex_good_small_key: self.bibtex_good_small,
            },
            {
                self.bibtex_good_small_key: self.bibtex_good_small
            },
            ValueError,
            {
                self.bibtex_good_small_key: self.bibtex_good_small
            },
        ]
        self.assert_null_hypothesis(variables, controls)


if __name__ == '__main__':
    tc = TestCase()
    tc.setUp()

    try:
        tc.test_case_0()
        tc.test_case_1()
        tc.test_case_2()
    finally:
        tc.tearDown()
