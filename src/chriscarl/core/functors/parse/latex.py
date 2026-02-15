#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
Author:         Chris Carl
Email:          chrisbcarl@outlook.com
Date:           2026-01-25
Description:

core.functors.parse.latex is stuff that mostly parses LaTeX.
core.functor are modules that functions that are usually defined as lambdas, but i like to hold onto them as named funcs. non-self-referential, low-import, etc.

Updates:
    2026-02-15 - core.functors.parse.latex - augmented evaluate, need for proper stack solution obvious
    2026-02-05 - core.functors.parse.latex - added evaluate
    2026-02-04 - core.functors.parse.latex - added latex_escape_raw and latex_escape is more straightforward...
                 core.functors.parse.latex - added latex_replace
    2026-01-25 - core.functors.parse.latex - initial commit
'''

# stdlib imports
from __future__ import absolute_import, print_function, division, with_statement  # , unicode_literals
import os
import sys
import logging
import re
import math
from typing import List, Optional

# third party imports

# project imports
from chriscarl.core.types.list import rows_to_str_rows

SCRIPT_RELPATH = 'chriscarl/core/functors/parse/latex.py'
if not hasattr(sys, '_MEIPASS'):
    SCRIPT_FILEPATH = os.path.abspath(__file__)
else:
    SCRIPT_FILEPATH = os.path.abspath(os.path.join(sys._MEIPASS, SCRIPT_RELPATH))  # pylint: disable=no-member
SCRIPT_DIRPATH = os.path.dirname(SCRIPT_FILEPATH)
SCRIPT_NAME = os.path.splitext(os.path.basename(__file__))[0]
THIS_MODULE = sys.modules[__name__]
LOGGER = logging.getLogger(__name__)
LOGGER.addHandler(logging.NullHandler())

REGEX_LATEX_ESCAPE_CHARS = re.compile(r'([\\$#%&~_^{}])')
REGEX_LATEX_NEEDS_ESCAPE = re.compile(r'([^\\])([$#%&~_^{}])')
REGEX_LATEX_NEEDS_ESCAPE_ENCLOSED = re.compile(r'([^\\])({[$#%&~_^{}]})')
REGEX_LATEX_FIND_COMMAND_AND_INLINE = re.compile(r'(\\\(.+?\\\)|~?\\[a-zA-Z]{3,}(?:\[.+?\])*(?:\{.+?\}\}?)*)', flags=re.MULTILINE)

LATEX_REPLACE = {
    '…': r'\cdots',
}


def latex_escape_raw(substr, regex=REGEX_LATEX_NEEDS_ESCAPE):
    # type: (str, re.Pattern) -> str
    # find characters that are NOT escaped, and escape them...
    # catch characters in a row like _____
    regex_comp = re.compile(regex)
    while regex_comp.search(substr):
        # {} within just causes problems.
        substr = regex_comp.sub(r'\1\\\2', substr)
    return substr


def latex_escape(text):
    # type: (str) -> str
    # in between the non-math and away from the literal latex commands... do a raw regex escape.
    tokens = []
    prev_end = 0
    for command_or_inline_mo in REGEX_LATEX_FIND_COMMAND_AND_INLINE.finditer(text):
        start, end = command_or_inline_mo.span()
        if start > prev_end:
            substr = text[prev_end:start]
            pure_latex = REGEX_LATEX_ESCAPE_CHARS.sub(r'\\\g<1>', substr)
            tokens.append(pure_latex)  # the whole set

        command_or_inline = text[start:end]
        tokens.append(command_or_inline)
        prev_end = end

    if prev_end < len(text):
        substr = text[prev_end:]
        pure_latex = REGEX_LATEX_ESCAPE_CHARS.sub(r'\\\g<1>', substr)
        tokens.append(pure_latex)  # the whole set
    return ''.join(tokens)


def latex_remove(text):
    return REGEX_LATEX_ESCAPE_CHARS.sub('', text)


ALIGNMENT_CHOICES = {
    'center': 'C',
    'left': 'l',
    'right': 'R',
}


def rows_to_latex(rows, caption=None, label=None, aligned='left'):
    # type: (List[dict], Optional[str], Optional[str], str) -> str
    if aligned not in ALIGNMENT_CHOICES:
        raise ValueError(f'{aligned!r} not in {ALIGNMENT_CHOICES}')
    row_strs, headers, _ = rows_to_str_rows(rows)

    two_column = len(headers) > 3

    table_rows = []
    for _, row in enumerate(row_strs):
        # if ''.join(row.values()) == '':
        #     table_rows.append(r'\addlinespace')
        # else:
        this_row = []
        for header in headers:
            this_row.append(row.get(header, ''))

        # table_rows.append(" & ".join(str(ele) for ele in row.values()))
        table_rows.append(" & ".join(this_row))

    caption_label = []
    if caption:
        caption_label.append(rf'\caption{{{caption}}}')
    if label:
        caption_label.append(rf'\label{{{label}}}')
    caption_label_str = '' if not caption_label else f'\n{"\n".join(caption_label)}\n'

    columns = " & ".join(headers)
    table_text = '\\\\\n'.join(table_rows)
    #     comment = r'''% % https://tex.stackexchange.com/a/305413
    # % \usepackage{tabularx,booktabs}
    # % % defined centered version of "X" column type:
    # % \newcolumntype{C}{>{\centering\arraybackslash}X}
    # % \setlength{\extrarowheight}{1pt} % for a bit more open "look"
    # % \usepackage{lipsum} % filler text
    # '''
    # TODO: can be changed to C instead of X, c instead of l for center
    #   this is because of the \newcolumntype{C}, not sure what else how to adjust
    column_alignment_statement = ''
    if aligned == 'center':
        column_alignment_statement = f'{ALIGNMENT_CHOICES[aligned]} ' * len(headers)
    elif aligned == 'left':
        column_alignment_statement = f'{ALIGNMENT_CHOICES[aligned]} ' * (len(headers) - 1) + 'C '
    elif aligned == 'right':
        column_alignment_statement = 'C ' + f'{ALIGNMENT_CHOICES[aligned]} ' * (len(headers) - 1)
    two_column_complex_line = rf'\begin{{tabularx}}{{\textwidth}}{{{column_alignment_statement}}}'
    # two_column_complex_line = r'\begin{tabularx}{\textwidth}{@{} l *{10}{X} c @{}}'
    single_column_complex_line = rf'\begin{{tabularx}}{{\linewidth}}{{{column_alignment_statement}}}'
    # single_column_complex_line = r'\begin{tabularx}{\linewidth}{p{1.75cm}>{\raggedright\arraybackslash}Xl}'
    begin_table = 'table*' if two_column else 'table'
    # {comment}\begin
    text = rf'''\begin{{{begin_table}}}{caption_label_str}{two_column_complex_line if two_column else single_column_complex_line}
\toprule
{columns} \\
\midrule
{table_text} \\
\bottomrule
\end{{tabularx}}
\end{{{begin_table}}}'''

    return text


def latex_replace(text):
    # type: (str) -> str
    for k, v in LATEX_REPLACE.items():
        text = text.replace(k, v)
    return text


def evaluate(latex):
    # type: (str) -> int|float
    # TODO: fails on r'\frac{56 - 70}{\frac{15.572411502397436}{\sqrt{5}}}', will need a flexible command level stack-based solution...
    latex = re.sub(r'\\frac\{([^\}]+)\}\{([^\}]+)\}', r'\g<1>/\g<2>', latex)
    latex = re.sub(r'\\sqrt\{([^\}]+)\}', r'math.sqrt(\g<1>)', latex)
    latex = latex.replace('^', '**')
    latex = latex.replace(')(', ') * (')
    latex = re.sub(r'(\d)\s*\(', r'\g<1> * (', latex)
    return eval(latex)
