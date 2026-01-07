#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
Author:         Chris Carl
Email:          chrisbcarl@outlook.com
Date:           2024-11-25
Description:

tools.shed.dev is the "shed" in which all of the "tools" go to pick one up.
tool are modules that define usually cli tools or mini applets that I or other people may find interesting or useful.

Updates:
    2026-01-07 - tools.shed.dev - create_modules_and_tests added namespace so that __init__ doesnt get added and related tests are removed
    2026-01-05 - tools.shed.dev - audit_cov uses python -m instead of pytest alone
    2024-12-20 - tools.shed.dev - audit_banned now includes the filename, lol
    2024-12-11 - tools.shed.dev - audit_stubgen modified to make use of ast analysis and merging
                 tools.shed.dev - added pytest actual results to audit cov
    2024-12-04 - tools.shed.dev - FIX: manifest-modify wasnt handling nested folders correctly, now it does
                 tools.shed.dev - combined modify and verify as I probably should have done all along, jesus
    2024-11-28 - tools.shed.dev - added audit_clean, audit_stubs, audit_cov
    2024-11-27 - tools.shed.dev - added audit_banned and it works!
    2024-11-26 - tools.shed.dev - renamed from lib to shed since pytest got confused with multiple test_lib's
                 tools.shed.dev - added audit_tdd
                 tools.shed.dev - FIX: if a dir already exists for a module, no action is taken rather than making a file as well
    2024-11-25 - tools.lib.dev - initial commit

TODO:
    - clean up the argument names--cwd/dirpath/root_dirpath, module/module_name, its a mess.
'''

# stdlib imports
from __future__ import absolute_import, print_function, division, with_statement  # , unicode_literals
import os
import sys
import re
import pydoc
import logging
import importlib
import subprocess
import shutil
import ast
from typing import List, Union, Tuple, Callable, Any, Optional, Dict

# third party imports

# project imports
import chriscarl
from chriscarl.core.constants import DATE, REPO_DIRPATH
from chriscarl.core.functors.python import run_func_args_kwargs, get_legal_python_name
from chriscarl.core.functors.parse.pytest_coverage import PytestCoverage
from chriscarl.core.lib.stdlib.ast import merge_python
from chriscarl.core.lib.stdlib.io import read_text_file, write_text_file
from chriscarl.core.lib.stdlib.json import read_json
from chriscarl.core.lib.stdlib.os import make_dirpath, abspath, chdir, walk
from chriscarl.core.lib.stdlib.importlib import walk_dirpath_for_module_files
from chriscarl.core.lib.stdlib.re import find_lineno_colno
from chriscarl.core.lib.stdlib.subprocess import run, launch_editor
from chriscarl.files import manifest
from chriscarl.tools.shed.constants import IGNORED_DIRS

SCRIPT_RELPATH = 'chriscarl/tools/shed/dev.py'
if not hasattr(sys, '_MEIPASS'):
    SCRIPT_FILEPATH = os.path.abspath(__file__)
else:
    SCRIPT_FILEPATH = os.path.abspath(os.path.join(sys._MEIPASS, SCRIPT_RELPATH))  # pylint: disable=no-member
SCRIPT_DIRPATH = os.path.dirname(SCRIPT_FILEPATH)
SCRIPT_NAME = os.path.splitext(os.path.basename(__file__))[0]
THIS_MODULE = sys.modules[__name__]
LOGGER = logging.getLogger(__name__)
LOGGER.addHandler(logging.NullHandler())

STUB_OUTPUT_DIRPATH = 'dist/typing'


def create_modules_and_tests(
    root_module,
    modules,
    descriptions=None,
    author='',
    email='',
    tests_dirname='tests',
    cwd=os.getcwd(),
    force=False,
    tool=False,
    no_test=False,
    no_module=False,
    namespace=False,
    launch=False,
):
    # type: (str, List[str], Optional[dict], str, str, str, str, bool, bool, bool, bool, bool, bool) -> List[Tuple[str, str, str]]
    with chdir(cwd):
        descriptions = descriptions or read_json(manifest.FILEPATH_DEFAULT_DESCRIPTIONS_JSON)
        module_template = read_text_file(manifest.FILEPATH_TEMPLATE)
        test_template = read_text_file(manifest.FILEPATH_TEST_TEMPLATE)
        tool_template = read_text_file(manifest.FILEPATH_TOOL_TEMPLATE)
        mod_lib_template = read_text_file(manifest.FILEPATH_MOD_LIB_TEMPLATE)
        created_type_module_filepaths: List[Tuple[str, str, str]] = []
        namespaced_module = ''
        src_dirname = 'src'
        warnings = 0
        for m, module in enumerate(modules):
            if module.startswith(root_module):
                raise ValueError('you provided root module {} and module {}, you dont need the root in the 2nd.'.format(root_module, module))

        for m, module in enumerate(modules):
            tokens = [root_module] + module.split('.')  # ['module', 'a', 'b']
            if namespace:
                namespaced_module = '.'.join(tokens[:-1])

            if no_module:
                LOGGER.warning('skipping module generation!')
            else:
                # create directories
                LOGGER.info('module %d / %d - %s - step 1 - directories', m, len(modules) - 1, module)
                for t, token in enumerate(tokens[:-1]):  # ['module', 'a']
                    directory = '{}/{}'.format(src_dirname, '/'.join(tokens[:t + 1]))
                    current_bad_relpath = '{}.py'.format(directory)
                    LOGGER.info('module %d / %d - %s - step 1 - directory from %r - "%s"!', m, len(modules) - 1, module, token, directory)
                    if os.path.isfile(current_bad_relpath):
                        LOGGER.warning(
                            'module %d / %d - %s - step 1 - directory from %r - "%s" is a file "%s"!', m,
                            len(modules) - 1, module, token, directory, current_bad_relpath
                        )
                        if force:
                            LOGGER.critical(
                                'module %d / %d - %s - step 1 - directory from %r - "%s" is a file "%s"! FORCING!', m,
                                len(modules) - 1, module, token, directory, current_bad_relpath
                            )
                            os.remove(current_bad_relpath)
                        else:
                            warnings += 1
                            continue
                    make_dirpath(directory)

                # create inits
                LOGGER.info('module %d / %d - %s - step 2 - __init__.py', m, len(modules) - 1, module)
                for t, token in enumerate(tokens[:-1]):  # ['module', 'a']
                    directory = '{}/{}'.format(src_dirname, '/'.join(tokens[:t + 1]))
                    module_so_far = '.'.join(tokens[:t + 1])
                    current_init_relpath = '{}/__init__.py'.format(directory)
                    if namespaced_module and module_so_far in namespaced_module:
                        doit = True
                        if os.path.isfile(current_init_relpath):
                            LOGGER.error(
                                'module %d / %d - %s - step 2 - __init__.py from %r - "%s" exists! remove namespace %r with --force!', m,
                                len(modules) - 1, module, token, current_init_relpath, namespaced_module
                            )
                            if force:
                                LOGGER.critical(
                                    'module %d / %d - %s - step 2 - __init__.py from %r - "%s" already exists! FORCING REMOVAL to conform to namespace %r!', m,
                                    len(modules) - 1, module, token, current_init_relpath, namespaced_module
                                )
                            else:
                                doit = False
                                warnings += 1
                                continue
                        else:
                            doit = False
                        if doit:
                            os.remove(current_init_relpath)

                    else:
                        LOGGER.info('module %d / %d - %s - step 2 - __init__.py from %r - "%s"', m, len(modules) - 1, module, token, current_init_relpath)
                        doit = True
                        if os.path.isfile(current_init_relpath):
                            LOGGER.warning('module %d / %d - %s - step 2 - __init__.py from %r - "%s" already exists!', m, len(modules) - 1, module, token, current_init_relpath)
                            if force:
                                LOGGER.critical(
                                    'module %d / %d - %s - step 2 - __init__.py from %r - "%s" already exists! FORCING!', m,
                                    len(modules) - 1, module, token, current_init_relpath
                                )
                            else:
                                doit = False
                                warnings += 1
                                continue
                        if doit:
                            write_text_file(current_init_relpath, '')
                            created_type_module_filepaths.append(('__init__', module_so_far, abspath(current_init_relpath)))

                # create module file
                module_relpath = '{}/{}.py'.format(src_dirname, '/'.join(tokens))
                module_bad_dirpath = '{}/{}'.format(src_dirname, '/'.join(tokens))
                if os.path.isdir(module_bad_dirpath):
                    LOGGER.warning(
                        'module %d / %d - %s - step 3 - module %r - "%s" exists as a dir not a module! Not removing or altering at all!', m,
                        len(modules) - 1, module, token, module_bad_dirpath
                    )
                    warnings += 1
                else:
                    LOGGER.info('module %d / %d - %s - step 3 - module', m, len(modules) - 1, module)
                    LOGGER.info('module %d / %d - %s - step 3 - module %r - "%s"', m, len(modules) - 1, module, token, module_relpath)
                    doit = True
                    if os.path.isfile(module_relpath):
                        LOGGER.warning('module %d / %d - %s - step 3 - module %r - "%s" exists!', m, len(modules) - 1, module, token, module_relpath)
                        if force:
                            LOGGER.critical('module %d / %d - %s - step 3 - module %r - "%s" exists! FORCING!', m, len(modules) - 1, module, token, module_relpath)
                        else:
                            doit = False
                            warnings += 1

                if doit:
                    description_key_length = -1
                    default_description = ''
                    for k, v in descriptions.items():
                        if k in module and len(k) > description_key_length:
                            description_key_length = len(k)
                            default_description = '{} are modules that {}'.format(k, v)

                    template_kwargs = dict(
                        author=author,
                        email=email,
                        module_dot_path=module,
                        date=DATE,
                        script_relpath=module_relpath.replace('src/', ''),
                    )
                    template = module_template
                    if module.startswith('mod.lib'):
                        template = mod_lib_template
                        template_kwargs.update(dict(shadow_module=tokens[-1], default_description=default_description))
                    elif tool:
                        template = tool_template
                    else:
                        stdlib_import, third_import = '', ''
                        if 'stdlib.' in module:
                            stdlib_import = '\nimport {}'.format(tokens[-1])
                        elif 'third.' in module:
                            third_import = '\nimport {}'.format(tokens[-1])
                        template_kwargs.update(dict(default_description=default_description, stdlib_import=stdlib_import, third_import=third_import))

                    content = template.format(**template_kwargs)
                    write_text_file(module_relpath, content)
                    created_type_module_filepaths.append(('module', '.'.join(tokens), abspath(module_relpath)))

            if no_test:
                LOGGER.warning('skipping test generation!')
            else:
                # create test directories
                LOGGER.info('module %d / %d - %s - step 4 - test directories', m, len(modules) - 1, module)
                test_root_directory = abspath(tests_dirname)
                tests_base = os.path.basename(test_root_directory)
                make_dirpath(test_root_directory)

                current_directory = os.path.relpath(test_root_directory, '').replace('\\', '/')
                for t, token in enumerate(tokens[:-1]):
                    current_directory = '{}/{}'.format(current_directory, token)
                    LOGGER.info('module %d / %d - %s - step 4 - test directories from %r - "%s"!', m, len(modules) - 1, module, token, current_directory)
                    make_dirpath(current_directory)

                # create tests
                LOGGER.info('module %d / %d - %s - step 5 - tests', m, len(modules) - 1, module)
                current_directory = os.path.relpath(test_root_directory, '').replace('\\', '/')
                for t, token in enumerate(tokens):
                    module_so_far = '.'.join(tokens[:t + 1])
                    test_relpath = '{}/test_{}.py'.format(current_directory, token)
                    # test_relpath = '{}/test_{}.py'.format(tests_base, module_so_far)
                    if namespaced_module and module_so_far in namespaced_module:
                        doit = True
                        if os.path.isfile(test_relpath):
                            LOGGER.error(
                                'module %d / %d - %s - step 5 - tests from %r - "%s" exists! remove namespace %r with --force!', m,
                                len(modules) - 1, module, token, current_init_relpath, namespaced_module
                            )
                            if force:
                                LOGGER.critical(
                                    'module %d / %d - %s - step 5 - tests from %r - "%s" already exists! FORCING REMOVAL to conform to namespace %r!', m,
                                    len(modules) - 1, module, token, current_init_relpath, namespaced_module
                                )
                            else:
                                doit = False
                                warnings += 1
                                continue
                        else:
                            doit = False
                        if doit:
                            os.remove(test_relpath)
                    else:
                        LOGGER.info('module %d / %d - %s - step 5 - tests from %r - "%s"!', m, len(modules) - 1, module, token, test_relpath)
                        doit = True
                        if os.path.isfile(test_relpath):
                            LOGGER.warning('module %d / %d - %s - step 5 - tests from %r - "%s" already exists!', m, len(modules) - 1, module, token, test_relpath)
                            if force:
                                LOGGER.critical('module %d / %d - %s - step 5 - tests from %r - "%s" already exists! FORCING!', m, len(modules) - 1, module, token, test_relpath)
                            else:
                                warnings += 1
                                doit = False

                        if doit:
                            test_module_dot_path = '{}.{}'.format(tests_base, module_so_far)
                            content = test_template.format(
                                author=author,
                                email=email,
                                date=DATE,
                                module_dot_path=module_so_far,
                                test_module_dot_path=test_module_dot_path,
                                script_relpath=test_relpath,
                            )
                            write_text_file(test_relpath, content)
                            created_type_module_filepaths.append(('test', module_so_far, abspath(test_relpath)))

                    current_directory = '{}/{}'.format(current_directory, token)

            if not no_test:
                LOGGER.info('test generated at:   "%s"', test_relpath)
                if launch:
                    launch_editor(test_relpath)
            if not no_module:
                LOGGER.info('module generated at: "%s"', module_relpath)
                if launch:
                    launch_editor(module_relpath)
        return created_type_module_filepaths


def run_functions_by_dot_path(root_module, func_names, print_help=False, log_level='DEBUG'):
    # type: (str, List[str], bool, Union[str, int]) -> int
    try:
        full_names = ['{}.{}'.format(root_module, func_name) for func_name in func_names]
        funcs: List[Union[Callable, Tuple[Callable, Any]]] = []
        for full_name in full_names:
            tokens = full_name.split('.')
            module = importlib.import_module('.'.join(tokens[:-1]))
            func = getattr(module, tokens[-1])
            if print_help:
                funcs.append((pydoc.render_doc, (func, )))
            else:
                funcs.append(func)

        LOGGER.info('running %d funcs %s!', len(funcs), len(funcs))
        results = list(run_func_args_kwargs(funcs, log_level=log_level))  # type: ignore
        return 0 if all(results) else 1
    except ModuleNotFoundError as mnfe:
        LOGGER.error('could not find module %r based on provided root %r and funcs!', mnfe.name, root_module)
        LOGGER.debug('exception', exc_info=True)
        return 1
    except AttributeError as ae:
        LOGGER.error('%s, perhaps a mispelled or stale function name %r?', ' '.join(ae.args), ae.name)
        LOGGER.debug('exception', exc_info=True)
        return 2


def audit_manifest(no_modify=False, no_verify=False):
    # type: (bool, bool) -> int
    '''
    Description:
        update the files manifest
        run this to update the DIRPATH_* and FILEPATH_* constants that represent actual file paths
    '''
    if no_modify:
        LOGGER.info('skipping modifying "%s"', manifest.__file__)
    else:
        LOGGER.info('modifying "%s"', manifest.__file__)
        importlib.reload(manifest)
        manifest_filepath = abspath(manifest.__file__)
        with open(manifest_filepath, 'r', encoding='utf-8') as r:
            lines = r.read().splitlines()
            indexes = [l for l, line in enumerate(lines) if line.startswith('# ###')]

        with chdir(os.path.dirname(manifest.__file__)):
            tokens = []
            for d, _, fs in os.walk('./'):
                if '__pycache__' in d:
                    continue
                dirname = os.path.basename(d)
                dupper = dirname.upper()
                d_relpath = d.replace('\\', '/')
                tokens.append("# {}".format(d_relpath))
                if dupper:
                    tokens.append("DIRPATH_{} = os.path.join(SCRIPT_DIRPATH, '{}')".format(dupper, d_relpath))
                else:
                    dupper = 'ROOT'
                    tokens.append("DIRPATH_ROOT = SCRIPT_DIRPATH")
                for f in fs:
                    if '__init__' in f:
                        continue
                    pname = get_legal_python_name(f)
                    tokens.append("FILEPATH_{} = os.path.join(DIRPATH_{}, '{}')".format(pname.upper(), dupper, f))

                tokens.append("")

        new_content = lines[0:indexes[0]] + ['# ###\n'] + tokens + lines[indexes[1]:]
        LOGGER.info('writing %d lines of filepath content', len(tokens))
        with open(manifest_filepath, 'w', encoding='utf-8') as w:
            w.write('\n'.join(new_content))

    # check each of the DIRPATH_* and FILEPATH_* actually exist...
    if no_verify:
        LOGGER.info('skipping verifying "%s"', manifest.__file__)
    else:
        LOGGER.info('verifying "%s"', manifest.__file__)
        importlib.reload(manifest)
        lcls = dict(vars(manifest))
        for k, v in lcls.items():
            if k.startswith('DIRPATH') and not os.path.isdir(v):
                raise OSError('dir {} at "{}" does not exist!'.format(k, v))
        for k, v in lcls.items():
            if k.startswith('FILEPATH') and not os.path.isfile(v):
                raise OSError('file {} at "{}" does not exist!'.format(k, v))

    return 0


SCRIPT_RELPLATH_REGEX = re.compile(r"SCRIPT_RELPATH = r?'[\d\w\-\\\/\.]+\.py'")
DEFAULT_EXTENSIONS = ['.py']


def audit_relpath(dirpath=os.getcwd(), extensions=DEFAULT_EXTENSIONS, included_dirs=None, ignored_dirs=IGNORED_DIRS, dry=False):
    # type: (str, List[str], Optional[List[str]], List[str], bool) -> int
    '''
    Description:
        find every file that contains        SCRIPT_RELPATH = 'chriscarl/tools/shed/dev.py'
        and convert them into something like SCRIPT_RELPATH = 'chriscarl/tools/shed/dev.py'

    Arguments:
        dirpath: str
            where do we start crawling?
        extensions: List[str]
            which files should we look at?
        included_dirs: List[str]
            any directories that you do care about, and run them relatively to dirpath?
        ignored_dirs: List[str]
            any directories you dont care about?
        dry: bool
            do not write?
    '''
    with chdir(dirpath):
        original_dirpath = abspath(dirpath)
        LOGGER.debug('going through "%s"...', original_dirpath)
        extensions = extensions or []
        chars = 128  # if verbose else 16
        changes = 0

        for filepath in walk(original_dirpath, extensions=extensions, include=included_dirs, ignore=ignored_dirs, case_insensitive=True):
            LOGGER.debug('"%s"', filepath)
            basename = os.path.basename(filepath)
            relpath = os.path.relpath(filepath, original_dirpath).replace('\\', '/')
            if 'src/' in relpath:
                relpath = relpath.replace('src/', '')
            with open(filepath) as r:
                contents = r.read()
            search = SCRIPT_RELPLATH_REGEX.search(contents)
            LOGGER.debug('%s: "%s"', 'something' if bool(search) else 'notathing', filepath)
            if search:
                replacement = replacement_preview = "SCRIPT_RELPATH = '{}'".format(relpath)
                original = original_preview = search.string[search.start():search.end()]
                if len(original) > chars:
                    original_preview = original_preview[0:chars - 3] + '...'
                if len(replacement_preview) > chars:
                    replacement_preview = replacement_preview[0:chars - 3] + '...'

                if replacement != original_preview:
                    LOGGER.debug('replacing %s %r %r', relpath, replacement, original_preview)
                    lines = contents[:search.end()].splitlines()
                    lineno = len(lines) + 1
                    charno = len(lines[-1])  # just a best effort
                    changes += 1
                    if not dry:
                        LOGGER.info('replacing %s %r -> %r', '{} [line:{}; char:{}]: '.format(basename, lineno, charno), original_preview, replacement_preview)
                        new_contents = SCRIPT_RELPLATH_REGEX.sub(replacement, contents)
                        with open(filepath, 'w') as w:
                            w.write(new_contents)
        LOGGER.info('%d changes', changes)
        if dry and changes > 0:
            LOGGER.warning('remember to remove --dry if youd like to flush these changes.')
        return 0


def audit_tdd(
    dirpath=REPO_DIRPATH,
    module_name=chriscarl.__name__,
    tests_dirname='tests',
    dry=True,
    author='',
    email='',
    descriptions=None,
    cwd=os.getcwd(),
    force=False,
    tool=False,
    no_test=False,
    no_module=False,
):
    # type: (str, str, str, bool, str, str, Optional[dict], str, bool, bool, bool, bool) -> int
    '''
    Description:
        check to see which files have a corresponding test, which files do not, and which tests are abandoned
        this wont work on non-pypa repo packages like installed or .pyc packaged packages.
    '''
    with chdir(dirpath):
        top_module_name = module_name
        src_to_test = {}
        src_to_file = {}
        test_to_src = {}
        test_to_file = {}
        # test_module_prepend = 'tests.test_'

        # non src/ convention
        for module_name, filepath in walk_dirpath_for_module_files(module_name):
            tokens = module_name.split('.')
            tokens[-1] = 'test_{}'.format(tokens[-1])
            test_module_tokens = [tests_dirname] + tokens
            test_module = '.'.join(test_module_tokens)
            # test_module = '{}{}'.format(test_module_prepend, module_name)
            src_to_test[module_name] = test_module
            src_to_file[module_name] = filepath
        # src convention
        for module_name, filepath in walk_dirpath_for_module_files('src/{}'.format(module_name)):
            tokens = module_name.split('.')
            tokens[-1] = 'test_{}'.format(tokens[-1])
            test_module_tokens = [tests_dirname] + tokens
            test_module = '.'.join(test_module_tokens)
            # test_module = '{}{}'.format(test_module_prepend, module_name)
            src_to_test[module_name] = test_module
            src_to_file[module_name] = filepath

        # test
        for module_name, filepath in walk_dirpath_for_module_files(tests_dirname):
            tokens = module_name.split('.')
            tokens[-1] = tokens[-1][5:]  # get rid of the test_ prepend
            src_module_tokens = tokens[1:]
            src_module = '.'.join(src_module_tokens)
            # src_module = module_name[len(test_module_prepend):]
            test_to_src[module_name] = src_module
            test_to_file[module_name] = filepath

    src_without_tests = set(k for k, v in src_to_test.items() if v not in test_to_src)
    orphaned_tests = set(test_to_file[k] for k, v in test_to_src.items() if v not in src_to_test)

    ret = 0
    create_these_modules = [x[len(top_module_name) + 1:] for x in sorted(src_without_tests)]

    if src_without_tests:
        LOGGER.info('recommendation: run the following command line:\n\n    dev create %s --module "%s"\n\n', ' '.join(create_these_modules), top_module_name)
        ret += len(src_without_tests)
        LOGGER.critical('%d src files detected without equivalent tests! %s', len(src_without_tests), sorted(src_without_tests))
    if orphaned_tests:
        LOGGER.info('recommendation: refactor and then remove with the following command lines:\n\n%s\n\n', '\n'.join('    rm "{}"'.format(ele) for ele in orphaned_tests))
        ret += len(orphaned_tests)
        LOGGER.critical('%d orphaned tests detected! %s', len(orphaned_tests), sorted(orphaned_tests))

    if dry:
        LOGGER.critical('skipping test creation for the %d modules that are missing them! pass dry=True to generate them!', len(create_these_modules))
    else:
        if len(create_these_modules) > 0:
            LOGGER.critical('creating tests for the %d modules that are missing them!', len(create_these_modules))
            results = create_modules_and_tests(
                top_module_name,
                create_these_modules,
                descriptions=descriptions or read_json(manifest.FILEPATH_DEFAULT_DESCRIPTIONS_JSON),
                author=author,
                email=email,
                tests_dirname=tests_dirname,
                cwd=cwd,
                force=force,
                tool=tool,
                no_test=no_test,
                no_module=no_module,
            )
            return len(results)
        else:
            LOGGER.info('%d modules are missing tests! good job.', len(create_these_modules))

    return ret


def audit_banned(root_dirpath, words, word_case_insensitive=True, extensions=None, ignore=IGNORED_DIRS, include=None, file_case_insensitive=True):
    # type: (str, List[str], bool, Optional[List[str]], Optional[List[str]], Optional[List[str]], bool) -> Dict[str, Dict[str, List[Tuple[int, int]]]]
    findings: Dict[str, Dict[str, List[Tuple[int, int]]]] = {}
    words = sorted(set(words))
    longest = 0
    hit = set()
    for relpath in walk(root_dirpath, extensions=extensions, ignore=ignore, include=include, case_insensitive=file_case_insensitive, relpath=True):
        if len(relpath) > longest:
            longest = len(relpath)
        try:
            contents = read_text_file(abspath(root_dirpath, relpath))
        except UnicodeDecodeError:
            LOGGER.warning('couldnt read file "%s" due to unicode decode error, likely not a real file', relpath)
            LOGGER.debug('exception', exc_info=True)
        file_findings = findings[relpath] = {}
        for word in words:
            if word in relpath:
                hit.add(word)
                if word not in file_findings:
                    file_findings[word] = []
                file_findings[word].append((0, 0))
                LOGGER.warning('File "%s" itself - %r matched!', relpath, lineno, colno, word)
            lineno_colno = list(find_lineno_colno(word, contents, case_insensitive=word_case_insensitive))
            if lineno_colno:
                hit.add(word)

            lineno_colno = list(find_lineno_colno(word, contents, case_insensitive=word_case_insensitive))
            if lineno_colno:
                hit.add(word)
                if word not in file_findings:
                    file_findings[word] = []
                file_findings[word].extend(lineno_colno)
                for lineno, colno in lineno_colno:
                    LOGGER.warning('File "%s", line %d, col %d - %r matched!', relpath, lineno, colno, word)
        if not file_findings:
            del findings[relpath]
    hits = sum(len(v) for v in findings.values())
    if hits > 0:
        LOGGER.error('encountered %d hits of %d banned words among %d files! banned: %s', hits, len(hit), len(findings), sorted(hit))
    else:
        LOGGER.info('clean as a whistle')
    return findings


def audit_stubs(dirpath=REPO_DIRPATH, module_name=chriscarl.__name__, output_dirpath=STUB_OUTPUT_DIRPATH):
    # type: (str, str, str) -> int
    '''
    Description:
        generate .pyi files that contain type hints. in the case of MY module, it will also create augmented typehints for the shadow modules
        modeled after this command which can be run at any time:
            stubgen src/chriscarl -o dist/typing
    '''
    with chdir(dirpath):
        dist_typing = abspath(dirpath, output_dirpath)
        if os.path.isdir(dist_typing):
            LOGGER.info('removing stale typings in "%s"', dist_typing)
            shutil.rmtree(dist_typing)
        os.makedirs(output_dirpath)
        root_src_directory = 'src/{}'.format(module_name)
        cmd = ['stubgen', root_src_directory, '-o', output_dirpath]
        exit_code = subprocess.check_call(cmd, cwd=dirpath)

        # if module_name != chriscarl.__name__:
        #     LOGGER.info('skipping shadow module feature that is exclusive to %r', chriscarl.__name__)
        #     return exit_code

        LOGGER.info('generating shadow module stub files that are exclusive to %r', chriscarl.__name__)
        modded_libs = abspath(dist_typing, module_name, 'mod/lib')
        generated = 0
        for src in walk(modded_libs, extensions=['.pyi'], ignore=['__init__']):
            name = os.path.splitext(os.path.basename(src))[0]
            dst = abspath(dist_typing, name, '__init__.pyi')
            LOGGER.debug('generating stub file for module %r', name)

            cmd = ['stubgen', '-m', name, '-o', output_dirpath]
            subprocess.check_call(cmd, cwd=dirpath)

            l_python, r_python = read_text_file(dst), read_text_file(src)
            # remove imports like these: (from logging import * | import logging)
            r_python = '\n'.join(line for line in r_python.splitlines() if 'from {}'.format(name) not in line and 'import {}'.format(name) not in line)
            m_python = merge_python(l_python, r_python)
            write_text_file(dst, m_python)
            LOGGER.debug('merged to to stub file "%s" from "%s"', dst, src)
            generated += 1
        LOGGER.info('generated %d shadow module stub files', generated)

    return exit_code


def audit_clean(dirpath=REPO_DIRPATH):
    # type: (str) -> int
    '''
    Description:
        clean up the repository, mostly means .pyc files
    '''
    with chdir(dirpath):
        pycs = 0
        for pyc in walk(dirpath, extensions=['.pyc']):
            try:
                os.remove(pyc)
                pycs += 1
            except OSError:
                LOGGER.error('unable to remove pyc "%s"', pyc)
                LOGGER.debug('traceback', exc_info=True)
        LOGGER.info('removed %d pycs', pycs)

    return pycs


def audit_cov(dirpath=REPO_DIRPATH, module=chriscarl.__name__, tests_dirname='tests', threshold=0.69):
    # type: (str, str, str, float) -> int
    '''
    Description:
        run pytest coverage and call out anything below a certain threshold
        modeled after this command which can be run at any time:
            python -m pytest --cov=chriscarl tests --cov-report term-missing
            python -m pytest --cov=chriscarl.core.types tests/chriscarl/core/types --cov-report term-missing
        WARNING: sometimes running just pytest gives you "Fatal error in launcher: Unable to create process using"
            solve with python -m
    '''
    with chdir(dirpath):
        cmd = ['python', '-m', 'pytest', '--cov={}'.format(module), '{}/'.format(tests_dirname), '--cov-report', 'term-missing']
        _, output = run(cmd, cwd=dirpath)

    for line in output.splitlines():
        print(line)

    below = [pc for pc in PytestCoverage.parse_coverage(output) if pc.cover < threshold]
    failed = PytestCoverage.parse_tests(output, tests_dirname=tests_dirname)
    if below:
        LOGGER.warning('encountered %d items below the %0.2f%% threshold!', len(below), threshold)
        for pc in below:
            LOGGER.warning('"%s" (%d%%)', pc.name, pc.cover * 100)
            for missing in pc.missing:
                LOGGER.warning('    "%s", line %s', pc.name, missing)
        LOGGER.warning('encountered %d items below the %0.2f%% threshold!', len(below), threshold)
    else:
        LOGGER.info('encountered %d items below the %0.2f%% threshold!', len(below), threshold)

    if failed:
        LOGGER.error('%d items outright failed!', len(failed))
        for filepath, lineno, exc in failed:
            LOGGER.error('"%s", line %d w/ %r', filepath, lineno, exc)
    else:
        LOGGER.info('0 items outright failed!')

    return len(below)
