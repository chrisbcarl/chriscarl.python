#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
Author:         Chris Carl
Email:          chrisbcarl@outlook.com
Date:           2026-01-09
Description:

tools.str is a tool which manipulates strings as a service or as a oneoff

Updates:
    2026-01-09 - tools.str - initial commit
'''

# stdlib imports
from __future__ import absolute_import, print_function, division, with_statement  # , unicode_literals
import os
import sys
import logging
import time
import json
from typing import List, Generator, Optional, Callable
from dataclasses import dataclass, field
from argparse import ArgumentParser, _SubParsersAction

# third party imports

# project imports
from chriscarl.core.constants import TEMP_DIRPATH
from chriscarl.core.lib.stdlib.logging import NAME_TO_LEVEL, configure_ez
from chriscarl.core.lib.stdlib.argparse import ArgparseNiceFormat
from chriscarl.core.lib.stdlib.os import abspath, make_dirpath
from chriscarl.core.lib.stdlib.io import read_text_file, write_text_file
import chriscarl.core.functors.parse.str as str_lib

SCRIPT_RELPATH = 'chriscarl/tools/str.py'
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
DEFAULT_OUTPUT_DIRPATH = abspath(TEMP_DIRPATH, 'tools.str')
DEFAULT_LOG_FILEPATH = abspath(TEMP_DIRPATH, 'tools.str.log')

# tool constants
FUNC_FILEPATHS = {
    str_lib.lines_to_dict: {
        'inp': abspath(DEFAULT_OUTPUT_DIRPATH, 'lines_to_dict', 'input.txt'),
        'out': abspath(DEFAULT_OUTPUT_DIRPATH, 'lines_to_dict', 'output.json'),
    },
    str_lib.lines_to_headers: {
        'inp': abspath(DEFAULT_OUTPUT_DIRPATH, 'lines_to_headers', 'input.txt'),
        'out': abspath(DEFAULT_OUTPUT_DIRPATH, 'lines_to_headers', 'output.json'),
    }
}


def service():
    '''
    Description:
        Run all funcs in a loop until ctrl+c

    Returns:
        None
    '''
    last_modified_inputs = {}
    for func, filemap in FUNC_FILEPATHS.items():
        last_modified_inputs[func] = os.stat(filemap['inp']).st_mtime
        LOGGER.info('%r input:  "%s"', func.__name__, filemap['inp'])
        LOGGER.info('%r output: "%s"', func.__name__, filemap['out'])

    while True:
        try:
            modified = {func: os.stat(filemap['inp']).st_mtime for func, filemap in FUNC_FILEPATHS.items()}
            for func, mtime in modified.items():
                if last_modified_inputs[func] != mtime:
                    inp = FUNC_FILEPATHS[func]['inp']
                    out = FUNC_FILEPATHS[func]['out']
                    LOGGER.info('%r @ "%s" modified! running function...', func.__name__, inp)
                    read = read_text_file(inp)
                    write = func(read)
                    if isinstance(write, dict):
                        with open(out, 'w', encoding='utf-8') as w:
                            json.dump(write, w, indent=2)
                    else:
                        write_text_file(out, write)
                    last_modified_inputs[func] = mtime
            time.sleep(0.25)
        except KeyboardInterrupt:
            LOGGER.info('ctrl + c detected!')
            break


@dataclass
class Arguments:
    '''
    Document this class with any specifics for the process function.
    '''
    func: Callable = service
    input_filepath: str = DEFAULT_OUTPUT_DIRPATH
    output_filepath: str = DEFAULT_OUTPUT_DIRPATH
    # messages: List[str] = field(default_factory=lambda: [])
    debug: bool = False
    log_level: str = 'INFO'
    log_filepath: str = DEFAULT_LOG_FILEPATH

    @staticmethod
    def add_command(parser, func):
        # type: (_SubParsersAction, Callable) -> ArgumentParser
        mode = parser.add_parser(func.__name__, help=func.__doc__)
        mode.set_defaults(func=func)

        # common_group = mode.add_argument_group('app')
        mode.add_argument('input-filepath', '-i', type=str, default=FUNC_FILEPATHS[func]['inp'], help='input filepath?')
        mode.add_argument('--output-filepath', '-o', type=str, default=FUNC_FILEPATHS[func]['out'], help='output filepath?')

        # common_group = mode.add_argument_group('debug')
        mode.add_argument('--debug', action='store_true', help='chose to print debug info')
        mode.add_argument('--log-level', type=str, default='INFO', choices=NAME_TO_LEVEL, help='log level?')
        mode.add_argument('--log-filepath', type=str, default=DEFAULT_LOG_FILEPATH, help='log filepath?')

        return mode

    @staticmethod
    def argparser():
        # type: () -> ArgumentParser
        example_mode = 'lines_to_headers'

        parser = ArgumentParser(prog=SCRIPT_NAME, description=__doc__, formatter_class=ArgparseNiceFormat)
        modes = parser.add_subparsers(help='which mode do you want? run "{} {} -h" to get help on the {!r} mode'.format(SCRIPT_NAME, example_mode, example_mode))

        service_mode = modes.add_parser(service.__name__, help=service.__doc__)
        # common_group = service_mode.add_argument_group('debug')
        service_mode.add_argument('--debug', action='store_true', help='chose to print debug info')
        service_mode.add_argument('--log-level', type=str, default='INFO', choices=NAME_TO_LEVEL, help='log level?')
        service_mode.add_argument('--log-filepath', type=str, default=DEFAULT_LOG_FILEPATH, help='log filepath?')

        Arguments.add_command(modes, str_lib.lines_to_dict)
        Arguments.add_command(modes, str_lib.lines_to_headers)

        return parser

    def process(self):
        for filemap in FUNC_FILEPATHS.values():
            for filepath in filemap.values():
                make_dirpath(os.path.dirname(filepath))
                if not os.path.isfile(filepath):
                    write_text_file(filepath, '')
        if self.debug:
            self.log_level = 'DEBUG'
        configure_ez(level=self.log_level, filepath=self.log_filepath)

    @staticmethod
    def parse(parser=None, argv=None):
        # type: (Optional[ArgumentParser], Optional[List[str]]) -> Arguments
        parser = parser or Arguments.argparser()
        ns = parser.parse_args(argv)
        arguments = Arguments(**(vars(ns)))
        arguments.process()
        return arguments


def main():
    # type: () -> int
    parser = Arguments.argparser()
    if len(sys.argv) == 1:
        parser.print_help()
        sys.exit(1)

    args = Arguments.parse(parser=parser)

    LOGGER.info('beginning %r', args.func.__name__)
    if args.func == service:
        args.func()
    else:
        read = read_text_file(args.input_filepath)
        write = args.func(read)
        write_text_file(args.output_filepath, write)

    return 0


if __name__ == '__main__':
    sys.exit(main())
