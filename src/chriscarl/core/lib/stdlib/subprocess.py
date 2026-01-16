#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
Author:         Chris Carl
Email:          chrisbcarl@outlook.com
Date:           2024-11-25
Description:

core.lib.stdlib.subprocess is mostly wrappers around handling subprocesses.
core.lib are modules that contain code that is about (but does not modify) the library. somewhat referential to core.functor and core.types.

Updates:
    2026-01-16 - core.lib.stdlib.subprocess - added kill
    2024-11-27 - core.lib.stdlib.subprocess - added run and launch_editor
    2024-11-25 - core.lib.stdlib.subprocess - initial commit
'''

# stdlib imports
from __future__ import absolute_import, print_function, division, with_statement  # , unicode_literals
import os
import sys
import logging
import tempfile
import subprocess
from typing import Union, List, Optional, Tuple

# third party imports

# project imports
from chriscarl.core.lib.stdlib.io import read_text_file

SCRIPT_RELPATH = 'chriscarl/core/lib/stdlib/subprocess.py'
if not hasattr(sys, '_MEIPASS'):
    SCRIPT_FILEPATH = os.path.abspath(__file__)
else:
    SCRIPT_FILEPATH = os.path.abspath(os.path.join(sys._MEIPASS, SCRIPT_RELPATH))  # pylint: disable=no-member
SCRIPT_DIRPATH = os.path.dirname(SCRIPT_FILEPATH)
SCRIPT_NAME = os.path.splitext(os.path.basename(__file__))[0]
THIS_MODULE = sys.modules[__name__]
LOGGER = logging.getLogger(__name__)
LOGGER.addHandler(logging.NullHandler())


def run(cmd, cwd=None):
    # type: (Union[str, List[str]], Optional[str]) -> Tuple[int, str]
    fd, stdout = tempfile.mkstemp()
    os.close(fd)
    fd, stdin = tempfile.mkstemp()
    os.close(fd)
    with open(stdout, 'w', encoding='utf-8') as out, open(stdin, 'r', encoding='utf-8') as in_:
        exit_code = subprocess.Popen(cmd, stdout=out, stderr=out, stdin=in_, shell=True, cwd=cwd, universal_newlines=True).wait()
    output = read_text_file(stdout)
    return exit_code, output


def launch_editor(filepath):
    # https://stackoverflow.com/questions/39453951/open-file-at-specific-line-in-vscode
    # TODO: code --goto "<filepath>:<linenumber>:<x-coordinates>"
    subprocess.Popen(['code', '--goto', filepath], shell=True)


def kill(pid):
    # type: (int) -> int
    if sys.platform == 'win32':
        exit_code = subprocess.Popen(['taskkill', '/pid', str(pid), '/f', '/t'], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL).wait()
    else:
        exit_code = subprocess.Popen(['kill', str(pid), '-9'], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL).wait()
    return exit_code
