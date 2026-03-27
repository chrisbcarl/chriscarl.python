#!/usr/bin/env python
# -*- coding: utf-8 -*-
r'''
Author:         Chris Carl
Email:          chrisbcarl@outlook.com
Date:           2026-03-26
Description:

core.math.probability is all of the probability learnings I have had over time.
core are modules that define the bedrock from which other things do import. non-self-referential, low-import, etc.

Updates:
    2026-03-26 - core.math.probability - initial commit
                 core.math.probability - added binomial_pdf
'''

# stdlib imports
from __future__ import absolute_import, print_function, division, with_statement  # , unicode_literals
import os
import sys
import logging

# third party imports

# project imports
from chriscarl.core.math.counting import combination

SCRIPT_RELPATH = 'chriscarl/core/math/probability.py'
if not hasattr(sys, '_MEIPASS'):
    SCRIPT_FILEPATH = os.path.abspath(__file__)
else:
    SCRIPT_FILEPATH = os.path.abspath(os.path.join(sys._MEIPASS, SCRIPT_RELPATH))  # pylint: disable=no-member
SCRIPT_DIRPATH = os.path.dirname(SCRIPT_FILEPATH)
SCRIPT_NAME = os.path.splitext(os.path.basename(__file__))[0]
THIS_MODULE = sys.modules[__name__]
LOGGER = logging.getLogger(__name__)
LOGGER.addHandler(logging.NullHandler())


def binomial_pdf(k, n, p, precision=4):
    r'''
    Description:
        $X \overset{iid}{\sim} Bin(n, p) \rightarrow P(X = k) \in \mathbb{R}[0,1]$
        $P(X = k) = \binom{n}{k}p^{k}(1-p)^{n-k}$
        X is a random variable that realizes 0 or 1 at a rate of $p$ 1s.
        The probability that the number of successes is exactly $k$ is given by this PDF at $k$.
        Plot from $k=[0,n]$ for the whole PDF.
    Example:
        - Chance of heads 0.50, 10 coin flips, probability of observing EXACTLY 5 heads?
            $X \overset{iid}{\sim} Bin(n=10, p=0.5)$
            $P(X = 5) = f_{n=10,p=0.5}(5) = \binom{10}{5}(0.5^{5})(1-0.5)^(10-5)$
            >>> binomial_pdf(5, 10, 0.5) = 0.0103
        - Chance of failure 0.28, 1000 widgets, probability of observing EXACTLY 300 failures?
            $X \overset{iid}{\sim} Bin(n=1000, p=0.28)$
            $P(X = 300) = f_{n=10,p=0.5}(300) = \binom{10}{5}(0.5^{5})(1-0.5)^(10-5)$
            >>> binomial_pdf(300, 1000, 0.28) = 0.0103
    Arguments:
        l: int
            less than or equal to l "successes"
        n: int
            total population size
        p: float
            proportion of "successes"
        precision: int
            round to?
    Returns:
        float - probability
    '''
    if not (0 <= p and p <= 1.0):
        raise ValueError(rf'required: $0 \le p \le 1$, provided p={p}')
    probability = combination(n, k) * (p**k) * ((1 - p)**(n - k))
    return round(probability, precision)


def binomial_cdf(l, n, p, precision=4):
    # type: (int, int, float, int) -> float
    r'''
    Description:
        binomial_exact_test, binomial_cdf
        $X \overset{iid}{\sim} Bin(n, p) \rightarrow P(X \le l) = \displaystyle\sum_{k=0}^{l}\binom{n}{k}p^{k}(1-p)^{n-k}$
        This random variable realizes a 1 at some rate $p$ and realizes a 0 at some rate $1 - p$
        Say you will experiment and realize/observe $n$ of these random variables.
        What is the probability you will observe less than $m$ successes?
    Example:
        - Chance of heads 0.50, 10 coin flips, probability of observing LESS THAN 5 heads?
            $X \overset{iid}{\sim} Bin(n=10, p=0.5)$
            $P(X < 5) = P(X \le 4) = F_{n=10,p=0.5}(4) = 0.0751$
            >>> binomial_cdf(4, 10, 0.5) = 0.3770
        - Chance of failure 0.28, 1000 widgets, probability of observing MORE THAN 300 failures?
            $X \overset{iid}{\sim} Bin(n=1000, p=0.28)$
            $P(X > 300) = 1 - P(X \le 300) = 1 - F_{n=1000,p=0.28}(300) = 0.0751$
            >>> 1 - binomial_cdf(300, 1000, 0.28) = 1 - 0.0751
    Arguments:
        l: int
            less than or equal to l "successes"
        n: int
            total population size
        p: float
            proportion of "successes"
        precision: int
            round to?
    Returns:
        float - probability
    '''
    if not (0 <= p and p <= 1.0):
        raise ValueError(rf'required: $0 \le p \le 1$, provided p={p}')
    # probability = sum(binomial_pdf(k, n, p) for k in range(0, l + 1))
    probability = sum(combination(n, k) * (p**k) * ((1 - p)**(n - k)) for k in range(0, l + 1))
    return round(probability, precision)


binomial_exact_test = binomial_cdf
