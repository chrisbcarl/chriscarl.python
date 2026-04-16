#!/usr/bin/env python
# -*- coding: utf-8 -*-
r'''
Author:         Chris Carl
Email:          chrisbcarl@outlook.com
Date:           2026-04-13
Description:

core.operating_systems.concurrency is my way of understanding concurrency from a typical operating systems class perspective.
core are modules that define the bedrock from which other things do import. non-self-referential, low-import, etc.

Updates:
    2026-04-13 - core.operating_systems.concurrency - peterson
'''

# stdlib imports
from __future__ import absolute_import, print_function, division, with_statement  # , unicode_literals
import os
import sys
import logging
import threading
import time

# third party imports

# project imports

SCRIPT_RELPATH = 'chriscarl/core/operating_systems/concurrency.py'
if not hasattr(sys, '_MEIPASS'):
    SCRIPT_FILEPATH = os.path.abspath(__file__)
else:
    SCRIPT_FILEPATH = os.path.abspath(os.path.join(sys._MEIPASS, SCRIPT_RELPATH))  # pylint: disable=no-member
SCRIPT_DIRPATH = os.path.dirname(SCRIPT_FILEPATH)
SCRIPT_NAME = os.path.splitext(os.path.basename(__file__))[0]
THIS_MODULE = sys.modules[__name__]
LOGGER = logging.getLogger(__name__)
LOGGER.addHandler(logging.NullHandler())


def peterson():
    # type: () -> None
    '''
    Description:
        signal my intent
        turn = other
        while other signaled intent AND its their turn: spin
        designal my intent
        NOTE:
            # while (not stop.is_set() and shared['flag'][id_self] == True and shared['turn'] != id_self):  # NON CANNON, my personal understanding, IS WRONG
            # CANNON WORKS and allows p0 to run indefinitely if p1 dies or never starts or vice versa
    '''

    shared = {  # declared as dict for global access
        'turn': 9999,
        'flag': [False, False]  # intent to enter, .lock()
    }

    def peterson_thread(id_self, id_other, stop=threading.Event(), debug=False):  # 0, 1
        # type: (int, int, threading._Event, bool) -> None
        while not stop.is_set():
            shared['flag'][id_self] = True  # signal my intent
            shared['turn'] = id_other  # turn = other

            while (not stop.is_set() and shared['flag'][id_other] == True and shared['turn'] == id_other):  # CANNON
                if debug:
                    name = threading.current_thread().name  # BREAKPOINT: here

            if stop.is_set():
                break

            # critical section
            print(f'{id_self} - {time.time():0.6f}')

            shared['flag'][id_self] = False

    stop = threading.Event()
    p0 = threading.Thread(name='p0', target=peterson_thread, args=(0, 1), kwargs=dict(stop=stop), daemon=False)
    p1 = threading.Thread(name='p1', target=peterson_thread, args=(1, 0), kwargs=dict(stop=stop), daemon=False)

    try:
        p0.start()
        time.sleep(0.001)  # correct solution allows p0 to run unabated
        p1.start()
        while True:
            time.sleep(0.005)  # spin
    except KeyboardInterrupt:
        stop.set()
        LOGGER.warning('ctrl+c')
