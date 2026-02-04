#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
Author:         Chris Carl
Email:          chrisbcarl@outlook.com
Date:           2026-02-02
Description:

core.algorithms.number_theory is... TODO: lorem ipsum
core are modules that define the bedrock from which other things do import. non-self-referential, low-import, etc.

Updates:
    2026-02-02 - core.algorithms.number_theory - initial commit
'''

# stdlib imports
from __future__ import absolute_import, print_function, division, with_statement  # , unicode_literals
import os
import sys
import logging

# third party imports

# project imports

SCRIPT_RELPATH = 'chriscarl/core/algorithms/number_theory.py'
if not hasattr(sys, '_MEIPASS'):
    SCRIPT_FILEPATH = os.path.abspath(__file__)
else:
    SCRIPT_FILEPATH = os.path.abspath(os.path.join(sys._MEIPASS, SCRIPT_RELPATH))  # pylint: disable=no-member
SCRIPT_DIRPATH = os.path.dirname(SCRIPT_FILEPATH)
SCRIPT_NAME = os.path.splitext(os.path.basename(__file__))[0]
THIS_MODULE = sys.modules[__name__]
LOGGER = logging.getLogger(__name__)
LOGGER.addHandler(logging.NullHandler())

import string

DIGIT_POWER = list(str(idx) for idx in range(10)) + list(string.ascii_uppercase)


def base_n_to_base_10(value, base=2):
    # type: (str, int) -> int|float
    '''
    NOTE: NOT 2's comp representation. 10000000 is treated as 2^7, not -1
    should cover the following assignment requests
    base_n to base 10(signed)
            binary to decimal - 57b
            ocal to decimal - 58c
            hex to decimal - 59a
    >>> base_n_to_base_10('1010.01011', base=2, signed=False) -> 10.34375
    >>> base_n_to_base_10('F.8', base=16, signed=False) -> 15.5
    >>> base_n_to_base_10('-.01011', base=2, signed=False) -> 0.34375
    '''
    value = str(value)
    # step 1, note the sign
    sign = ''
    if value.startswith('+'):
        sign = ''
    elif value.startswith('-'):
        sign = '-'
        value = value[1:]

    if value.startswith('.'):
        value = f'0{value}'

    # step 2 - compute whole
    halves = value.upper().split('.')  # 1010.01011
    if len(halves) == 2:
        whole, fraction = halves[0], halves[1]
    else:
        whole, fraction = halves[0], ''

    # step 2 - compute whole - 1010
    acc_whole = 0  # base 10
    for pow, tok in enumerate(reversed(whole)):  # 0101
        tok_val = DIGIT_POWER.index(tok)
        acc_whole += tok_val * base**pow  # 0 * 2^0 + 1 * 2^1

    # step 3 - compute decimal - 01011
    acc_frac = 0
    for pow, tok in enumerate(fraction):  # 01011 (as provided)
        tok_val = DIGIT_POWER.index(tok)
        acc_frac += tok_val * 1 / (base**(pow + 1))  # 0/2^1 + 1/2^2
    if acc_frac == 0:
        res = f'{sign}{acc_whole}'
        return int(res)
    res = f'{sign}{acc_whole + acc_frac}'
    return float(res)


base_n_to_base_10('1010', base=2)
base_n_to_base_10('-01011', base=2)
base_n_to_base_10('DEAD', base=16)
base_n_to_base_10('-BEEF', base=16)
base_n_to_base_10('e298', base=16)  # 58008
base_n_to_base_10('1010.01011', base=2)
assert base_n_to_base_10('80085', base=10) == 80085
assert base_n_to_base_10('F.8', base=16) == 15.5
base_n_to_base_10('0.01011', base=2)
base_n_to_base_10('.01011', base=2)
assert base_n_to_base_10('-.01011', base=2) == -0.34375

import re


def ieee754_to_decimal(binstr, double=False):
    # type: (str, bool) -> float
    if not re.match(r'[01\.…]{4,64}', binstr):
        raise ValueError('binstr must at least be 00.0, composed of 0s and 1s and a few dots. right?')
    width = (binstr.count('0') + binstr.count('1'))
    if width > 64:
        raise NotImplementedError(f'for str size {len(binstr)}')
    if not double:
        if width > 32:
            double = True
    e_len = 11 if double else 8
    f_len = 52 if double else 23
    b = 2**(e_len - 1) - 1  # bias

    binstr = re.sub(r'(\.\.\.|…)', '>', binstr)  # replace ALL expanders with a common expander
    mo = re.search(r'\.\d', binstr)
    if not mo:
        raise ValueError(f'could not detect decimal point, must resemble \\.\\d even with compaction! {binstr!r}')
    sign_exp = binstr[:mo.start()]
    if len(sign_exp) == 2:
        sign, exp = sign_exp[0], sign_exp  # case when 0....0... or 1....0...
    else:
        sign, exp = sign_exp[0], sign_exp[1:]

    frac = binstr[mo.start() + 1:]

    def elipses(txt, bits):
        if '>' not in txt:
            return txt
        left, right = txt.split('>')
        used_bits = len(left) + len(right)
        bits = bits - used_bits
        repeated = left[-1]
        return f'{left}{repeated * bits}{right}'

    s = 0 if sign == '0' else 1

    expX, fracX = elipses(exp, e_len), elipses(frac, f_len)
    # special cases
    if expX.count('0') == e_len:
        if fracX.count('0') == f_len:
            return 0
        # valid data, just needs to be normalized, will be quite small
    if expX.count('1') == e_len:
        if fracX.count('0') == f_len:
            if s == 0:
                return float('inf')
            else:
                return float('-inf')
        else:
            return float('nan')

    e = base_n_to_base_10(expX, base=2)
    f = base_n_to_base_10(f'0.{fracX}', base=2)
    n = (1 - 2 * s) * (1 + f) * 2**(e - b)
    # print({'binstr': binstr, 'double': double, 'exp': exp, 'frac': frac, 'expX': expX, 'fracX': fracX, 's': s, 'e': e, 'b': b, 'f': f, 'n': n, 'e_len': e_len, 'f_len': f_len})

    return float(n)


# equivalent, -1.0, q4
ieee754_to_decimal('101111111.00000000000000000000000')
ieee754_to_decimal('101....0...')
ieee754_to_decimal('101….0…')

ieee754_to_decimal('0….0…')
ieee754_to_decimal('0....0...')
assert ieee754_to_decimal('0….0…') == 0
assert ieee754_to_decimal('1….0…') == float('-inf')
assert ieee754_to_decimal('01….0…') == float('inf')
assert str(ieee754_to_decimal('01….10…')) == str(float('nan'))

# double, -1.0
ieee754_to_decimal('101111111111.0000000000000000000000000000000000000000000000000000')
ieee754_to_decimal('101....0...', double=True)
ieee754_to_decimal('101….0…', double=True)

# q5
ieee754_to_decimal('001000...0.110...0000', double=True)
ieee754_to_decimal('001000000000.1100000000000000000000000000000000000000000000000000')

ieee754_to_decimal('10....0...1')
ieee754_to_decimal('101111111.00000000000000000000000', double=True)
ieee754_to_decimal('101...1.0...0')
ieee754_to_decimal('110000000.010...0000')
ieee754_to_decimal('110000000.010…0000')
ieee754_to_decimal('001000...0.110...0000')
ieee754_to_decimal('001000…0.110…0000')
ieee754_to_decimal('001000...0.110...0000', double=True)
ieee754_to_decimal('001000…0.110…0000', double=True)

import re


def compute_math(txt):
    txt = re.sub(r'\\frac\{([^\}]+)\}\{([^\}]+)\}', r'\g<1>/\g<2>', txt)
    txt = txt.replace('^', '**')
    print(txt)
    return eval(txt)


whole = compute_math('1*2^0 + 0*2^1 + 0*2^2 + 1*2^3 + 1*2^4 + 1*2^5')
frac = compute_math(r'\frac{0}{2^1} + \frac{0}{2^2} + \frac{1}{2^3} + \frac{1}{2^4}')
print(whole + frac)
