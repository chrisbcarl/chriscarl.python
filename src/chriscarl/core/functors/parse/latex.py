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
    2026-03-02 - core.functors.parse.latex - added lstlisting_supported
    2026-02-16 - core.functors.parse.latex - added matrix_to_latex
    2026-02-15 - core.functors.parse.latex - augmented evaluate, need for proper stack solution obvious
    2026-02-05 - core.functors.parse.latex - added evaluate
    2026-02-04 - core.functors.parse.latex - added latex_escape_raw and latex_escape is more straightforward...
                 core.functors.parse.latex - added latex_replace
    2026-01-25 - core.functors.parse.latex - initial commit

TODO:
- BUG: bottom
'''

# stdlib imports
from __future__ import absolute_import, print_function, division, with_statement  # , unicode_literals
import os
import sys
import logging
import re
import math  # needed for sqrt evaluate
from typing import List, Optional, Any

# third party imports

# project imports
from chriscarl.core.lib.stdlib.typing import isinstance_raise
from chriscarl.core.types.str import indent
from chriscarl.core.types.list import rows_to_str_rows, matrix_to_str_rows

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


def evaluate(latex, lcls):
    # type: (str, dict) -> int|float
    # BUG: fails on r'\frac{56 - 70}{\frac{15.572411502397436}{\sqrt{5}}}', will need a flexible command level stack-based solution...
    latex = re.sub(r'\\frac\{([^\}]+)\}\{([^\}]+)\}', r'\g<1>/\g<2>', latex)
    latex = re.sub(r'\\sqrt\{([^\}]+)\}', r'math.sqrt(\g<1>)', latex)
    latex = latex.replace('^', '**')
    latex = latex.replace(')(', ') * (')
    latex = re.sub(r'(\d)\s*\(', r'\g<1> * (', latex)
    return eval(latex, None, lcls)


def matrix_to_latex(array, column_vector=True, one_line=False):
    # type: (List[Any] | List[List[Any]], bool, bool) -> str
    if not column_vector:
        raise NotImplementedError("not sure how to represent otherwise especially for multi-d matricies...")
    isinstance_raise(array, (List[Any], List[List[Any]]))
    if not isinstance(array[0], list):
        return rf'\begin{{bmatrix}}{"\\\\".join(str(ele) for ele in array)}\end{{bmatrix}}'
    else:
        if isinstance(array[0][0], list):
            raise NotImplementedError('too deeply nested!')

        rows, _, max_str_len = matrix_to_str_rows(array)
        fmt = '{:%ds}' % max_str_len
        tokens = ['\\begin{bmatrix}']
        for row in rows:
            tokens.append(f'{" & ".join(fmt.format(r) for r in row)} \\\\')
        tokens.append('\\end{bmatrix}')
        if one_line:
            return ' '.join(tokens)
        else:
            return f'{tokens[0]}\n{indent("\n".join(tokens[1:-1]))}\n{tokens[-1]}'


LSTLISTINGS = '''
# https://www.overleaf.com/learn/latex/Code_listing
ABAP (R/2 4.3, R/2 5.0, R/3 3.1, R/3 4.6C, R/3 6.10)	ACSL
Ada (2005, 83, 95)	Algol (60, 68)
Ant	Assembler (Motorola68k, x86masm)
Awk (gnu, POSIX)	bash
Basic (Visual)	C (ANSI, Handel, Objective, Sharp)
C++ (ANSI, GNU, ISO, Visual)	Caml (light, Objective)
CIL	Clean
Cobol (1974, 1985, ibm)	Comal 80
command.com (WinXP)	Comsol
csh	Delphi
Eiffel	Elan
erlang	Euphoria
Fortran (77, 90, 95)	GCL
Gnuplot	Haskell
HTML	IDL (empty, CORBA)
inform	Java (empty, AspectJ)
JVMIS	ksh
Lingo	Lisp (empty, Auto)
Logo	make (empty, gnu)
Mathematica (1.0, 3.0, 5.2)	Matlab
Mercury	MetaPost
Miranda	Mizar
ML	Modula-2
MuPAD	NASTRAN
Oberon-2	OCL (decorative, OMG)
Octave	Oz
Pascal (Borland6, Standard, XSC)	Perl
PHP	PL/I
Plasm	PostScript
POV	Prolog
Promela	PSTricks
Python	R
Reduce	Rexx
RSL	Ruby
S (empty, PLUS)	SAS
Scilab	sh
SHELXL	Simula (67, CII, DEC, IBM)
SPARQL	SQL
tcl (empty, tk)	TeX (AlLaTeX, common, LaTeX, plain, primitive)
VBScript	Verilog
VHDL (empty, AMS)	VRML (97)
XML	XSLT'''
LSTLISTING_DICT = {}
for __line in LSTLISTINGS.splitlines():
    if not __line or __line.startswith('#'):
        continue
    tokens = __line.split('\t')
    for token in tokens:
        token = token.strip()
        if '(' not in token:
            LSTLISTING_DICT[token.lower()] = token
        else:
            token, subs = token[:-1].split('(')
            for sub in subs.split(','):
                subtoken = f'{token.strip()}[{sub.strip()}]'
                LSTLISTING_DICT[subtoken.lower()] = subtoken


def lstlisting_supported(lst):
    # type: (str) -> str|None
    return LSTLISTING_DICT.get(lst.lower(), None)
