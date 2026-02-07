#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
Author:         Chris Carl
Email:          chrisbcarl@outlook.com
Date:           2026-01-07
Description:

tools.fib is a tool which... really doesnt do much

Updates:
    2026-01-07 - tools.fib - initial commit  # FEATURE: tool-fib
'''

# stdlib imports
from __future__ import absolute_import, print_function, division, with_statement  # , unicode_literals
import os
import sys
import logging
from typing import List, Generator, Optional
from dataclasses import dataclass, field
from argparse import ArgumentParser

# third party imports

# project imports
from chriscarl.core.constants import TEMP_DIRPATH
from chriscarl.core.lib.stdlib.logging import NAME_TO_LEVEL, configure_ez
from chriscarl.core.lib.stdlib.argparse import ArgparseNiceFormat
from chriscarl.core.lib.stdlib.os import abspath, make_dirpath

SCRIPT_RELPATH = 'chriscarl/tools/fib.py'
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
DEFAULT_OUTPUT_DIRPATH = abspath(TEMP_DIRPATH, 'tool')
DEFAULT_LOG_FILEPATH = abspath(TEMP_DIRPATH, 'tool.log')

# tool constants


def fast_fib(n, debug=False, a=0, b=1):
    # type: (int, bool, int, int) -> Generator[int, None, None]
    if debug:
        LOGGER.debug('a = %s; b = %s', a, b)
    yield 0
    yield 1
    for i in range(3, n + 1):  # because we're calculating the 3rd number
        c = a + b
        if debug:
            LOGGER.debug('a = %s; b = %s; c = %s; i = %s', a, b, c, i)
        yield c
        a = b
        b = c
        if debug:
            LOGGER.debug('\tafter swapping c, b, a...')
            LOGGER.debug('\ta = %s; b = %s; c = %s; i = %s', a, b, c, i)
    if debug:
        LOGGER.debug('finished %s steps!', n)


@dataclass
class Arguments:
    '''
    Document this class with any specifics for the process function.
    '''
    n: int
    debug: bool
    times: int
    init: List[int] = field(default_factory=lambda: DEFAULT_FIB_INIT)
    output_dirpath: str = DEFAULT_OUTPUT_DIRPATH
    messages: List[str] = field(default_factory=lambda: [])
    log_level: str = 'INFO'
    log_filepath: str = DEFAULT_LOG_FILEPATH

    @classmethod
    def argparser(cls):
        # type: () -> ArgumentParser
        parser = ArgumentParser(prog=SCRIPT_NAME, description=__doc__, formatter_class=ArgparseNiceFormat)
        app = parser.add_argument_group('app')
        app.add_argument('n', type=int, help='the -th term of fib you want')
        app.add_argument('--times', '-t', type=lambda x: int(x, base=0), required=True, help='print how many times? any numerical format is ok')
        app.add_argument('--init', type=int, nargs=2, default=DEFAULT_FIB_INIT, help='assume sequence starts with these 2 numbers')

        misc = parser.add_argument_group('misc')
        misc.add_argument('--debug', action='store_true', help='chose to print debug info')
        misc.add_argument('--output-dirpath', '-o', type=str, default=DEFAULT_OUTPUT_DIRPATH, help='where do you want to save a text of the sequence')
        misc.add_argument('--messages', '-m', type=str, nargs='*', default=[], help='messages youd like to have printed')
        misc.add_argument('--log-level', type=str, default='INFO', choices=NAME_TO_LEVEL, help='log level?')
        misc.add_argument('--log-filepath', type=str, default=DEFAULT_LOG_FILEPATH, help='log filepath?')
        return parser

    def process(self):
        make_dirpath(self.output_dirpath)
        if self.debug:
            self.log_level = 'DEBUG'
        configure_ez(level=self.log_level, filepath=self.log_filepath)

    @classmethod
    def parse(parser=None, argv=None):
        # type: (Optional[ArgumentParser], Optional[List[str]]) -> Arguments
        parser = parser or cls.argparser()
        ns = parser.parse_args(argv)
        arguments = cls(**(vars(ns)))
        arguments.process()
        return arguments


def main():
    # type: () -> int
    parser = cls.argparser()
    if len(sys.argv) == 1:
        parser.print_help()
        sys.exit(1)

    args = Arguments.parse(parser=parser)
    numbers = []
    for fib in fast_fib(args.n, debug=args.debug, a=args.init[0], b=args.init[1]):
        numbers.append(fib)

    if args.debug:
        LOGGER.debug('numbers: %s', numbers)
    LOGGER.info(numbers[-1])

    if args.messages:
        with open(abspath(args.output_dirpath, 'out'), 'w', encoding='utf-8') as w:
            for i in range(args.times):
                for m, message in enumerate(args.messages):
                    LOGGER.info('%d - %d - %s', i, m, message)
                    # cannot use braces since this is a template, lol, such a headache
                    w.write(message + '\n')  # type: ignore

    LOGGER.info('fib: %s', fib)
    return fib


if __name__ == '__main__':
    sys.exit(main())
