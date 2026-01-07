#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
Author:         Chris Carl
Email:          chrisbcarl@outlook.com
Date:           2026-01-07
Description:

tools.lf is a tool that emulates dos2unix

Updates:
    2026-01-07 - tools.lf - initial commit
'''

# stdlib imports
from __future__ import absolute_import, print_function, division, with_statement  # , unicode_literals
import os
import sys
import logging
import re
from dataclasses import dataclass, field
from argparse import ArgumentParser
from typing import List

# third party imports

# project imports
from chriscarl.core.constants import TEMP_DIRPATH
from chriscarl.core.lib.stdlib.logging import NAME_TO_LEVEL, configure_ez
from chriscarl.core.lib.stdlib.argparse import ArgparseNiceFormat
from chriscarl.core.lib.stdlib.os import abspath, make_dirpath
from chriscarl.tools.shed.constants import IGNORED_DIRS

SCRIPT_RELPATH = 'chriscarl/tools/lf.py'
if not hasattr(sys, '_MEIPASS'):
    SCRIPT_FILEPATH = os.path.abspath(__file__)
else:
    SCRIPT_FILEPATH = os.path.abspath(os.path.join(sys._MEIPASS, SCRIPT_RELPATH))  # pylint: disable=no-member
SCRIPT_DIRPATH = os.path.dirname(SCRIPT_FILEPATH)
SCRIPT_NAME = os.path.splitext(os.path.basename(__file__))[0]
THIS_MODULE = sys.modules[__name__]
LOGGER = logging.getLogger(__name__)
LOGGER.addHandler(logging.NullHandler())

# argument defaults
DEFAULT_FIB_INIT = [0, 1]
DEFAULT_LOG_FILEPATH = abspath(TEMP_DIRPATH, 'tool.log')
DEFAULT_IGNORE = ['collateral']
DEFAULT_THRESHOLD = 0.95

# tool constants


@dataclass
class Arguments:
    '''
    Document this class with any specifics for the process function.
    '''
    dirpath: str = ''
    binary: bool = False
    threshold: float = DEFAULT_THRESHOLD
    ignore: List[str] = field(default_factory=lambda: DEFAULT_IGNORE)
    debug: bool = False
    log_level: str = 'INFO'
    log_filepath: str = DEFAULT_LOG_FILEPATH

    @staticmethod
    def argparser():
        # type: () -> ArgumentParser
        parser = ArgumentParser(prog=SCRIPT_NAME, description=__doc__, formatter_class=ArgparseNiceFormat)
        app = parser.add_argument_group('app')
        app.add_argument('dirpath', type=str, help='where to recurse on?')
        app.add_argument('--binary', action='store_true', help='look for occurances of the BYTES CRLF rather than than the unicode. much more dangerous')
        app.add_argument('--threshold', type=float, default=DEFAULT_THRESHOLD, help='chose to print debug info')
        app.add_argument('--ignore', type=str, nargs='*', default=DEFAULT_IGNORE, help='more dirs to ignore in addition to the usual')

        misc = parser.add_argument_group('misc')
        misc.add_argument('--debug', action='store_true', help='chose to print debug info')
        misc.add_argument('--log-level', type=str, default='INFO', choices=NAME_TO_LEVEL, help='log level?')
        misc.add_argument('--log-filepath', type=str, default=DEFAULT_LOG_FILEPATH, help='log filepath?')
        return parser

    def process(self):
        if self.debug:
            self.log_level = 'DEBUG'
        configure_ez(level=self.log_level, filepath=self.log_filepath)

    @staticmethod
    def from_argparser(parser):
        # type: (ArgumentParser) -> Arguments
        ns = parser.parse_args()
        arguments = Arguments(**(vars(ns)))
        arguments.process()
        return arguments


def main():
    # type: () -> int
    parser = Arguments.argparser()
    if len(sys.argv) == 1:
        parser.print_help()
        sys.exit(1)

    args = Arguments.from_argparser(parser)
    args.dirpath = abspath(args.dirpath)

    LOGGER.info('starting')
    filepaths = []
    for dirpath, _, filenames in os.walk(args.dirpath):
        dirtokens = dirpath.split(os.sep)
        if any(token in IGNORED_DIRS + args.ignore for token in dirtokens):
            continue
        for filename in filenames:
            filepath = abspath(dirpath, filename)
            filepaths.append(filepath)
    replacements = 0
    for f, filepath in enumerate(filepaths):
        if (f + 1 % 100) == 0:
            LOGGER.info('%0.2f%%', f / len(filepaths))
        if args.binary:
            raise NotImplementedError('havent tried yet...')
            with open(filepath, 'rb') as rb:
                content = r.read()
            # i = len(content) - 1
            # while i > 0:
            #     if content[i] == bytes('\n') and content[i - 1] == bytes('\n'):
            #         # get rid of that byte, etc.
        else:
            try:
                with open(filepath, 'r', encoding='utf-8') as r:
                    content = r.read()
                chars = len(content)
                if chars == 0:
                    continue
                # unichars = len([ord(char) > 255 for char in content])
                # if unichars / chars > args.threshold:
                LOGGER.debug(filepath)
                with open(filepath, 'w', encoding='utf-8') as w:
                    w.write(content.replace('\r\n', '\n'))

                replacements += 1
            except UnicodeDecodeError:
                continue

    LOGGER.info('made replacements in %d files!', replacements)
    return 0


if __name__ == '__main__':
    sys.exit(main())
