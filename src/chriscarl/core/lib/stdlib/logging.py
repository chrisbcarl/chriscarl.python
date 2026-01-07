#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
Author:         Chris Carl
Email:          chrisbcarl@outlook.com
Date:           2024-11-26
Description:

core.lib.stdlib.logging is one of the most pivotal libraries and largely informs how its shadow module counterpart is implemented
core.lib are modules that contain code that is about (but does not modify) the library. somewhat referential to core.functor and core.types.

Updates:
    2024-12-20 - core.lib.stdlib.logging - FIX:  the padding actually expands correctly
    2024-12-09 - core.lib.stdlib.logging - added configure, level_to_int, levels_to_ints, SuccinctFormatter, ConsoleConfig, FileConfig (this is the big one)
    2024-12-08 - core.lib.stdlib.logging - added Logger_makeRecord, SuccinctFormatter
    2024-11-26 - core.lib.stdlib.logging - initial commit

Notes:
    https://docs.python.org/3/library/logging.html#logrecord-attributes
        '%(name)-12s: %(levelname)-8s %(message)s'
        '%(asctime)s %(name)-12s %(levelname)-8s %(message)s'
        '%(asctime)s %(name)s %(levelname)s %(message)s'
        '%(asctime)s %(processName)-10s %(name)s %(levelname)-8s %(message)s'
        '%(asctime)s %(name)-15s %(levelname)-8s %(processName)-10s %(message)s'
        '%(asctime)-15s %(clientip)s %(user)-8s %(message)s'
        '%(relativeCreated)6d %(threadName)s %(message)s'
        '%(relativeCreated)5d %(name)-15s %(levelname)-8s %(message)s'
        '%(levelname)s %(asctime)s %(module)s %(process)d %(thread)d %(message)s'
        '%(asctime)s - %(levelname)-8s - %(filename)-16s - %(funcName)-16s - %(lineno)-4d - %(message)s'
        '%(asctime)s - %(levelname)10s - %(filename)s - %(funcName)s - %(message)s'
'''

# stdlib imports
from __future__ import absolute_import, print_function, division, with_statement  # , unicode_literals
import __main__
import os
import sys
import logging
import datetime
import functools
import logging.handlers
from dataclasses import dataclass
from typing import Union, Callable, List, Optional, Type
from types import ModuleType

# third party imports
from six import string_types, integer_types

# project imports
import chriscarl
from chriscarl.core.constants import CWD
from chriscarl.core.types.list import as_list
from chriscarl.core.types.iterable import contains
from chriscarl.core.types.str import size_to_bytes
from chriscarl.core.lib.stdlib.io import MODES
from chriscarl.core.lib.stdlib.os import abspath, make_file_dirpath, TEMP_DIRPATH

SCRIPT_RELPATH = 'chriscarl/core/lib/stdlib/logging.py'
if not hasattr(sys, '_MEIPASS'):
    SCRIPT_FILEPATH = os.path.abspath(__file__)
else:
    SCRIPT_FILEPATH = os.path.abspath(os.path.join(sys._MEIPASS, SCRIPT_RELPATH))  # pylint: disable=no-member
SCRIPT_DIRPATH = os.path.dirname(SCRIPT_FILEPATH)
SCRIPT_NAME = os.path.splitext(os.path.basename(__file__))[0]
THIS_MODULE = sys.modules[__name__]
LOGGER = logging.getLogger(__name__)
LOGGER.addHandler(logging.NullHandler())

if sys.version_info[0] == 2:
    NAME_TO_LEVEL = logging._levelNames
else:
    NAME_TO_LEVEL = logging._nameToLevel
LEVEL_TO_NAME = {v: k for k, v in NAME_TO_LEVEL.items()}
BASIC_FORMAT = '%(asctime)s - %(message)s'
NICE_FOR_USERS_FORMAT = '%(asctime)s - %(levelname)s - %(message)s'
DEFAULT_FORMAT = '%(levelname)s - %(name)s, line %(lineno)d - %(asctime)s: %(message)s'
BARE_FORMAT = '%(levelname)-10s - %(asctime)s - %(name)s, line %(lineno)d: %(message)s'
DEV_FORMAT = '%(asctime)s %(levelname)10s - %(filename)32s, line %(lineno)d: %(message)s'
ESSENTIAL_FORMAT = '%(levelname)-10s - %(asctime)s - %(name)s, %(funcName)s, line: %(lineno)d - %(message)s '
ESSENTIAL_FORMAT2 = '%(levelname)-10s - %(asctime)s - "%(pathname)s", line: %(lineno)d - %(message)s '
VERBOSE_FORMAT = '%(levelname)s - %(processName)s - %(process)d %(funcName)s, line %(lineno)d - %(asctime)s: %(message)s'
DEFAULT_RIGID_FORMAT = '%(levelname)-10s - %(name)48s, line %(lineno)-4d - %(asctime)s: %(message)s'
VERBOSE_RIGID_FORMAT = '%(levelname)-10s - %(processName)-32s - pid: %(process)6d %(funcName)48s, line %(lineno)-4d - %(asctime)s: %(message)s'
VERBOSE_CSV_DEFAULT_FORMAT = '"%(levelname)s","%(processName)s","%(process)d","%(funcName)s","%(name)s","%(lineno)d","%(asctime)s","%(message)s"'
CSV_DEFAULT_FORMAT = '"%(levelname)s","%(name)s","%(lineno)d","%(asctime)s","%(message)s"'
MULTIPROCESS_DEFAULT_FORMAT = '%(levelname)-10s - %(processName)-32s - pid: %(process)6d - %(funcName)48s, line %(lineno)-4d - %(asctime)s: %(message)s'
THREADING_DEFAULT_FORMAT = '%(levelname)-10s - %(threadName)-32s - pid: %(process)6d - %(funcName)48s, line %(lineno)-4d - %(asctime)s: %(message)s'
PIPE_LOGFORMAT = (
    '| %(asctime)s | %(levelname)10s | %(name)48s | %(processName)16s | %(process)6d | %(message)s '
    '| %(pathname)s, line %(lineno)d'
    # '| %(name)32s | %(pathname)s, line %(lineno)-6d | %(message)s'
    # '| %(name)48s | %(funcName)32s(), line %(lineno)6d | %(message)s | %(pathname)s'
    # '%(name)s.%(funcName)s, line %(lineno)d: %(message)s'
)
PIPE_THREAD_LOGFORMAT = (
    '| %(asctime)s | %(levelname)10s | %(name)48s | %(threadName)16s | %(process)6d | %(message)s '
    '| %(pathname)s, line %(lineno)d'
    # '| %(name)32s | %(pathname)s, line %(lineno)-6d | %(message)s'
    # '| %(name)48s | %(funcName)32s(), line %(lineno)6d | %(message)s | %(pathname)s'
    # '%(name)s.%(funcName)s, line %(lineno)d: %(message)s'
)
EVERYTHING_FORMAT = (
    '%(asctime)s: | %(levelname)10s | thread %(thread)6d-%(threadName)-64s process %(process)6d-%(processName)-64s | '
    # '%(name)64s %(module)64s.%(funcName)-64s | line %(lineno)6d | %(message)s'
    '%(name)64s | %(module)64s | %(funcName)-64s | line %(lineno)6d | %(message)s'
)
TIMED_ROTATING_WHEN = ['S', 'M', 'H', 'D', 'midnight']
TIMED_ROTATING_WHEN += ['W{}'.format(__d) for __d in range(7)]


def get_log_func_from_level(log_level='DEBUG'):
    # type: (Union[str, int]) -> Callable
    if isinstance(log_level, str):
        log_level_int = logging._nameToLevel.get(log_level, 1)
        if log_level_int != 1:
            return getattr(logging, log_level.lower())
    else:
        log_level_int = log_level
    log = functools.partial(logging.log, log_level_int)
    return log


def level_to_int(level):
    # type: (Union[str, int]) -> int
    '''
    Description:
        WARNING -> 30
    '''
    if isinstance(level, int):
        return level
    contains(NAME_TO_LEVEL, level, exc=True)
    return NAME_TO_LEVEL.get(level, -1)


def levels_to_ints(levels):
    # type: (List[Union[str, int]]) -> List[int]
    '''
    Description:
        [10, INFO, WARNING, 50] -> [10, 20, 30, 50]
    '''
    int_levels = []
    for level in levels:
        if isinstance(level, int):
            int_levels.append(level)
        else:
            contains(NAME_TO_LEVEL, level, exc=True)
            int_levels.append(NAME_TO_LEVEL.get(level, -1))
    return int_levels


def Logger_makeRecord(self, name, level, fn, lno, msg, args, exc_info, func=None, extra=None, sinfo=None, **kwargs):
    '''
    Description:
        makeRecord is a default function definition but it limits which keys are modifiable in the extra dict.
        set logging.Logger.makeRecord = Logger_makeRecord to see the fruits of this change.
    '''
    # "C:/Python27/lib/logging/__init__.py", line 1270
    # "C:/Python36/lib/logging/__init__.py", line 1406
    if sys.version_info[0] == 2:
        rv = logging.LogRecord(name, level, fn, lno, msg, args, exc_info, func)
    else:
        rv = logging._logRecordFactory(name, level, fn, lno, msg, args, exc_info, func, sinfo)
    if extra is not None:
        for key in extra:
            # THIS is the behavior I want to disable--you can modify ANY key in the extra dict, including the "sacred" message / asctime
            # if (key in ['message', 'asctime']) or (key in rv.__dict__):
            #     raise KeyError('Attempt to overwrite %r in LogRecord' % key)
            rv.__dict__[key] = extra[key]
    return rv


class SuccinctFormatter(logging.Formatter):
    '''
    Description:
        inspired by https://flask.palletsprojects.com/en/2.1.x/logging/#injecting-request-information
        see https://docs.python.org/3/library/logging.html#logrecord-attributes
        it basically creates a new format field called "debug_info"
            depending on the mode it makes that debug info long or short
        some of the nice features:
            - if long filepaths are found, it extends all other logs after this one to space out based on that last length

    Arguments:
        mode: int
            0 - default:
                asctime - level - relpath, lineno: message
            1 - verbose:
                asctime - level - top_module: filepath, lineno: message
            2 - all:
                asctime - level - thread/proc - filepath, lineno: message
    '''
    _MODES = ['default', 'verbose', 'all']
    mode = 'default'
    _mode = 0
    _fmt_provided = False
    BASE_FORMAT = ('%(asctime)s - %(levelname){len_level_name}s - %(debug_info){len_debug_info}s: %(message)s')
    len_level_name = 5  # grows
    len_debug_info = 16  # grows

    def __init__(self, fmt=None, datefmt=None, style='%', validate=True, mode='default'):
        if mode not in self.__class__._MODES:
            raise ValueError('provided mode {!r} not in {}!'.format(mode, self.__class__._MODES))
        self.mode = mode
        self._mode = self.__class__._MODES.index(mode)
        self._fmt_provided = False
        self.len_level_name = self.__class__.len_level_name
        self.len_debug_info = self.__class__.len_debug_info

        if isinstance(fmt, string_types):
            self._fmt_provided = True
        else:
            fmt = self.__class__.BASE_FORMAT.format(len_level_name=self.len_level_name, len_debug_info=self.len_debug_info)
        if sys.version_info[0] == 3 and sys.version_info[1] >= 8:
            super(SuccinctFormatter, self).__init__(fmt=fmt, datefmt=datefmt, style=style, validate=validate)
        else:
            super(SuccinctFormatter, self).__init__(fmt=fmt, datefmt=datefmt)

    def change_mode(self, mode):
        # type: (Union[str, int]) -> None
        if isinstance(mode, integer_types):
            if mode >= len(self.__class__._MODES):
                raise ValueError('only have {} modes, provided {} exceeds!'.format(len(self.__class__._MODES), mode))
            self._mode = mode
            self.mode = self.__class__._MODES[mode]
        elif isinstance(mode, string_types):
            if mode not in self.__class__._MODES:
                raise ValueError('provided mode {!r} not in {}!'.format(mode, self.__class__._MODES))
            self.mode = mode
            self._mode = self.__class__._MODES.index(mode)
        else:
            raise TypeError('mode must be of type {}, provided {}!'.format(Union[str, int], type(mode)))

    def format(self, record):
        # type: (logging.LogRecord) -> str
        if self._fmt_provided:
            return super(SuccinctFormatter, self).format(record)

        len_changed = False
        if len(record.levelname) > self.len_level_name:
            self.len_level_name = len(record.levelname)
            len_changed = True

        if self._mode == 0:  # default
            relpath = os.path.relpath(record.pathname, CWD)
            debug_info = '"{:s}", line {:d}'.format(relpath, record.lineno)
        elif self._mode == 1:  # verbose
            top_module = record.name.split('.')[0]
            debug_info = '<{:s}>"{:s}", line {:d}'.format(top_module, record.pathname, record.lineno)
        elif self._mode == 2:  # all
            debug_info = 'p{:s}({:s})/t{:s}({:s}) - "{:s}", line {:d}'.format(
                str(record.process), record.processName, str(record.thread), record.threadName, record.pathname, record.lineno
            )
        setattr(record, 'debug_info', debug_info)

        if len(debug_info) > self.len_debug_info:
            self.len_debug_info = len(debug_info)
            len_changed = True

        if len_changed:
            fmt = self.__class__.BASE_FORMAT.format(len_level_name=self.len_level_name, len_debug_info=self.len_debug_info)
            self._fmt = fmt
            self._style._fmt = fmt  # NOTE: its actually the Style object that does the formatting in python 3+

        return super(SuccinctFormatter, self).format(record)


DEFAULT_FORMATTER = SuccinctFormatter()


@dataclass
class ConsoleConfig:
    level: Union[str, int] = logging.INFO
    format: str = ''
    formatter: logging.Formatter = DEFAULT_FORMATTER
    propagate: bool = True

    def __post_init__(self):
        if isinstance(self.format, string_types) and self.format:
            self.formatter = logging.Formatter(fmt=self.format)

    def set_handle(self, handle):
        # type: (logging.Handler) -> None
        handle.setFormatter(self.formatter)
        handle.setLevel(self.level)
        handle.propagate = self.propagate

    def get_handle(self):
        # type: () -> Type[logging.StreamHandler]
        handle = logging.StreamHandler(sys.stdout)
        self.set_handle(handle)
        return handle


DEFAULT_CONSOLE_CONFIG = ConsoleConfig(level=logging.INFO, format='', formatter=DEFAULT_FORMATTER, propagate=False)
DEFAULT_FILEPATH = abspath(TEMP_DIRPATH, 'log.log')


@dataclass
class FileConfig(ConsoleConfig):
    filepath: str = DEFAULT_FILEPATH
    mode: str = 'a'
    size: float = -1
    backups: int = 3
    when: Optional[str] = None
    atTime: Optional[datetime.time] = None
    interval: int = 1

    def __post_init__(self):
        super().__post_init__()
        contains(MODES, self.mode, exc=True)
        if isinstance(self.when, str):
            contains(TIMED_ROTATING_WHEN, self.when, exc=True)
        make_file_dirpath(self.filepath)
        self.size = self.size if isinstance(self.size, (int, float)) else size_to_bytes(self.size, into='b')

    def set_handle(self, handle):
        # type: (logging.FileHandler) -> None
        handle.setFormatter(self.formatter)
        handle.setLevel(self.level)
        handle.propagate = self.propagate

    def get_handle(self):
        # type: () -> Type[logging.FileHandler]
        if isinstance(self.when, str):
            handle = logging.handlers.TimedRotatingFileHandler(self.filepath, when=self.when, atTime=self.atTime, interval=self.interval, backupCount=self.backups)
            self.set_handle(handle)
            return handle
        else:
            if self.size <= 0:
                handle = logging.FileHandler(self.filepath, mode=self.mode)  # pylint: disable=no-member
                self.set_handle(handle)
                return handle
            else:
                handle = logging.handlers.RotatingFileHandler(self.filepath, mode=self.mode, maxBytes=self.size, backupCount=self.backups)
                self.set_handle(handle)
                return handle


DEFAULT_FILE_CONFIG = FileConfig(level=logging.INFO, format='', formatter=DEFAULT_FORMATTER, propagate=False, filepath=DEFAULT_FILEPATH)
DEFAULT_CONFIGS = [DEFAULT_CONSOLE_CONFIG, DEFAULT_FILE_CONFIG]
DEFAULT_LOGGERS = [chriscarl.__name__, __main__.__name__]


def loggers_from_names_modules_or_loggers(names_modules_or_loggers=None):
    # type: (Optional[List[Union[str, ModuleType, logging.Logger]]]) -> List[logging.Logger]
    loggers = []
    names_modules_or_loggers = as_list(names_modules_or_loggers or DEFAULT_LOGGERS, List[Union[str, ModuleType, logging.Logger]])
    for obj in names_modules_or_loggers:
        if isinstance(obj, logging.Logger):
            loggers.append(obj)
        elif isinstance(obj, ModuleType):
            loggers.append(logging.getLogger(obj.__name__))
        else:
            loggers.append(logging.getLogger(obj))
    return loggers


def configure(names=None, configs=DEFAULT_CONFIGS):
    # type: (Optional[List[Union[str, ModuleType, logging.Logger]]], List[ConsoleConfig]) -> List[logging.Logger]
    '''
    Description:
        set up loggers (one per module) that all follow the same configuration

    Arguments:
        names: List[Union[str, ModuleType, logging.Logger]]
            provide a mix of log names, modules, or loggers, or singular
        console: ConsoleConfig
            how the console is going to be set up for the above names, modules, or loggers
        file: FileConfig
            how the file is going to be set up for the above names, modules, or loggers

    Returns:
        List[logging.Logger]
            logger objects you can use by themselves
    '''
    loggers = loggers_from_names_modules_or_loggers(names_modules_or_loggers=names)
    lowest_level = min(levels_to_ints([config.level for config in configs]))
    for config in configs:
        hndl = config.get_handle()
        for logger in loggers:
            logger.propagate = config.propagate
            # if a handler of the same type already exists on this logger, just modify that one
            add_handler = True
            for handle in logger.handlers:
                if type(hndl) is type(handle):
                    config.set_handle(handle)
                    add_handler = False
            if add_handler:
                logger.handlers.append(hndl)
            logger.setLevel(lowest_level)
    return loggers


def configure_ez(names=None, level='INFO', filepath='', fmt='', file_level='', console_level=''):
    # type: (Optional[List[Union[str, ModuleType, logging.Logger]]], str, str, str, str, str) -> List[logging.Logger]
    configs = []  # type: List[ConsoleConfig]
    if filepath:
        fc = FileConfig(level=file_level or level, format=fmt, formatter=DEFAULT_FORMATTER, propagate=False, filepath=filepath)
        configs.append(fc)
    cc = ConsoleConfig(level=console_level or level, format=fmt, formatter=DEFAULT_FORMATTER, propagate=False)
    configs.append(cc)
    return configure(names=names, configs=configs)
