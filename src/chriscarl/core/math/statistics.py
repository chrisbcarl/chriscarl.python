#!/usr/bin/env python
# -*- coding: utf-8 -*-
r'''
Author:         Chris Carl
Email:          chrisbcarl@outlook.com
Date:           2026-04-28
Description:

core.math.statistics is writing down all of the learnings i've had taking "statistics".
core are modules that define the bedrock from which other things do import. non-self-referential, low-import, etc.

Updates:
    2026-04-28 - core.math.statistics - initial commit
'''

# stdlib imports
from __future__ import absolute_import, print_function, division, with_statement  # , unicode_literals
import os
import sys
import logging
from typing import List
import math

# third party imports

# project imports

SCRIPT_RELPATH = 'chriscarl/core/math/statistics.py'
if not hasattr(sys, '_MEIPASS'):
    SCRIPT_FILEPATH = os.path.abspath(__file__)
else:
    SCRIPT_FILEPATH = os.path.abspath(os.path.join(sys._MEIPASS, SCRIPT_RELPATH))  # pylint: disable=no-member
SCRIPT_DIRPATH = os.path.dirname(SCRIPT_FILEPATH)
SCRIPT_NAME = os.path.splitext(os.path.basename(__file__))[0]
THIS_MODULE = sys.modules[__name__]
LOGGER = logging.getLogger(__name__)
LOGGER.addHandler(logging.NullHandler())


def expected_value(X, precision=4):
    # type: (List[float|int], int) -> float
    r'''
    Description:
        $$
        E(X) = \mu = \frac{1}{n} \sum X_i \\
        E(X^2) = \frac{1}{n} \sum X_i^2 \\
        E(aX + b) = a E(X) + b
        $$
    Arguments:
        X: List[float|int]
            data as an array
        precision: int
            round to?
    '''
    n = len(X)
    mu = 1/n * sum(X_i for X_i in X)
    if round == -1:
        return mu
    return round(mu, precision)

E = expected_value
mu = expected_value
mean = expected_value

def variance(X, precision=4):
    # type: (List[float|int], int) -> float
    r'''
    Description:
        $$
        Var(X) = \sigma^2 = E[(X - E(X))^2]  \\  % NOTE: bug catastrophic cancellation
        Var(X) = \sigma^2 = E(X^2) - E(X)^2  \\  % NOTE: bug catastrophic cancellation
        Var(X) = \frac{1}{n - 1} \sum_{i=1}^{n} (X_i - \bar{X})^2  \\  % SS sum of squares method, "two-pass", stable
        Var(aX + b) = E([aX + b]^2) - E(aX + b)^2 = a^2 Var(X) \\
        $$
    NOTE:
        - this assumes uniform PDF...
        - WARNING: computational form is unstable, preferred SS form
        - Welford's
    Arguments:
        X: List[float|int]
            data as an array
        precision: int
            round to?
    '''
    mu = E(X)
    # NOTE: https://en.wikipedia.org/wiki/Algorithms_for_calculating_variance
    var = E([(X_i - mu)**2 for X_i in X])
    # var = E([X_i**2 for X_i in X], precision=-1) - E(X, precision=-1)**2
    n = len(X)
    # NOTE: stable due to sum() using compensated summation
    # https://en.wikipedia.org/wiki/Kahan_summation_algorithm
    var = 1/(n-1) * sum((X_i - mu)**2 for X_i in X)
    if round == -1:
        return var
    return round(var, precision)

Var = variance
sigma_squared = variance
