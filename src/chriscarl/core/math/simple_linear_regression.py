#!/usr/bin/env python
# -*- coding: utf-8 -*-
r'''
Author:         Chris Carl
Email:          chrisbcarl@outlook.com
Date:           2026-03-27
Description:

core.math.simple_linear_regression is writing down all of my learnings from theoretical applied probability and statistics into 1 spot.
core are modules that define the bedrock from which other things do import. non-self-referential, low-import, etc.

Updates:
    2026-03-27 - core.math.simple_linear_regression - initial commit
'''

# stdlib imports
from __future__ import absolute_import, print_function, division, with_statement  # , unicode_literals
import os
import sys
import logging
from typing import List, Tuple

# third party imports

# project imports

SCRIPT_RELPATH = 'chriscarl/core/math/simple_linear_regression.py'
if not hasattr(sys, '_MEIPASS'):
    SCRIPT_FILEPATH = os.path.abspath(__file__)
else:
    SCRIPT_FILEPATH = os.path.abspath(os.path.join(sys._MEIPASS, SCRIPT_RELPATH))  # pylint: disable=no-member
SCRIPT_DIRPATH = os.path.dirname(SCRIPT_FILEPATH)
SCRIPT_NAME = os.path.splitext(os.path.basename(__file__))[0]
THIS_MODULE = sys.modules[__name__]
LOGGER = logging.getLogger(__name__)
LOGGER.addHandler(logging.NullHandler())


def least_squares(X, Y, precision=4):
    # type: (List[float|int], List[float|int], int) -> Tuple[float, float]
    r'''
    Description:
        - model: $Y = \beta_0 + \beta_1 X + \epsilon \overset{iid}{\sim} \mathcal{N}(0, \sigma^2)$
        - point estimator: $\hat{y} = \hat{\beta_0} + \hat{\beta_1} x + e \overset{iid}{\sim} \mathcal{N}(0, \sigma^2)$
        - solve:
            - determining values for $\hat{\beta_0}$ and $\hat{\beta_1}$ is done by minimizing the Least Squares objective function.
            - $\underset {x\in (-\infty ,-1]}{\operatorname{arg\,min}} \sum_{i = 1}^{n} (y_i - \hat{y_i})^2$
            - solve by partial differentiation on $\beta_0$ and $\beta_1$, set both to 0 (the min), then solve for $\beta_0$ and $\beta_1$
            - the closed form of the minimized least squares expresses $\beta_0$ and $\beta_1$ in terms of summary statistics.
            $$
            \begin{aligned}
            S_{{xy}} &= \sum X_i Y_i - \frac{{\sum X_i \sum Y_i}}{{n}}  \\
            S_{{xx}} &= \sum X_i^2 - \frac{{(\sum X_i)^2}}{{n}}  \\
            \hat{{\beta_1}} &= \frac{{S_{{xy}}}}{{S_{{xx}}}} \\
            \hat{{\beta_0}} &= \bar{Y} - \hat{{\beta_1}} \bar{X} = \frac{{\sum Y_i}}{{n}} - \hat{{\beta_1}} * \frac{{\sum X_i}}{{n}} \\
            \end{aligned}
            $$
    Arguments:
        X: List[float|int]
        Y: List[float|int]
        precision: int
            round to?
    Returns:
        $\hat{\beta_0}, \hat{\beta_1}$
    '''
    n, m = len(X), len(Y)
    if n != m:
        raise ValueError('X must be same size as Y!')
    stats = {
        'X^2': [x**2 for x in X],
        'Y^2': [y**2 for y in Y],
        'XY': [X[i] * Y[i] for i, _ in enumerate(X)],
    }
    X_bar = (1 / n) * sum(X)
    Y_bar = 1 / n * sum(Y)

    S_xy = sum(stats['XY']) - sum(X) * sum(Y) / n
    S_xx = sum(stats['X^2']) - sum(X)**2 / n

    beta1hat = S_xy / S_xx
    beta0hat = Y_bar - beta1hat * X_bar

    return round(beta0hat, precision), round(beta1hat, precision)
