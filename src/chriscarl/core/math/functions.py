#!/usr/bin/env python
# -*- coding: utf-8 -*-
r'''
Author:         Chris Carl
Email:          chrisbcarl@outlook.com
Date:           2026-05-12
Description:

core.math.functions is functions that behave interestingly.
core are modules that define the bedrock from which other things do import. non-self-referential, low-import, etc.

Updates:
    2026-05-12 - /penalty
                 core.math.functions - curious first little function, 'closeness' which exhibits good 'punishment/penalty' behavior
'''

# stdlib imports
from __future__ import absolute_import, print_function, division, with_statement  # , unicode_literals
import os
import sys
import logging

# third party imports

# project imports

SCRIPT_RELPATH = 'chriscarl/core/math/functions.py'
if not hasattr(sys, '_MEIPASS'):
    SCRIPT_FILEPATH = os.path.abspath(__file__)
else:
    SCRIPT_FILEPATH = os.path.abspath(os.path.join(sys._MEIPASS, SCRIPT_RELPATH))  # pylint: disable=no-member
SCRIPT_DIRPATH = os.path.dirname(SCRIPT_FILEPATH)
SCRIPT_NAME = os.path.splitext(os.path.basename(__file__))[0]
THIS_MODULE = sys.modules[__name__]
LOGGER = logging.getLogger(__name__)
LOGGER.addHandler(logging.NullHandler())


def closeness(a, b, base=10):
    # type: (int|float, float, int|float) -> float
    '''
    usage:
        - "punish" things too far away from some objective
            - say i want 10 things, but I have 25, 50, 100 things. how "bad" is that?
                >>> closeness(10, 20, base=1.01)  # .408
                >>> closeness(10, 50, base=1.01)  # .672
                >>> closeness(10, 25, base=1.01)  # .861
            - say i want my kid to score a 90, but they only got an 89, 85, 80, 75. is that basically okay?
                >>> [closeness(90, ele, base=1.01) for ele in [89, 85, 80, 75]]
                ... [0.990, 0.951, 0.905, 0.861]  # typical parent. a 75, wanted 90? that's a "B" result.
                >>> [closeness(90, ele, base=1.1) for ele in [89, 85, 80, 75]]
                ... [0.909, 0.621, 0.386, 0.239]  # tiger-mom. you got an 85? That's as a "D" result!
        - approximate parabolic interaction
            >>> import matplotlib.pyplot as plt
            >>> import seaborn as sns
            >>> arr = np.arange(0, 1, 0.001)
            >>> sns.lineplot(np.vectorize(lambda x: closeness(1, x, base=25   ))(arr)); plt.show()  # very parabolic up to the right
            >>> sns.lineplot(np.vectorize(lambda x: closeness(0, x, base=25   ))(arr)); plt.show()  # very parabolic up to the left
            >>> sns.lineplot(np.vectorize(lambda x: closeness(0, x, base=0.25 ))(arr)); plt.show()  # (base between 0-1) moderately parabolic up to the right
            ... # equivalent:
            >>> sns.lineplot(np.vectorize(lambda x: closeness(0, x, base=0.001))(arr)); plt.show()
            >>> sns.lineplot(np.vectorize(lambda x: closeness(1, x, base=1000 ))(arr)); plt.show()
        - model roots
            >>> closeness(-1, -.5, base=2) == 0.707, sqrt(.707) 0.5
    examples:
        (1, 0.999999, 10)   0.9999976974175578
        (1, 0.999, 10)      0.9977000638225533
        (1, 0.99, 10)       0.9772372209558107
        (1, 0.95, 10)       0.8912509381337455
        (1, 0.9, 10)        0.7943282347242815
        (1, 0.5, 10)        0.31622776601683794
        (1, 0.1, 10)        0.12589254117941673
    cases:
        base == 1? straight line
        base == 10? kinda parabolic
        base == 25? very parabolic
    '''
    if base <= 0:
        raise RuntimeError('base cannot be \\le 0')
    diff = abs(a - b)
    return base**(-diff)  # always exponentiated to a negative power
