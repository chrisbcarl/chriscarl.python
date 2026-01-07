#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
Author:         Carl, Chris
Email:          chrisbcarl@chriscarl.com
Date:           2024-11-23
Description:

core.lib.stdlib.typing is tricky, but I think I can hack at it to make it useful.
core.lib are modules that contain code that is about (but does not modify) the library. somewhat referential to core.functor and core.types.

Updates:
    2024-11-22 - core.lib.stdlib.typing - initial commit
'''

# stdlib imports
from __future__ import absolute_import, print_function, division, with_statement  # , unicode_literals
import os
import sys
import inspect
import logging
# TODO: _AnyMeta breaks on 3.9 and 3.10...
from typing import (  # type: ignore
    Any, List, Literal, Iterable, Union, _AnyMeta, _UnionGenericAlias, _GenericAlias,
)
from types import ModuleType

# third party imports

# project imports

SCRIPT_RELPATH = 'chriscarl/core/lib/stdlib/typing.py'
if not hasattr(sys, '_MEIPASS'):
    SCRIPT_FILEPATH = os.path.abspath(__file__)
else:
    SCRIPT_FILEPATH = os.path.abspath(os.path.join(sys._MEIPASS, SCRIPT_RELPATH))  # pylint: disable=no-member
SCRIPT_DIRPATH = os.path.dirname(SCRIPT_FILEPATH)
SCRIPT_NAME = os.path.splitext(os.path.basename(__file__))[0]
THIS_MODULE = sys.modules[__name__]
LOGGER = logging.getLogger(__name__)
LOGGER.addHandler(logging.NullHandler())

_isinstance = isinstance
T_TYPING = Union[type, Iterable, _AnyMeta, None, _UnionGenericAlias, _GenericAlias, ModuleType]


def isof_typing(obj, typing):
    # type: (Any, Union[_UnionGenericAlias, _GenericAlias]) -> bool
    if _isinstance(typing, (tuple, list, set, dict)):
        return any(isof_one(obj, typ) for typ in typing)

    name = getattr(typing, '_name', '')
    origin = getattr(typing, '__origin__', None)
    if not isinstance(origin, type):
        if origin is not Union:
            raise RuntimeError('ive never encountered an __origin__ whose type was {} - {}!'.format(type(origin), origin))
    args = getattr(typing, '__args__', None)
    if args is None:
        args = tuple()
    if not isinstance(args, tuple):
        raise RuntimeError('ive never encountered an __args__ whose type was {} - {}!'.format(type(args), args))
    # params: tuple = getattr(typing, '__params__', None)
    if origin:
        # Tuple, List, Set, Dict | Union | Callable | Generator | Literal
        if name in ['List', 'Tuple', 'Dict', 'Set']:
            # applies to list, dict, tuple, set
            if not _isinstance(obj, origin):
                return False
            if len(args) == 0:
                return True  # we can't validate further

            if name == 'Dict':
                # Dict[str, List[Union[int, float]]] -> '__args__': (<class 'str'>, typing.List[typing.Union[int, float]])
                return all(isof_one(k, args[0]) and isof_one(v, args[1]) for k, v in obj.items())
            elif name == 'Tuple':
                if len(obj) != len(args):
                    return False
                # Tuple[list, dict, set] -> '__args__': (<class 'list'>, <class 'dict'>, <class 'set'>),
                return all(isof_one(obj[a], arg) for a, arg in enumerate(args))

            return all(isof_one(ele, args) for ele in obj)
        elif origin is Union:
            # Union[int, float] -> '__args__': (<class 'int'>, <class 'float'>)
            return isof_one(obj, args)
        elif name == 'Callable':
            # Callable[[int, typing.List[float]], typing.Tuple[int, float]] -> '__args__': (<class 'int'>, typing.List[float], typing.Tuple[int, float])
            # TODO: i can definitely do some argspec investigation to be sure, but hey.
            return callable(obj)
        elif name == 'Generator':
            # Generator[typing.Tuple[int, typing.List[float]], NoneType, NoneType] ->  '__args__': (typing.Tuple[int, typing.List[float]], <class 'NoneType'>, <class 'NoneType'>)
            # TODO: i can definitely do some argspec investigation to be sure, but hey.
            if callable(obj):
                raise RuntimeError('you actually cant typecheck a FUNCTION to see if it is a generator, you have to call it first and GET a generator...')
            return inspect.isgenerator(obj)
        elif origin is Literal:
            # Literal[True] -> '__args__': (True,)
            return obj == args[0]

    # ultimate fallback
    try:
        return _isinstance(obj, typing)
    except TypeError:
        pass

    raise NotImplementedError('im so sorry, I havent yet figured out how to handle {}'.format(typing))


def isof_iterable(obj, itr):
    # type: (Any, Iterable[Union[type ,_UnionGenericAlias, _GenericAlias]]) -> bool
    return any(isof_one(obj, typ) for typ in itr)


def isof_one(obj, typing):
    # type: (Any, T_TYPING) -> bool
    if typing is Any:
        return True
    if typing is None:
        if obj is None:
            return True
        return False
    if _isinstance(typing, type):
        return _isinstance(obj, typing)  # type: ignore
    if typing is ModuleType:
        return _isinstance(obj, typing)  # type: ignore

    return isof_typing(obj, typing)


def isof(obj, *typings):
    # type: (Any, T_TYPING) -> bool
    '''
    Description:
        wouldnt it be nice to do something like this?
            isinstance(lst, List[Union[int, float]])
        now you can!

    NOTE:
        there are a few cases to handle (not to mention the halting problem with respect to generators...):
            typings is singular
            typings is a tuple
            typings is a typing and therefore nested, etc.
        - prior research had me look at https://stackoverflow.com/questions/37973820
            but I just blew right past it and I'm happy with what I've got
    '''
    if len(typings) == 1:
        return isof_one(obj, *typings)
    return any(isof_one(obj, typing) for typing in typings)


def isinstance_raise(obj, *typings, msg=''):
    # type: (Any, T_TYPING, str) -> bool
    # TODO: as_list(1, List[str]) needs to have nicer output message saying elements within the datastruct are no good, rather than the whole:
    #       TypeError: provided <class 'list'> for 'obj_or_list', requires: typing.List[str]
    from chriscarl.core.lib.stdlib.inspect import get_variable_name_lineno
    var_name = get_variable_name_lineno(obj)[0]

    res = isof(obj, *typings)
    if not res:
        msg = msg or 'provided {} for {!r}, requires: {}'.format(type(obj), var_name, typings if len(typings) > 1 else typings[0])
        raise TypeError(msg)
    return res
