#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
Author:         Chris Carl
Email:          chrisbcarl@outlook.com
Date:           2026-01-24
Description:

core.functors.parse.markdown is functors that can work with markdown text directly rather than relying on something external.
core.functor are modules that functions that are usually defined as lambdas, but i like to hold onto them as named funcs. non-self-referential, low-import, etc.

Updates:
    2026-02-26 - core.functors.parse.markdown - if an svg it prints lineno
    2026-02-20 - core.functors.parse.markdown - moved analyze_extract_sections, sections_to_doclets from tool, brought them here.
    2026-02-01 - core.functors.parse.markdown - added table_to_list, table_to_rows
    2026-01-29 - core.functors.parse.markdown - added table_listified
    2026-01-24 - core.functors.parse.markdown - initial commit
                 core.functors.parse.markdown - LMAO that's why life ain't TDD. TDD is only as good as the test.
'''

# stdlib imports
from __future__ import absolute_import, print_function, division, with_statement  # , unicode_literals
import os
import sys
import logging
import re
from typing import List, Dict, Optional, Tuple
import dataclasses
import pathlib
from collections import OrderedDict

# third party imports

# project imports
from chriscarl.core import constants
from chriscarl.core.lib.stdlib.os import dirpath, is_file
from chriscarl.core.lib.stdlib.io import read_text_file
from chriscarl.core.types.str import indent, find_lineno_index
from chriscarl.core.functors.parse.html import list_to_html

SCRIPT_RELPATH = 'chriscarl/core/functors/parse/markdown.py'
if not hasattr(sys, '_MEIPASS'):
    SCRIPT_FILEPATH = os.path.abspath(__file__)
else:
    SCRIPT_FILEPATH = os.path.abspath(os.path.join(sys._MEIPASS, SCRIPT_RELPATH))  # pylint: disable=no-member
SCRIPT_DIRPATH = os.path.dirname(SCRIPT_FILEPATH)
SCRIPT_NAME = os.path.splitext(os.path.basename(__file__))[0]
THIS_MODULE = sys.modules[__name__]
LOGGER = logging.getLogger(__name__)
LOGGER.addHandler(logging.NullHandler())


def table_to_list(table_text, null=False):
    # type: (str, bool) -> List[list]
    table_text = table_text.strip()
    if not table_text.startswith('|') or not table_text.endswith('|'):
        raise ValueError('probably invalid markdown table! could not detect either the start pipe or end pipe!')

    rows = []
    lines = table_text.splitlines()
    for line in lines:
        row = []
        for col in line.strip()[1:-1].split('|'):  # avoid the end pipes, split on the mid pipes
            col = col.strip()
            if null:
                row.append(col or None)
            else:
                row.append(col)
        rows.append(row)

    return rows


def table_to_rows(table_text, null=False):
    # type: (str, bool) -> List[dict]
    rows = table_to_list(table_text, null=null)

    header = rows[0]
    left = rows[2:]
    rows = []
    for row in left:
        rows.append({head: row[h] for h, head in enumerate(header)})

    return rows


def table_prettify(table_text):
    # type: (str) -> str
    rows = table_to_list(table_text, null=False)

    fmt_cols = []
    cols = len(rows[0])
    for col in range(0, cols):
        maxcollen = -1
        for row in rows:
            maxcollen = max([maxcollen, len(row[col])])
        fmt_cols.append('{:%ss}' % maxcollen)

    out = '\n'.join(f'|{"|".join(fmt_cols[col].format(cell) for col, cell in enumerate(row))}|' for row in rows)
    return out


def table_listified(content, ordered=False):
    # type: (str, bool) -> str
    '''
    Description
        |col|col|col|
        |---|---|---|
        |a  |b  |a,b|
            ===>
        |col|col|col|
        |---|---|---|
        |a  |b  |<ul><li>a</li><li>b</li></ul>|
    Arguments:
        content: str
            markdown content
        ordered: do you want an OL or a UL?
    Returns:
        str
    '''
    table_mos = list(re.finditer(r'\| *([^\|]*?,[^\|]+) *\b', content))
    for _, mo in enumerate(reversed(table_mos)):
        start, end = mo.start(), mo.end()
        substr = mo.groups()[0]
        # print(len(substr), repr(substr))
        lst = [ele.strip() for ele in substr.split(',')]
        if lst:
            replacement = list_to_html(lst, ordered=ordered)
            content = f'{content[:start]}|{replacement}{content[end:]}'

    return content


T_SECTION = Tuple[str, str, Optional[re.Match]]

# BIG sections of markdown potentially
REGEX_CAPTION_LABEL_COMMON = re.compile(r'(?P<caption>(?:caption: *)[^\n]+(?:\n+))?(?P<label>(?:label: *)[^\n]+(?:\n+))?', flags=re.DOTALL | re.MULTILINE)
REGEX_HTML_COMMENT = re.compile(r'\<\!--(.*?)--\>', flags=re.DOTALL | re.MULTILINE)
REGEX_MARKDOWN_YAML = re.compile(r'---\n(.*?)\n---', flags=re.DOTALL | re.MULTILINE)
REGEX_EXTRACT_SECTIONS = OrderedDict([
    ('comment', REGEX_HTML_COMMENT),
    ('yaml', REGEX_MARKDOWN_YAML),
])

REGEX_MARKDOWN_TABLE = re.compile(r'(?:caption: *)?(?P<caption>[^\n]+)?\n+?(?:label: *)?(?P<label>[^\n]+)?\n+?\|(?P<content>.+?)\|\n\n', flags=re.DOTALL | re.MULTILINE)
REGEX_MARKDOWN_LATEX = re.compile(r'\$\$\n\s*(%?\\label\{)?(?P<label>[A-Za-z0-9\-_\.]+)?(\}\n)?(?P<content>.*?)\$\$', flags=re.DOTALL | re.MULTILINE)
REGEX_MARKDOWN_MULTILINE_LITERAL = re.compile(r'```\n(?P<content>.*?)```', flags=re.DOTALL | re.MULTILINE)
REGEX_MARKDOWN_CODE = re.compile(
    r'(?:caption: *)?(?P<caption>[^\n]+)?\n+?(?:label: *)?(?P<label>[^\n]+)?\n+?```(?P<language>[a-z\-\+\# ]+?)\n(?P<content>.*?)```', flags=re.DOTALL | re.MULTILINE
)
# NOTE: THIS ONE IS WEIRD, doing groups[content] will only give you the last quote, but it DOES pick all of them up...
REGEX_MARKDOWN_QUOTE = re.compile(r'(?P<caption>(?:caption: *)[^\n]+(?:\n+))?(?P<label>(?:label: *)[^\n]+(?:\n+))?(?P<content>^>.*\n){1,}', flags=re.MULTILINE)
# NOTE: special unfortunately...
# old - (?:[ \t\n]*(?:[\d+]\.|[-\*]+)\s*(?:.+)\n){2,}
REGEX_MARKDOWN_LIST = re.compile(r'(?:^[ \t\n]*(?:[\d+]\. |[-\*]+) ?(?:.*)\n){1,}', flags=re.MULTILINE)

REGEX_LARGE_SECTIONS = OrderedDict(
    [
        # can have other stuff embedded
        ('table', REGEX_MARKDOWN_TABLE),
        ('latex', REGEX_MARKDOWN_LATEX),
        ('literal', REGEX_MARKDOWN_MULTILINE_LITERAL),
        ('code', REGEX_MARKDOWN_CODE),
        ('quote', REGEX_MARKDOWN_QUOTE),
        ('list', REGEX_MARKDOWN_LIST),
        # implicit ('any': '')
    ]
)
REGEX_MARKDOWN_HEADER = re.compile(r'(?P<octothorps>#+) (?P<title>.+)')
REGEX_MARKDOWN_IMG = re.compile(r'!\[(?P<alt>.*?)\]\((?P<path>.*?\))')
REGEX_MARKDOWN_LITERAL_INLINE = re.compile(r'`(?P<content>[^`]*?)`')
# TODO: I dont know what the non-capture group is doing...
# REGEX_MARKDOWN_LATEX_INLINE = re.compile(r'(?:(?!\$\d[\d\.\,]+ \b))\$(?P<content>.+?)\$')  # , flags=re.DOTALL
REGEX_MARKDOWN_LATEX_INLINE = re.compile(r'(\$|\\\()(?P<content>.*?)(\$|\\\))')  # , flags=re.DOTALL
REGEX_SMALL_SECTIONS = OrderedDict(
    [
        ('header', REGEX_MARKDOWN_HEADER),
        ('img', REGEX_MARKDOWN_IMG),
        ('literal-inline', REGEX_MARKDOWN_LITERAL_INLINE),
        ('latex-inline', REGEX_MARKDOWN_LATEX_INLINE),
    ]
)

SECTION_ABBREV = {
    'table': ('Table', 'Tbl'),
    'latex': ('Equation', 'Eq'),
    'literal': ('Listing', 'Lit'),
    'code': ('Code', 'Cd'),
    'img': ('Figure', 'Fig'),
    # doesnt really come up
    'comment': ('Comment', 'Cmt'),
    'yaml': ('YAML', 'YML'),
    'quote': ('Quote', 'Qt'),
    'list': ('List', 'Lst'),
    'any': ('Any', 'Any'),
    'literal-inline': ('Literal', 'Lit'),
    'latex-inline': ('LaTeX', 'LaT'),
}

# https://www.freecodecamp.org/news/how-to-write-a-regular-expression-for-a-url/
REGEX_URL = re.compile(
    r'(https:\/\/www\.|http:\/\/www\.|https:\/\/|http:\/\/)[a-zA-Z]{2,}(\.[a-zA-Z]{2,})(\.[a-zA-Z]{2,})?\/[a-zA-Z0-9]{2,}|((https:\/\/www\.|http:\/\/www\.|https:\/\/|http:\/\/)[a-zA-Z]{2,}(\.[a-zA-Z]{2,})(\.[a-zA-Z]{2,})?)|(https:\/\/www\.|http:\/\/www\.|https:\/\/|http:\/\/)[a-zA-Z0-9]{2,}\.[a-zA-Z0-9]{2,}\.[a-zA-Z0-9]{2,}(\.[a-zA-Z0-9]{2,})?'
)
# REGEX_URL = re.compile(r'(https?:\/\/)[a-z0-9\-\_\.]{3,}\/?[A-Za-z0-9\-\_\.\/\?\=\&]*')


def analyze_sections(md_content, regex_dict, include_between=True):
    # find large sections then smaller sections and so on.
    sections = [
        # ('yaml', 'whatever', mo)
        # ('code', 'whatever', mo)
        # ('latex', 'whatever', mo)
    ]
    # these regexes define entire sections at a time and everything else in between is peanuts
    while md_content:
        md_content = md_content.strip()
        mos = [(k, regex.search(md_content)) for k, regex in regex_dict.items()]
        mos = sorted(mos, key=lambda tpl: 999999 if not tpl[1] else tpl[1].start())
        section, first_mo = mos[0]
        if first_mo:
            start, end = first_mo.span()
            if start == 0:
                content = md_content[:end]
                sections.append((section, content, first_mo))
            else:
                # include the in-between the matches as "any"
                content = md_content[:start]
                if include_between:
                    sections.append(('any', content, None))
                content = md_content[start:end]
                sections.append((section, content, first_mo))
            md_content = md_content[end:]
        else:
            # dump the rest as "any"
            content = md_content
            if include_between:
                sections.append(('any', content, None))
            md_content = ''
    return sections


def analyze_extract_sections(md_content):
    # type: (str) -> Tuple[List[T_SECTION], str]
    sections = analyze_sections(md_content, REGEX_EXTRACT_SECTIONS, include_between=False)
    for _, content, _ in reversed(sections):
        md_content = md_content.replace(content, '')
    return sections, md_content


def analyze_large_sections(md_content):
    # type: (str) -> List[T_SECTION]
    return analyze_sections(md_content, REGEX_LARGE_SECTIONS)


def analyze_small_sections(md_content):
    # type: (str) -> List[T_SECTION]
    return analyze_sections(md_content, REGEX_SMALL_SECTIONS)


@dataclasses.dataclass
class MarkdownDoclet(object):
    section: str
    label: str = ''
    caption: str = ''
    content: str = ''
    appendix: bool = False
    mo: Optional[re.Match] = None
    data: dict = dataclasses.field(default_factory=lambda: {})


REGEX_CITATION_CONTENT = re.compile(r'[A-Za-z0-9\-_\.]+')
REGEX_CITATION_WRONG = re.compile(r'\[([^\[\]]+)\]')


def find_bad_citations(content):
    # type: (str) -> Tuple[List[str], List[str]]
    errors, warnings = [], []
    for mo in REGEX_CITATION_WRONG.finditer(content):
        start, end = mo.span()
        citation = content[start:end]
        if not REGEX_CITATION_CONTENT.match(citation):
            continue
        if '-' in citation:
            errors.append(f'BAD [] citation style {citation}, use <> style instead')
        else:
            warnings.append(f'possible bad [] citation style {citation}, use <> style instead')
    return errors, warnings


def sections_to_doclets(sections, md_filepath, output_dirpath=constants.TEMP_DIRPATH, auto_label_caption=False, use_angle_citations=False):
    # type: (List[T_SECTION], str, str, bool, bool) -> Tuple[List[MarkdownDoclet], Dict[str, str], List[Tuple[str, str]], List[str], List[str]]
    '''
    Description:
        - given the list of discovered big sections and the original markdown file
        - break them up into MarkdownDoclets (interdoc_labels, captions, other data)
            - download any images
    Returns:
        Tuple[List[MarkdownDoclet], Dict[str, str], List[str], List[str], List[str]]
            doclets, interdoc_labels, download_url_filepaths, errors, warnings
    '''
    original_md_content = read_text_file(md_filepath)
    md_relpath = os.path.relpath(md_filepath, os.getcwd())
    md_dirpath = pathlib.Path(dirpath(md_filepath))
    output_dirpath_pl = pathlib.Path(output_dirpath)

    errors, warnings = [], []
    doclets = [
        # ('yaml', '---asdf: whatever---', spellcheck='')
        # ('plain', 'asdfasdfasdf', spellcheck='asdfasdf')
        # ('comment', '---asdf: whatever---', spellcheck='')
        # ('table', '|||', caption='capt', label='asdf', spellcheck='')
        # ...
        # ('header', 'introduction', label='introduction', spellcheck='introduction')
        # ...
        # ('header', 'introduction', label='introduction', spellcheck='introduction', appendix=True)
    ]
    appendix = False
    interdoc_labels = {}
    section_freq = {}
    download_url_filepaths = []
    while sections:
        section, md_content, mo = sections.pop(0)

        if section != 'comment':
            for url_mo in REGEX_URL.finditer(md_content):
                start = url_mo.start()
                if md_content[start - 1] != '(':
                    end = start + 64
                    endline = md_content.find('\n', start) - 1
                    end = min([end, endline])
                    lineno = list(find_lineno_index(md_content[start:end].strip(), original_md_content))[0][0]
                    errors.append(f'naked url! enclose with []()! lineno {lineno} {md_content[start:end]}...')

        if appendix:
            appendix = False  # switch it back off, we JUST turned it on for someone else
        data = {}
        content = md_content
        label = ''
        caption = ''
        groups = []
        groupdict = {}
        if mo is not None:
            groups = mo.groups()
            groupdict = mo.groupdict()
        if section != 'any':
            if section in set(['table', 'code', 'latex', 'quote', 'literal']):
                if section not in section_freq:
                    section_freq[section] = 0
                section_freq[section] += 1

                default_label = ''
                default_caption = ''
                if auto_label_caption:
                    tpl = SECTION_ABBREV.get(section, ('', ''))
                    default_caption = f'{tpl[0]}-{section_freq[section]}'
                    default_label = f'{tpl[1].lower()}-{section_freq[section]}'

                caption = groupdict.get('caption', '') or default_caption
                label = groupdict.get('label', '') or default_label
                content = groupdict.get('content', '') or ''

                if section in set(['quote']):
                    # NOTE: starting from the very first > to the last...
                    content = REGEX_CAPTION_LABEL_COMMON.sub('', md_content)
                elif section in set(['latex']):
                    # $$  # 301 gets caught as the label...
                    # 301 = 03~ 00~ 01 = 0000~0011, 0000~0000, 0000~0001
                    # $$
                    if r'\label' not in md_content and groupdict.get('label', ''):
                        label = default_label
                        bad_label = groupdict.get('label', '') or ''
                        content = f'{bad_label}{content}'

                if not content:
                    raise RuntimeError('could not determine content?!')
                lineno = list(find_lineno_index(md_content.strip(), original_md_content))[0][0] + 1

                if not label and section not in set(['literal', 'quote']):
                    example = 'label: something-or-other'
                    if section in set(['latex']):
                        example = '%\\label{something-or-other}, note the % comment is for markdown purposes.'
                    errors.append(f'{section} missing "{example}" at "{md_relpath}", lineno {lineno}!\n{indent(md_content[:64])}...')
                if not caption and section not in set(['latex', 'literal', 'quote']):
                    # caption is also required for these
                    errors.append(f'{section} missing "caption: Something or Other" at "{md_relpath}", lineno {lineno}!\n{indent(md_content[:64])}...')

                if label:
                    if label.startswith('label:'):
                        label = label[6:].strip()
                if caption:
                    if caption.startswith('caption:'):
                        caption = caption[8:].strip()

                if section == 'code':
                    data['language'] = groupdict.get('language') or ''
                elif section == 'table':
                    content = f'|{content}|'  # NOTE: it omits the first and last pipe unfortunately

            # elif section in set(['list']):
            #     content = md_content

            elif section in set(['yaml']):
                content = groups[0]

            if section not in set(['yaml', 'comment']) and use_angle_citations:
                # i know ahead of time that bad usage of citations is a bad look.
                cite_errors, cite_warnings = find_bad_citations(md_content)
                errors.extend(cite_errors)
                warnings.extend(cite_warnings)

            if label:
                if label in interdoc_labels:
                    errors.append(f'duplicate {section} label {label!r}')
                interdoc_labels[label] = section

            doclets.append(MarkdownDoclet(
                section=section,
                label=label,
                caption=caption,
                content=content,
                appendix=appendix,
                mo=mo,
                data=data,
            ))
        else:
            small_sections = analyze_small_sections(md_content)
            for section_sub, md_content_sub, mo_sub in small_sections:
                if appendix:
                    appendix = False  # switch it back off, we JUST turned it on for someone else

                if section_sub not in section_freq:
                    section_freq[section_sub] = 0
                section_freq[section_sub] += 1

                default_label = ''
                default_caption = ''
                if auto_label_caption:
                    tpl = SECTION_ABBREV.get(section_sub, ('', ''))
                    default_caption = f'{tpl[0]}-{section_freq[section_sub]}'
                    default_label = f'{tpl[1].lower()}-{section_freq[section_sub]}'

                label = default_label
                caption = default_caption
                data = {}
                lineno = list(find_lineno_index(md_content_sub.strip(), original_md_content))[0][0] + 1
                groupdict_sub = {}
                if mo_sub is not None:
                    groupdict_sub = mo_sub.groupdict()
                if section_sub == 'header':
                    octothorps = groupdict_sub.get('octothorps') or ''
                    title = groupdict_sub.get('title', '')

                    data['octothorps'] = octothorps
                    data['title'] = title

                    label = title[:]
                    if len(octothorps) > 4:
                        errors.append(f'headings > 4 not supported at "{md_relpath}", lineno {lineno}, {label!r}')
                        continue

                    if title.lower() == 'appendix':
                        appendix = True
                    label = '-'.join(label.split())
                elif section_sub == 'img':
                    caption = groupdict_sub.get('alt', '')
                    path = groupdict_sub.get('path', ')')[:-1]
                    if not path:
                        errors.append(f'img missing path\n{indent(md_content_sub)}')
                        continue
                    label = os.path.basename(path)
                    # label = re.sub(r'[^\w]', '', os.path.splitext(label)[0])
                    # label = '-'.join(label.split())

                    if output_dirpath:
                        if path.startswith('http'):
                            basename = path.split('/')[-1].split('?')[0]
                            dst_filepath = output_dirpath_pl / basename
                            download_url_filepaths.append((path, dst_filepath))
                        else:
                            src_filepath = md_dirpath / path
                            dst_filepath = output_dirpath_pl / os.path.basename(path)
                            download_url_filepaths.append((src_filepath, dst_filepath))

                        path = dst_filepath.name
                        data['path'] = path

                    path, ext = os.path.splitext(path)  # doesnt like extensions???
                    if ext.lower() in ['.svg']:
                        lineno = list(find_lineno_index(path, original_md_content))[0][0] + 1
                        raise RuntimeError(f'image src at "{path}" is using a forbidden extension "{ext}" at "{md_filepath}", lineno {lineno}, cannot proceed')
                elif section_sub == 'literal-inline':
                    pass
                elif section_sub == 'latex-inline':
                    pass

                elif section_sub == 'any':
                    if use_angle_citations:
                        # i know ahead of time that bad usage of citations is a bad look.
                        cite_errors, cite_warnings = find_bad_citations(md_content_sub)
                        errors.extend(cite_errors)
                        warnings.extend(cite_warnings)

                else:
                    raise NotImplementedError(f'subsection {section_sub!r} not anticipated')

                if label:
                    if label in interdoc_labels:
                        errors.append(f'duplicate {section_sub} label {label!r}')
                    interdoc_labels[label] = section_sub

                doclets.append(MarkdownDoclet(
                    section=section_sub,
                    label=label,
                    caption=caption,
                    content=md_content_sub,
                    appendix=appendix,
                    mo=mo_sub,
                    data=data,
                ))

    return doclets, interdoc_labels, download_url_filepaths, errors, warnings


def markdown_to_doclets(md_filepath, output_dirpath=constants.TEMP_DIRPATH, auto_label_caption=True):
    # type: (str, str, bool) -> Tuple[List[MarkdownDoclet], Dict[str, str], List[Tuple[str, str]], List[str], List[str]]
    '''
    Description:
        Given some markdown text, dom-ify it basically.
        Each doclet is a self-contained section of the original markdown and can be recombined into the original as well
        interdoc_labels is about recognizing all of the anchors and navigation points in the markdown
        download_url_filepaths contains all of the (url, filepath) that could be downloaded based on the markdown
        errors/warnings are opinionated errors and warnings, both are disregardable.

    Arguments:
        md_filepath: str
            take a markdown document, file or string
        output_dirpath: str
            used to calculate destination filepaths for your detected images
        auto_label_caption: bool
            automatically add tables, figures, code, etc. to the dict of anchors

    Returns:
        Tuple[List[MarkdownDoclet], Dict[str, str], List[Tuple[str, str]], List[str], List[str]]
            doclets, interdoc_labels, download_url_filepaths, errors, warnings
                List[MarkdownDoclet] - doclets
                Dict[str, str] - interdoc_labels
                List[Tuple[str, str]] - download_url_filepaths
                List[str] - errors
                List[str] - warnings
    '''
    md_content = read_text_file(md_filepath)

    # sections
    sections, md_content = analyze_extract_sections(md_content)
    sections += analyze_large_sections(md_content)

    # doclets
    doclets, interdoc_labels, download_url_filepaths, errors, warnings = sections_to_doclets(
        sections, md_filepath, output_dirpath=output_dirpath, auto_label_caption=auto_label_caption
    )
    return doclets, interdoc_labels, download_url_filepaths, errors, warnings
