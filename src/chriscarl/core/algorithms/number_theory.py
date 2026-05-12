#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
Author:         Chris Carl
Email:          chrisbcarl@outlook.com
Date:           2026-02-02
Description:

core.algorithms.number_theory contains stuff like IEEE754
core are modules that define the bedrock from which other things do import. non-self-referential, low-import, etc.

Updates:
    2026-05-12 - core.algorithms.number_theory - added get_digit
    2026-02-05 - core.algorithms.number_theory - touch-ups
    2026-02-02 - core.algorithms.number_theory - initial commit
'''

# stdlib imports
from __future__ import absolute_import, print_function, division, with_statement  # , unicode_literals
import os
import sys
import logging
import re

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


def base_n_to_10(value, base=2):
    # type: (str, int) -> int|float
    '''
    Description:
        $(v)_{n} = (v')_{10}$
        - NOTE: negatives are not represented in 2's comp. 10000000 is treated as 2^7, not -1
    Examples:
        >>> base_n_to_10('1010.01011', base=2, signed=False) -> 10.34375
        >>> base_n_to_10('F.8', base=16, signed=False) -> 15.5
        >>> base_n_to_10('-.01011', base=2, signed=False) -> 0.34375
    Returns:
        int|float
            number in base 10
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


def _ieee754_to_decimal_elipses(txt, bits):
    if '>' not in txt:
        return txt
    left, right = txt.split('>')
    used_bits = len(left) + len(right)
    bits = bits - used_bits
    repeated = left[-1]
    return f'{left}{repeated * bits}{right}'


def ieee754_to_decimal(value, double=False):
    # type: (str, bool) -> float
    '''
    Description:
        these are all -1.0 (single-precision), note the unicode, elipses, and decimal:
            101111111.00000000000000000000000
            101....0...
            101….0…
    Arguments:
        value: str
        double: bool
            default False
            do you know if this is provided as a double-precision?
    Returns:
        float
            it always has to be a float return, can't be an int...
    '''
    # original = value
    if not re.match(r'[01\.…]{4,64}', value):
        raise ValueError('value must at least be 00.0, composed of 0s and 1s and a few dots. right?')
    width = (value.count('0') + value.count('1'))
    if width > 64:
        raise NotImplementedError(f'for str size {len(value)}')
    if not double:
        if width > 32:
            double = True
    e_len = 11 if double else 8
    f_len = 52 if double else 23
    b = 2**(e_len - 1) - 1  # bias

    value = re.sub(r'(\.\.\.|…)', '>', value)  # replace ALL expanders with a common expander
    mos = list(re.finditer(r'\.\d', value))
    if not mos or len(mos) > 1:
        raise ValueError(f'could not detect decimal point, must resemble only \\.\\d even with compaction! {value!r}')
    mo = mos[0]
    sign_exp = value[:mo.start()]
    sign, exp = sign_exp[0], sign_exp[1:]
    s = 0 if sign == '0' else 1

    # exp will be of the form 00000000, 0>0 or >0
    if exp.startswith('>'):
        exp = sign_exp  # the original because the user wanted the sign bit to repeat...

    frac = value[mo.start() + 1:]

    expX, fracX = _ieee754_to_decimal_elipses(exp, e_len), _ieee754_to_decimal_elipses(frac, f_len)
    # special cases
    if expX.count('0') == e_len:
        if fracX.count('0') == f_len:
            return 0.0
        # valid data, just needs to be normalized, will be quite small
    if expX.count('1') == e_len:
        if fracX.count('0') == f_len:
            if s == 0:
                return float('inf')
            else:
                return float('-inf')
        else:
            return float('nan')

    e = base_n_to_10(expX, base=2)
    f = base_n_to_10(f'0.{fracX}', base=2)
    n = (1 - 2 * s) * (1 + f) * 2**(e - b)
    # normalized = f'{"-" if sign else ""}1.{fracX} * 2**({e-b})'
    # print(
    #     {
    #         'original': original,
    #         'value': value,
    #         'double': double,
    #         'exp': exp,
    #         'frac': frac,
    #         'expX': expX,
    #         'fracX': fracX,
    #         's': s,
    #         'e': e,
    #         'b': b,
    #         'f': f,
    #         'e_len': e_len,
    #         'f_len': f_len,
    #         'normalized': normalized,
    #         'n': n,
    #     }
    # )

    return float(n)


def get_digit(num, pow):
    # type: (float|int, int) -> float
    '''
    Description:
        say you have 3.14 and you want the 4?
        >>> get_fractional_digit(3.14, -2)
        developed out of AI, Qwen3.6-35B-A3B-UD-Q5_K_XL -seed 69:
            >>> # python code to get the digit in the 1/10th place. respond with 1 code sample or less
            >>> digit = int(abs(num) * 10) % 10
    '''
    magnitude = 10**(pow)
    digit = int(abs(num) / magnitude) % 10
    return digit
