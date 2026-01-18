#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
Author:         Carl, Chris
Email:          chrisbcarl@chriscarl.com
Date:           2024-11-22
Description:

core.lib.stdlib.unittest includes stuff I want all unit tests to have access to
core.lib are modules that contain code that is about (but does not modify) the library. somewhat referential to core.functor and core.types.

Updates:
    2026-01-17 - core.lib.stdlib.unittest - added True as equivalent if the experiment is boolable
    2025-01-01 - core.lib.stdlib.unittest - FIX: stuff that yields generators now will have to answer for their exception crimes
    2024-12-09 - core.lib.stdlib.unittest - UnitTest now configures with my logging by default, so much nicer.
    2024-11-26 - core.lib.stdlib.unittest - added UnitTest as a class
                 core.lib.stdlib.unittest - assertions now outline the line above itself so that they make more sense
    2024-11-22 - core.lib.stdlib.unittest - initial commit
'''

# stdlib imports
from __future__ import absolute_import, print_function, division, with_statement  # , unicode_literals
import os
import sys
import shutil
import inspect
import logging
import unittest
import tempfile
from typing import Callable, Tuple, Iterable, List, Any, Union
from types import TracebackType

# third party imports

# project imports
from chriscarl.core.functors.python import T_FUNC_ARGS_KWARGS, conform_func_args_kwargs, invocation_string
from chriscarl.core.lib.stdlib.typing import isinstance_raise
from chriscarl.core.lib.stdlib.subprocess import launch_editor

SCRIPT_RELPATH = 'chriscarl/core/lib/stdlib/unittest.py'
if not hasattr(sys, '_MEIPASS'):
    SCRIPT_FILEPATH = os.path.abspath(__file__)
else:
    SCRIPT_FILEPATH = os.path.abspath(os.path.join(sys._MEIPASS, SCRIPT_RELPATH))  # pylint: disable=no-member
SCRIPT_DIRPATH = os.path.dirname(SCRIPT_FILEPATH)
SCRIPT_NAME = os.path.splitext(os.path.basename(__file__))[0]
THIS_MODULE = sys.modules[__name__]
LOGGER = logging.getLogger(__name__)
LOGGER.addHandler(logging.NullHandler())


class UnitTest(unittest.TestCase):
    tempdir = ''
    tempfile = ''

    def setUp(self):
        from chriscarl.core.lib.stdlib.logging import configure
        configure()
        fd, self.tempfile = tempfile.mkstemp()
        os.close(fd)
        self.tempdir = tempfile.mkdtemp()
        return super().setUp()

    def tearDown(self):
        try:
            os.remove(self.tempfile)
        except Exception:
            LOGGER.error('unable to remove tempfile at "%s"', self.tempfile)
        try:
            shutil.rmtree(self.tempdir)
        except Exception:
            LOGGER.error('unable to remove tempdir at "%s"', self.tempdir)
        return super().tearDown()

    @staticmethod
    def assert_null_hypothesis(variables, controls, break_idx=-1):
        # type: (T_FUNC_ARGS_KWARGS, List[Any], int) -> bool
        '''
        Description:
            h0 (the "null" hypothesis) is that there is no relationship between the variables and the function, therefore the control group will reflect the experiment results
            the goal here is "fail to fail to reject the null hypothesis"
            >>> variables = [
            >>>     (sum, ([1, 2, 3],), {}),
            >>>     (len, ([1, 2, 3]), {}),
            >>>     (len, 1),
            >>> ]
            >>> controls = [6, 3, TypeError]
            >>> assert_null_hypothesis(variables, controls)
        Arguments:
            variables: List[Union[Callable, Tuple[Callable, Union[list, tuple, Any, None]], Tuple[Callable, Union[list, tuple, Any, None], dict]]]
                basically:
                    (func)
                    (func, arg)
                    (func, kwargs)
                    (func, arg, kwargs)
                    (func, args tuple)
                    (func, args tuple, kwargs)
            controls: List[Any]
            break_idx: int
                set this to get an input pause so that you can "catch yourself" kind of like print debugging.
        '''
        try:
            isinstance_raise(variables, T_FUNC_ARGS_KWARGS)
            isinstance_raise(variables, List[Any])

            if len(variables) != len(controls):
                raise ValueError('len(variables) != len(controls): {} != {}'.format(len(variables), len(controls)))

            conformed_variables = conform_func_args_kwargs(variables)
            for e, tpl in enumerate(conformed_variables):
                func, args, kwargs = tpl
                control = controls[e]
                inv_str = invocation_string(func, args=args, kwargs=kwargs)
                status = 'experiment {} / {} - {}'.format(e, len(conformed_variables) - 1, inv_str)

                # stacklevel has a bug in it somewhere such that lazy formatting isnt correctly using THIS frame, but the stacklevel frame
                LOGGER.debug(status, stacklevel=2)

                if break_idx > -1 and break_idx == e:
                    try:
                        module = sys.modules[func.__module__]
                        if hasattr(module, '__file__'):
                            filepath = module.__file__
                            launch_editor(filepath)
                        input('!!! BREAK IDX ENCOUNTERED - {} !!!\nPress any key to continue (or actually set breakpoints)...'.format(status))
                    except KeyboardInterrupt:
                        sys.exit(2)  # SIGINT-ish

                if inspect.isclass(control) and issubclass(control, Exception):
                    exe = None
                    try:
                        experiment = func(*args, **kwargs)
                        # NOTE: code that yields a generator doesn't actually precompute shit at all--so if there are type checks they will be silent until the first iteration actually does anything...
                        if inspect.isgenerator(experiment) or isinstance(experiment, (map, filter)):
                            LOGGER.debug('{} encountered a generator... expanding.'.format(status))
                            experiment = list(experiment)  # expand it out
                    except Exception as ex:
                        experiment = exe = ex
                    if not exe:
                        assert False, '{} failed to accept null hypothesis (experiment raises exception): {} not encountered, got a real result instead {}!'.format(
                            status, control, experiment
                        )
                    assert issubclass(type(experiment), control), '{} failed to accept null hypothesis (control != experiment): {!r} != {!r}!'.format(status, control, experiment)
                    LOGGER.info('{} PASS w/ expected {}'.format(status, control), stacklevel=2)
                else:
                    experiment = func(*args, **kwargs)
                    if inspect.isgenerator(experiment) or isinstance(experiment, (map, filter)):
                        LOGGER.debug('{} encountered a generator... expanding.'.format(status))
                        experiment = list(experiment)  # expand it out
                    if isinstance(control, bool) and not isinstance(experiment, bool):  # exp = 'string', contr = True
                        assert bool(experiment) == control, '{} failed to accept null hypothesis (control != experiment): {!r} != {!r}'.format(status, control, experiment)
                    else:
                        assert experiment == control, '{} failed to accept null hypothesis (control != experiment): {!r} != {!r}'.format(status, control, experiment)
                    # stacklevel has a bug in it somewhere such that lazy formatting isnt correctly using THIS frame, but the stacklevel frame
                    LOGGER.info('{} PASS'.format(status), stacklevel=2)
            return True
        except AssertionError as ae:
            # https://stackoverflow.com/a/58821552
            exc_info = sys.exc_info()
            traceback = exc_info[2]
            back_frame = traceback.tb_frame.f_back
            back_tb = TracebackType(tb_next=None, tb_frame=back_frame, tb_lasti=back_frame.f_lasti, tb_lineno=back_frame.f_lineno)
            raise AssertionError(str(ae)).with_traceback(back_tb)
        # NOTE: for now I want natural exceptions to raise naturally so that the traceback is fully accurate
        # except Exception as ex:
        #     exc_info = sys.exc_info()
        #     type_ = exc_info[0]
        #     traceback = exc_info[2]
        #     back_frame = traceback.tb_frame.f_back
        #     back_tb = TracebackType(tb_next=None, tb_frame=back_frame, tb_lasti=back_frame.f_lasti, tb_lineno=back_frame.f_lineno)
        #     raise type_(*ex.args).with_traceback(back_tb)

    @staticmethod
    def assert_subset(subset, superset):
        # (Iterable, Iterable) -> bool
        '''
        Description:
            assert that all of the elements of the left are in the elements on the right
        Arguments:
            subset: Iterable
            superset: Iterable
        '''
        isinstance_raise(subset, Iterable)
        isinstance_raise(superset, Iterable)
        assert isinstance(subset, type(superset)), 'failed to assert subset type {} is the type as superset {}!'.format(type(subset), type(superset))

        subset = set(list(subset))
        superset = set(list(superset))

        assert subset.issubset(superset), 'failed to assert left set of {} elements is a subset of right set of {} elements!'.format(len(subset), len(superset))
        return True
