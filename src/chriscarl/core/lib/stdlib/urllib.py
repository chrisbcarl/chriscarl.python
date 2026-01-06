#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
Author:         Chris Carl
Email:          chrisbcarl@outlook.com
Date:           2026-01-06
Description:

core.lib.stdlib.urllib is where I stash most of my learnings on how to download things w/o requests
core.lib are modules that contain code that is about (but does not modify) the library. somewhat referential to core.functor and core.types.

Updates:
    2026-01-06 - core.lib.stdlib.urllib - initial commit
'''

# stdlib imports
from __future__ import absolute_import, print_function, division, with_statement  # , unicode_literals
import os
import sys
import logging
import ssl
import threading
import multiprocessing
import concurrent.futures
import urllib
import urllib.request
from urllib.parse import urljoin, urlparse
from typing import List, Optional, Callable

# third party imports

# project imports
from chriscarl.core.lib.stdlib.os import abspath

SCRIPT_RELPATH = 'chriscarl/core/lib/stdlib/urllib.py'
if not hasattr(sys, '_MEIPASS'):
    SCRIPT_FILEPATH = os.path.abspath(__file__)
else:
    SCRIPT_FILEPATH = os.path.abspath(os.path.join(sys._MEIPASS, SCRIPT_RELPATH))  # pylint: disable=no-member
SCRIPT_DIRPATH = os.path.dirname(SCRIPT_FILEPATH)
SCRIPT_NAME = os.path.splitext(os.path.basename(__file__))[0]
THIS_MODULE = sys.modules[__name__]
LOGGER = logging.getLogger(__name__)
LOGGER.addHandler(logging.NullHandler())


def get_basename(uri):
    # type: (str) -> str
    up = urlparse(uri)
    if not up.path:
        return up.hostname.split('www.')[1]
    return up.path.split('/')[-1]


def get_filepath(uri, dirpath, flat=False):
    # type: (str, str, bool) -> str
    up = urlparse(uri)
    hostname = up.hostname.split('www.')[-1]
    tokens = [hostname] + up.path.split('/')
    if flat:
        if tokens[-1]:
            filepath = abspath(dirpath, tokens[-1])
        else:
            filepath = abspath(dirpath, hostname)
    else:
        filepath = abspath(dirpath, *tokens)
    return filepath


def create_internet_shortcut(uri, dirpath):
    # type: (str, str) -> str
    basename = get_basename(uri)
    internet_shortcut_filepath = abspath(dirpath, f'{basename}.url')
    internet_shortcut = f'''[InternetShortcut]
URL={uri}'''
    with open(internet_shortcut_filepath, 'w', encoding='utf-8') as w:
        w.write(internet_shortcut)

    return internet_shortcut_filepath


HEADERS = {
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/143.0.0.0 Safari/537.36 Edg/143.0.0.0',
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
    'accept-encoding': 'gzip, deflate, br, zstd',
    'accept-language': 'en-US,en;q=0.9',
    'cache-control': 'no-cache;max-age=0',
    'connection': 'keep-alive',
    'pragma': 'no-cache',
}
SSL_BASIC_CTX = ssl.create_default_context()
SSL_BASIC_CTX.check_hostname = False
SSL_BASIC_CTX.verify_mode = ssl.CERT_NONE


def download(uri, dirpath, flat=True, exist_skip=False, context=SSL_BASIC_CTX, stop_event=None):
    # type: (str, str, bool, bool, ssl.SSLContext, threading.Event) -> str
    filepath = get_filepath(uri, dirpath, flat=flat)
    if exist_skip and os.path.isfile(filepath):
        return filepath
    dirpath = os.path.dirname(filepath)
    os.makedirs(dirpath, exist_ok=True)
    logging.debug('downloading %s to "%s"', uri, filepath)
    req = urllib.request.Request(uri, headers=HEADERS)  # NECESSARY so that it appears browser-ish
    with urllib.request.urlopen(req, context=context) as response, open(filepath, 'wb') as wb:
        wb.write(response.read())
    return filepath


def download_pool(urls, dirpath=None, flat=False, downloader=download, workers=multiprocessing.cpu_count() - 2):
    # type: (List[str], Optional[str], bool, Callable[[str, str, bool, bool, ssl.SSLContext, threading.Event], bool], int) -> int
    '''
    Description:
        Efficiently download using a pool
    Arguments:
        urls: List[str]
        dirpath: str
        flat: bool
            default False
            if flat, only use the basenames of urls as the filename
            otherwise, use the url path as subdirectories
        workers: int
            number of workers
    Returns:
        int:    number of failures
    '''
    with concurrent.futures.ThreadPoolExecutor(max_workers=workers) as executor:
        future_to_url = {}
        for url in urls:
            future = executor.submit(downloader, url, dirpath=dirpath, flat=flat, exist_skip=True)
            future_to_url[future] = url

        results = []
        finished = 0
        for future in concurrent.futures.as_completed(future_to_url):
            url = future_to_url[future]
            finished += 1
            try:
                results.append(future.result())
                logging.debug('%d / %d succeeded!', finished, len(future_to_url))
            except Exception:
                failures += 1
                logging.error('%d / %d failed!', finished, len(future_to_url))
                logging.debug('%d / %d failed!', finished, len(future_to_url), exc_info=True)
    return results
