#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
Author:         Chris Carl
Email:          chrisbcarl@chriscarl.com
Date:           2024-11-22
Description:

Python is lots of deep nerdy python shit that usually involves runtime fuckery.
chriscarl.core files are non-self-referential, do very little importing, and define the bedrock from which other things do import.

Updates:
    2024-12-11 - core.python - added abbreviate_arg now uses repr to avoid multiline string args in the output
    2024-12-09 - core.python - added get_this_file_lineno / get_caller_file_lineno
    2024-11-29 - core.python - fixed abbreviate_arg so that it wouldnt always have elipses
    2024-11-27 - core.python - added abbreviate_arg
    2024-11-26 - core.python - added invocation support for partials
    2024-11-25 - core.python - added fallback check which strangely hasnt been triggered yet until I tried Iterable
                 core.python - added ModuleDocumentation
    2024-11-22 - core.python - initial commit
'''

# stdlib imports
from __future__ import absolute_import, print_function, division, with_statement  # , unicode_literals
import os
import re
import sys
import logging
import datetime
import functools
import subprocess
from dataclasses import dataclass, field
from typing import Any, Tuple, List, Union, Callable, Generator, Dict, Optional, Iterable

# third party imports

# project imports
from chriscarl.core.constants import SENTINEL

SCRIPT_RELPATH = 'chriscarl/core/functors/python.py'
if not hasattr(sys, '_MEIPASS'):
    SCRIPT_FILEPATH = os.path.abspath(__file__)
else:
    SCRIPT_FILEPATH = os.path.abspath(os.path.join(sys._MEIPASS, SCRIPT_RELPATH))  # pylint: disable=no-member
SCRIPT_DIRPATH = os.path.dirname(SCRIPT_FILEPATH)
SCRIPT_NAME = os.path.splitext(os.path.basename(__file__))[0]
THIS_MODULE = sys.modules[__name__]
LOGGER = logging.getLogger(__name__)
LOGGER.addHandler(logging.NullHandler())

_hasattr = hasattr
_getattr = getattr
_setattr = setattr


def abbreviate_arg(arg, chars=32):
    # type: (Any, int) -> str
    '''
    '''
    if chars < 3:
        raise ValueError("you cant have an abbreviation less than 3... that would leave out '...' as an option...")
    if isinstance(arg, str):
        str_a = repr(arg)[1:-1]
        if len(str_a) - 3 > chars:
            if os.path.exists(str_a):
                relpath = os.path.relpath(str_a, os.getcwd())
                if len(relpath) - 3 > chars:
                    token = '"{}"'.format(relpath[:chars - 3] + "...")
                else:
                    token = '"{}"'.format(relpath)
            else:
                token = "'{}'".format(str_a[:chars - 3] + "...")
        else:
            token = str_a
    else:
        str_a = repr(arg)
        if len(str_a) - 3 > chars:
            token = str_a if len(str_a) < chars else str_a[:chars - 3] + '...'
        else:
            token = str_a
    return token


def invocation_arg_string(args):
    # type: (Iterable) -> str
    return ', '.join(abbreviate_arg(arg) for arg in args)


def invocation_kwarg_string(kwargs):
    # type: (dict) -> str
    return ', '.join('{}={!r}'.format(str(k), v) for k, v in kwargs.items())


def invocation_vararg_string(varargs=None, varkwargs=None):
    # type: (Optional[str], Optional[str]) -> str
    if varargs is not None and varkwargs is not None:
        return '*{}, **{}'.format(varargs, varkwargs)
    elif varargs is not None:
        return '*{}'.format(varargs)
    else:
        return '**{}'.format(varkwargs)


def invocation_just_arg_string(func, args, kwargs, varargs=None, varkwargs=None):
    # type: (Callable, Iterable, dict, Optional[str], Optional[str]) -> str
    arglist = invocation_arg_string(args)
    kwarglist = invocation_kwarg_string(kwargs)
    varlist = invocation_vararg_string(varargs=varargs, varkwargs=varkwargs)
    tokens = []
    if args:
        tokens.append(arglist)
    if sys.version_info[0] > 2:
        if varargs:
            tokens.append('*{}'.format(varargs))
        if kwargs:
            tokens.append(kwarglist)
        if varkwargs:
            tokens.append('**{}'.format(varkwargs))
    else:
        if kwargs:
            tokens.append(kwarglist)
        if varargs is not None or varkwargs is not None:
            tokens.append(varlist)

    return '{}'.format(', '.join(tokens))


def get_func_name(func):
    # type: (Callable) -> str
    if isinstance(func, functools.partial):
        func = func.func

    try:
        return func.__name__
    except Exception:
        pass

    try:
        # sys.version_info[0] == 2:
        return func._Method__name  # type: ignore
    except Exception:
        pass

    raise RuntimeError('could not determine name from func {}!'.format(func))


def invocation_string(func, args=None, kwargs=None, varargs=None, varkwargs=None, func_name=None):
    # type: (Callable, Optional[Iterable], Optional[dict], Optional[str], Optional[str], Optional[str]) -> str
    args = args or tuple()
    kwargs = kwargs or dict()
    func_name = func_name or get_func_name(func)
    return '{}({})'.format(func_name, invocation_just_arg_string(func, args, kwargs, varargs=varargs, varkwargs=varkwargs))


def hasattr_deep(obj, key):
    # type: (Any, str) -> bool
    '''
    Description:
        test if an object has a deeply nested attribute
        >>> hasattr_deep(obj, 'attr.member')
    '''
    subobj = obj
    for token in key.split('.'):
        if _hasattr(subobj, token):
            subobj = _getattr(subobj, token)
        else:
            return False
    return True


def hasattr_cmp(key, *objs):
    # type: (str, Any) -> Tuple[bool, bool]
    '''
    Description:
        if the first object has or doesnt have the deeply nested attribute:
            are ALL of the rest of the objects the same way?
        >>> hasattr_deep('attr.member', obj0, obj1, obj2)
        >>> (True, True)  # obj0 has attr.member, [obj1, obj2] does all have attr.member
        >>> (True, False)  # obj0 has attr.member, [obj1, obj2] does not all have attr.member
        >>> (False, True)  # obj0 does not have attr.member, [obj1, obj2] does not all have attr.member
        >>> (False, False)  # obj0 does not have attr.member, [obj1, obj2] does all have attr.member
    Returns:
        Tuple
            bool - whether the FIRST object had the deeply nested attribute
            bool - whether all objects are the same way as the first object
    '''
    if len(objs) < 2:
        raise ValueError('must supply multiple objects')

    A = objs[0]
    B = objs[1:]

    if hasattr_deep(A, key):
        return (True, all(hasattr_deep(obj, key) for obj in B))
    else:
        return (False, all(not hasattr_deep(obj, key) for obj in B))


def getattr_deep(obj, key, default=SENTINEL):
    # type: (Any, str, Any) -> Any
    '''
    Description:
        get an object's deeply nested attribute or raise AttributeError
        >>> getattr_deep(obj, 'attr.member')
        >>> 69
        >>> getattr_deep(obj, 'attr.member2') -> attribute error
        >>> getattr_deep(obj, 'attr.member2', False)
        >>> False
    Raises:
        AttributeError
    '''
    subobj = obj
    try:
        for token in key.split('.'):
            subobj = _getattr(subobj, token)
    except AttributeError as ae:
        if default != SENTINEL:  # i can't use None, because some deep code uses getattr(blah, blah, None), particularly in pytest...
            return default
        raise AttributeError('{} instance has no attribute {}'.format(obj.__class__.__name__, key)) from ae

    return subobj


def getattr_cmp(key, *objs):
    # type: (str, Any) -> bool
    '''
    Description:
        Are all of the deeply nested attributes equal among the objects?
        >>> getattr_cmp('attr.member', obj0, obj1, obj2)
        >>> True  # they are all equal
        >>> False  # one or more is not equal
    Returns:
        bool
    '''
    if len(objs) < 2:
        raise ValueError('must supply multiple objects')

    A = objs[0]
    B = objs[1:]

    value = getattr_deep(A, key)  # raises: AttributeError
    for obj in B:
        try:
            if value != getattr_deep(obj, key):
                return False
        except AttributeError:
            return False
    return True


def setattr_deep(obj, key, value):
    # type: (Any, str, Any) -> None
    '''
    Description:
        set an object's deeply nested attribute or raise AttributeError
        >>> setattr_deep(obj, 'attr.member')
    Raises:
        AttributeError
    '''
    subobj = obj
    try:
        tokens = key.split('.')
        for token in tokens[:-1]:
            subobj = _getattr(subobj, token)
        _setattr(subobj, tokens[-1], value)
    except AttributeError as ae:
        raise AttributeError('{} instance has no attribute {}'.format(obj.__class__.__name__, key)) from ae


T_FUNC_ARGS_KWARGS = List[Union[
    # print
    Callable,
    # print, ('hello', 'world',)
    Tuple[Callable, Union[list, tuple, Any, None]],
    # print, ('hello', 'world',), dict(end='|')
    Tuple[Callable, Union[list, tuple, Any, None], dict]]]


def conform_func_args_kwargs(func_args_kwargs):
    # type: (T_FUNC_ARGS_KWARGS) -> List[Tuple[Callable, tuple, dict]]
    sanitized = []
    for e, tpl in enumerate(func_args_kwargs):
        if callable(tpl):
            func, args, kwargs = tpl, tuple(), dict()  # type: ignore
        elif len(tpl) == 1:
            func, args, kwargs = tpl[0], tuple(), dict()
        elif len(tpl) == 2:
            func, args = tpl[0], tpl[1]  # type: ignore
            kwargs = dict()
        elif len(tpl) == 3:
            func, args, kwargs = tpl[0], tpl[1], tpl[2]  # type: ignore
        else:
            raise ValueError('variable {} is expected to be a 1-3 nary tuple of func, args, kwargs!'.format(e))
        if not isinstance(args, tuple):
            args = (args, )
        if not isinstance(kwargs, dict):
            raise TypeError('variable {} kwargs is not of type dict! it is expected to be a 1-3 nary tuple of func, args, kwargs!'.format(e))
        sanitized.append((func, args, kwargs))
    return sanitized


def run_func_args_kwargs(func_args_kwargs, break_idx=-1, log_level=logging.DEBUG):
    # type: (List[Union[Callable, Tuple[Callable, Union[tuple, Any, None]], Tuple[Callable, Union[tuple, Any, None], dict]]], int, Union[str, int]) -> Generator[Any, None, List[Any]]
    from chriscarl.core.lib.stdlib.logging import get_log_func_from_level
    log_func = get_log_func_from_level(log_level)
    variables = conform_func_args_kwargs(func_args_kwargs)
    results = []
    for e, tpl in enumerate(variables):
        func, args, kwargs = tpl
        inv_str = invocation_string(func, args=args, kwargs=kwargs)
        log_func('%s / %s - %s', e, len(variables) - 1, inv_str)

        if break_idx > -1 and break_idx == e:
            try:
                filepath = sys.modules[func.__module__].__file__
                # https://stackoverflow.com/questions/39453951/open-file-at-specific-line-in-vscode
                # TODO: code --goto "<filepath>:<linenumber>:<x-coordinates>"
                if filepath:  # wont be in in an interpreter
                    subprocess.Popen(['code', '--goto', filepath], shell=True)
                input('!!! BREAK IDX ENCOUNTERED !!!\nPress any key to continue (or actually set breakpoints)...')
            except KeyboardInterrupt:
                break
        result = func(*args, **kwargs)
        yield result
        log_func('%s / %s - %s = %s', e, len(variables) - 1, inv_str, result)
        results.append(result)

    return results


def is_legal_python_name(text):
    # type: (str) -> bool
    return not any([
        re.search(r'[^A-Za-z0-9_]', text),
        re.search(r'\s', text),
        re.match(r'^\d', text),
    ])


def get_legal_python_name(text):
    # type: (str) -> str
    sofar = re.sub(r'[^A-Za-z0-9_]', '_', text)
    sofar = re.sub(r'\s{1,}', '_', sofar)
    sofar = re.sub(r'_{2,}', '_', sofar)
    if re.match(r'^\d', sofar):
        sofar = '_{}'.format(sofar)
    return sofar


@dataclass
class ModuleDocumentation(object):
    '''
    Description:
        a documentation object that can analyze MY personal code style and make it a bit more of a data structure.
    '''
    author: str
    email: str
    date: Optional[datetime.datetime]
    description: str
    updates: Dict[datetime.datetime, list] = field(default_factory=lambda: {})

    @classmethod
    def parse(cls, text):
        # type: (str) -> ModuleDocumentation
        author_mo = re.search(r'author\:\s+([\w\ ]+)', text, flags=re.IGNORECASE)
        author = author_mo.groups()[0] if author_mo else ''
        email_mo = re.search(r'email\:\s+([\w\-\.]+@[\w-]+\.+[\w-]{2,})', text, flags=re.IGNORECASE)  # https://regex101.com/r/lHs2R3/1
        email = email_mo.groups()[0] if email_mo else ''
        date_mo = re.search(r'date\:\s+(\d{4}-\d{2}-\d{2})', text, flags=re.IGNORECASE)
        date = datetime.datetime.strptime(date_mo.groups()[0], '%Y-%m-%d') if date_mo else None
        description_idx = text.find('escription:') + len('escription:')
        updates_idx = text.find('pdates:') + len('pdates:')
        description_end = updates_idx - len('pdates:') - 1
        description = text[description_idx:description_end].strip()
        updates_text = text[updates_idx:]
        updates: Dict[datetime.datetime, list] = {}
        current_update_date = datetime.datetime.now()
        previous_line_idx = -1  # preserve any indents
        for line in updates_text.splitlines():
            if not line.strip():
                continue
            update_date_mo = re.search(r'(\d{4}-\d{2}-\d{2})\s?-\s?', line, flags=re.IGNORECASE)
            update_date = datetime.datetime.strptime(update_date_mo.groups()[0], '%Y-%m-%d') if update_date_mo else None
            if update_date and update_date != current_update_date:
                current_update_date = update_date
                updates[current_update_date] = []
            if update_date_mo:
                update_desc = line[update_date_mo.end():].strip()
                previous_line_idx = update_date_mo.end()
            else:
                update_desc = line[previous_line_idx:]
            updates[current_update_date].append(update_desc)

        return ModuleDocumentation(author=author, email=email, date=date, description=description, updates=updates)

    def to_string(self):
        tokens = []
        for date in sorted(self.updates, reverse=True):
            for m, message in enumerate(self.updates[date]):
                if m == 0:
                    tokens.append('    {} - {}'.format(date.strftime('%Y-%m-%d'), message))
                else:
                    tokens.append('                 {}'.format(message))
        update_text = '\n'.join(tokens)
        text = '''
Author:         {}
Email:          {}
Date:           {}
Description:

{}

Updates:
{}
'''.format(self.author, self.email,
           self.date.strftime('%Y-%m-%d') if self.date else '', self.description, update_text)
        return text
