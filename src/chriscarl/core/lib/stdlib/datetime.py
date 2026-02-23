#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
Author:         Chris Carl
Email:          chrisbcarl@outlook.com
Date:           2026-02-20
Description:

core.lib.stdlib.datetime is fast functions that are exactly what I want
core.lib are modules that contain code that is about (but does not modify) the library. somewhat referential to core.functor and core.types.

Updates:
    2026-02-22 - core.lib.stdlib.datetime - FIX: jesus christ its good we're testing this... added from_str
    2026-02-20 - core.lib.stdlib.datetime - initial commit

TODO:
    - timezone info, utc, etc.
'''

# stdlib imports
from __future__ import absolute_import, print_function, division, with_statement  # , unicode_literals
import os
import sys
import logging
import datetime

# third party imports

# project imports

SCRIPT_RELPATH = 'chriscarl/core/lib/stdlib/datetime.py'
if not hasattr(sys, '_MEIPASS'):
    SCRIPT_FILEPATH = os.path.abspath(__file__)
else:
    SCRIPT_FILEPATH = os.path.abspath(os.path.join(sys._MEIPASS, SCRIPT_RELPATH))  # pylint: disable=no-member
SCRIPT_DIRPATH = os.path.dirname(SCRIPT_FILEPATH)
SCRIPT_NAME = os.path.splitext(os.path.basename(__file__))[0]
THIS_MODULE = sys.modules[__name__]
LOGGER = logging.getLogger(__name__)
LOGGER.addHandler(logging.NullHandler())

NOW = datetime.datetime.now()


def get_start_of_week(now=NOW):
    # type: (datetime.datetime) -> datetime.datetime
    '''
    Description:
        Return a datetime whose date is the start of the week. (time not adjusted)
        https://stackoverflow.com/a/19216386
    Arguments:
        now: datetime.datetime
    Returns:
        datetime.datetime
    '''
    daynumber = now.weekday()
    start_of_week = now - datetime.timedelta(days=daynumber)
    return start_of_week


def get_start_of_day(now):
    # type: (datetime.datetime) -> datetime.datetime
    '''
    Description:
        Wipe out the time info.
    Arguments:
        now: datetime.datetime
    Returns:
        datetime.datetime
    '''
    return datetime.datetime(year=now.year, month=now.month, day=now.day)


def get_end_of_day(now):
    # type: (datetime.datetime) -> datetime.datetime
    '''
    Description:
        Set to the end of the day
    Arguments:
        now: datetime.datetime
    Returns:
        datetime.datetime
    '''
    return datetime.datetime(year=now.year, month=now.month, day=now.day, hour=23, minute=59, second=59, microsecond=999999)


DATETIME_FORMATS = [
    '%Y-%m-%d',
    '%Y-%m-%d %H:%M:%S',
    '%Y-%m-%d %H:%M:%S.%f',
    '%Y-%m-%d %H:%M',
]
# TODO: timezone info, utc, etc.
DATETIME_TZ_FORMATS = [
    # '%Y-%m-%dT%H:%M',
    # '%Y-%m-%dT%H:%M:%S',
    # '%Y-%m-%dT%H:%M:%S %z',
    # '%Y-%m-%d %H:%M:%S %z',
    # '%Y-%m-%dT%H:%M:%S.%f',
    # '%Y-%m-%dT%H:%M:%S.%f %z',
    # '%Y-%m-%d %H:%M:%S.%f %z',
]


def from_str(text):
    # type: (str) -> datetime.datetime|None
    for fmt in DATETIME_FORMATS + DATETIME_TZ_FORMATS:
        try:
            return datetime.datetime.strptime(text, fmt)
        except ValueError:
            pass

    return None
