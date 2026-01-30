#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
Author:         Chris Carl
Email:          chrisbcarl@outlook.com
Date:           2026-01-06
Description:

core.lib.stdlib.urllib is where I stash most of my learnings on how to download things w/o requests
core.lib are modules that contain code that is about (but does not modify) the library. somewhat referential to core.functor and core.types.

Examples:
    python -m chriscarl.core.lib.stdlib.http
    python -c "from chriscarl.core.lib.stdlib.urllib import get; print(get('http://localhost:8000').body)"

Updates:
    2026-01-16 - core.lib.stdlib.urllib - download can return just the text now and handle file:///
                 core.lib.stdlib.urllib - added RESTful methods
    2026-01-13 - core.lib.stdlib.urllib - fixed bugs where the return type wasnt tuple and wasnt tested as tuple
    2026-01-07 - core.lib.stdlib.urllib - download augmented to deal with edge cases like Wikipedia of all places
    2026-01-06 - core.lib.stdlib.urllib - initial commit
'''

# stdlib imports
from __future__ import absolute_import, print_function, division, with_statement  # , unicode_literals
import os
import sys
import logging
import re
import time
import random
import ssl
import json
import threading
import contextlib
import dataclasses
import multiprocessing
import concurrent.futures
import urllib.error
import urllib.request
import urllib.parse
from urllib.parse import urlparse
from typing import List, Optional, Callable, Tuple, Dict, Any

# third party imports

# project imports
from chriscarl.core import constants
from chriscarl.core.lib.stdlib.os import abspath
from chriscarl.core.lib.stdlib.io import read_text_file, read_text_file_try, write_text_file
from chriscarl.core.lib.stdlib.typing import isinstance_raise

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


def get_basename(url):
    # type: (str) -> str
    up = urlparse(url)
    if not up.path:
        if not up.hostname:
            raise ValueError(f'cannot get basename for a url without a hostname like {url!r}')
        return up.hostname.split('www.')[-1]
    return up.path.split('/')[-1]


def get_filepath(url, dirpath=constants.TEMP_DIRPATH, flat=False):
    # type: (str, str, bool) -> str
    url = url.replace('\\', '/')  # file:///C:\temp is valid
    up = urlparse(url)
    if not up.hostname and up.scheme != 'file':
        raise ValueError(f'cannot get filepath for a url without a hostname like {url!r}')
    if up.hostname:
        hostname = up.hostname.split('www.')[-1]
    else:
        # scheme == 'file'
        hostname = 'localhost'
    tokens = [hostname] + up.path.split('/')
    if flat:
        if tokens[-1]:
            filepath = abspath(dirpath, tokens[-1])
        else:
            filepath = abspath(dirpath, hostname)
    else:
        filepath = abspath(dirpath, *tokens)
    return filepath


def create_internet_shortcut(url, dirpath):
    # type: (str, str) -> str
    basename = get_basename(url)
    internet_shortcut_filepath = abspath(dirpath, f'{basename}.url')
    internet_shortcut = f'''[InternetShortcut]
URL={url}'''
    write_text_file(internet_shortcut_filepath, internet_shortcut)

    return internet_shortcut_filepath


HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/143.0.0.0 Safari/537.36 Edg/143.0.0.0',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
    'Accept-Encoding': 'gzip, deflate, br, zstd',
    'Accept-Language': 'en-US,en;q=0.9',
    'Cache-Control': 'max-age=0',
    'Connection': 'keep-alive',
    'Pragma': 'no-cache',
    'Sec-Fetch-Dest': 'document',
    'Sec-Fetch-Mode': 'navigate',
    'Sec-Fetch-Site': 'none',
    'Sec-Fetch-User': '?1',
    'Upgrade-Insecure-Requests': '1',
    'sec-ch-ua': '"Microsoft Edge";v="143", "Chromium";v="143", "Not A(Brand";v="24"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
}
SSL_BASIC_CTX = ssl.create_default_context()
SSL_BASIC_CTX.check_hostname = False
SSL_BASIC_CTX.verify_mode = ssl.CERT_NONE
WEB_FILENAME_EXTENSIONS = set(
    [
        # https://www.geeksforgeeks.org/techtips/web-page-file-formats/
        '.html',
        '.htm',
        '.php',
        '.xhtml',  # (Extensible Hypertext Markup Language): An XML-based version of HTML
        '.asp',  # (.asp): One of these includes Active Server Pages [ASP] which is a server side script written by Microsoft. These are not meant for users, they comprise of server side code that gets delivered to a browser after processing by the ABS.:%.* These are among some of the commonly utilized in Windows based web hosting setups.
        '.aspx',  # (Active Server Pages Extended): An extension of ASP that supports .NET framework
        '.rss',  # (Really Simple Syndication): A web feed format
        '.xps',  # (.xps): XML-based file format
    ]
)


def download_method_0(url, filepath, context=SSL_BASIC_CTX, headers=HEADERS, is_a='link'):
    # type: (str, str, ssl.SSLContext, dict, str) -> Tuple[bool, str]
    LOGGER.debug('method 0 on %s to "%s"', url, filepath)
    dirpath = os.path.dirname(filepath)
    os.makedirs(dirpath, exist_ok=True)
    req = urllib.request.Request(url, headers=headers)  #
    try:
        # NOTE: PRIMARY, handles MOST cases.
        #   fails: wikipedia
        #       - https://upload.wikimedia.org/wikipedia/commons/thumb/e/ec/Mona_Lisa%2C_by_Leonardo_da_Vinci%2C_from_C2RMF_retouched.jpg/960px-Mona_Lisa%2C_by_Leonardo_da_Vinci%2C_from_C2RMF_retouched.jpg
        try_again = False
        try:
            urllib.request.urlretrieve(url, filepath)  # works most of the time, but we need the response.url
            if is_a == 'link':
                try:
                    content = read_text_file_try(filepath)
                    try_again = re.search(r'<body.+?body>', content, flags=re.DOTALL | re.MULTILINE) is None
                except UnicodeDecodeError:
                    try_again = True
        except urllib.error.HTTPError as he:
            if he.code in {404, 403}:
                raise he
            try_again = True

        with urllib.request.urlopen(req, context=context) as response:
            # shutil.copyfileobj(response, wb)  # also doesnt work all the time
            # BUG: https://www.marxists.org/archive/marx/works/download/index.htm
            url = response.url  # NOTE: we need to know this change... it could have been changed on access, like adding a / or full redirect name
            if try_again:
                body = response.read()
                with open(filepath, 'wb') as wb:
                    wb.write(body)  # doesnt work all the time, not sure why
        if is_a == 'link':
            try:
                content = read_text_file_try(filepath)
                try_again = re.search(r'<body.+?body>', content, flags=re.DOTALL | re.MULTILINE) is None
            except UnicodeDecodeError:
                try_again = True
            if try_again:
                raise RuntimeError(f'{url} which is a {is_a} could not be read as HTML!')
    except urllib.error.HTTPError as he:
        if he.code in {404, 403}:
            raise he
        LOGGER.debug('%s reason: %r, status code: %d', url, he.reason, he.code)
        LOGGER.debug('%s response headers: %s', url, he.hdrs)

        return False, url

    return True, url


def download_method_1(url, filepath, context=SSL_BASIC_CTX, headers=HEADERS):
    # type: (str, str, ssl.SSLContext, dict) -> Tuple[bool, str]
    # NOTE: SECONDARY, handles direct files just fine, not web page themselves for some reason...
    #   fails (output is malformed): index htmls
    #       - https://pypi.org/simple/six/
    # NOTE: https://stackoverflow.com/a/46511429
    LOGGER.debug('method 1 on %s to "%s"', url, filepath)
    dirpath = os.path.dirname(filepath)
    os.makedirs(dirpath, exist_ok=True)

    handler = urllib.request.HTTPSHandler(context=context)
    opener = urllib.request.build_opener(handler)
    opener.addheaders = [(k, v) for k, v in headers.items()]  # NECESSARY so that it appears browser-ish
    # urllib.request.install_opener(opener)

    # NOTE: C:\Python312\Lib\urllib\request.py, ripoff of urlretrieve
    with contextlib.closing(opener.open(url, data=None)) as response, open(filepath, 'wb') as wb:
        # headers = response.info()  # normally you'd check total read vs size = int(headers["Content-Length"])
        # BUG: https://www.marxists.org/archive/marx/works/download/index.htm
        url = response.url  # NOTE: we need to know this change... it could have been changed on access, like adding a / or full redirect name
        bs = 1024 * 8
        # size = -1
        read = 0
        blocknum = 0
        # if "content-length" in headers:
        #     size = int(headers["Content-Length"])
        while block := response.read(bs):  # WARNING: 3.8+ assignment operator and usage, loop ends when block == 0
            read += len(block)
            wb.write(block)
            blocknum += 1

    return True, url


def download(
    url,
    dirpath=constants.TEMP_DIRPATH,
    filepath=None,
    is_a='file',
    flat=True,
    skip_exist=False,
    skip_sleep=False,
    context=SSL_BASIC_CTX,
    stop_event=None,
    headers=HEADERS,
    as_body=False,
):
    # type: (str, str, Optional[str], str, bool, bool, bool, ssl.SSLContext, Optional[threading.Event], dict, bool) -> Tuple[str, str]
    '''
    Returns:
        Tuple[str, str]
            filepath, url
    '''
    global URLLIB_PRIOR_CONTEXT, URLLIB_OPENER
    if not isinstance(filepath, str):
        filepath = get_filepath(url, dirpath, flat=flat)
        if skip_exist and os.path.isfile(filepath):
            return filepath, url
        if os.path.isdir(filepath) or is_a == 'link':
            filepath = f'{filepath}.html'
    filepath = abspath(filepath)
    LOGGER.debug('downloading %s to "%s"', url, filepath)

    if is_a == 'file':
        _, url = download_method_1(url, filepath)
    else:
        worked, url = download_method_0(url, filepath, context=context, headers=headers, is_a=is_a)
        if not worked:
            LOGGER.debug('error attempting to download_method_0 %s, trying fallback...', url)
            _, url = download_method_1(url, filepath, context=context, headers=headers)

    if not skip_sleep:
        time.sleep(random.randint(0, 3690) / 1000)
    if as_body:
        filepath = read_text_file(filepath)
    return filepath, url


def download_pool(urls, dirpath=None, flat=False, skip_exist=False, skip_sleep=False, downloader=download, workers=multiprocessing.cpu_count() - 2):
    # type: (List[str], Optional[str], bool, bool, bool, Callable[[str, str, str, bool, bool, bool, ssl.SSLContext, Optional[threading.Event], dict], Tuple[str, str]], int) -> Tuple[List[str], int]
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
        skip_exist: bool
            default False
            if exists on disk, do not download
        skip_sleep: bool
            default False
            skip the random up to 3.69 second delay inbetween submitting files to be downloaded
        workers: int
            number of workers
    Returns:
        Tuple[List[str], int]
            List[str]:  downloaded filepaths
            int:        number of failures
    '''
    with concurrent.futures.ThreadPoolExecutor(max_workers=workers) as executor:
        future_to_url = {}
        for url in urls:
            future = executor.submit(downloader, url, is_a='file', dirpath=dirpath, flat=flat, skip_exist=skip_exist, skip_sleep=skip_sleep)
            future_to_url[future] = url

        results = []
        failures = 0
        finished = 0
        for future in concurrent.futures.as_completed(future_to_url):
            url = future_to_url[future]
            finished += 1
            if finished % 25 == 0:
                LOGGER.info('%d / %d - %0.2f%%', finished, len(future_to_url), finished / len(future_to_url) * 100)
            try:
                filepath, _ = future.result()  # updated_url
                results.append(filepath)
                LOGGER.debug('%d / %d - %s succeeded!', finished, len(future_to_url), url)
            except Exception:
                failures += 1
                LOGGER.error('%d / %d - %s failed!', finished, len(future_to_url), url)
                LOGGER.debug('%d / %d - %s failed!', finished, len(future_to_url), url, exc_info=True)
    return results, failures


@dataclasses.dataclass
class Response():
    method: str = ''
    url: str = ''
    status_code: int = -1
    headers: dict = dataclasses.field(default_factory=lambda: {})
    body: str | bytes = ''
    __json = None

    @property
    def json(self):
        # type: () -> dict
        if not self.__json:
            self.__json = json.loads(self.body)
        return self.__json

    def to_dict(self):
        return dataclasses.asdict(self)

    def __str__(self):
        return f'{self.method} {self.url} - {self.status_code}'

    def __eq__(self, value):
        # type: (Any) -> bool
        if not isinstance(value, Response):
            return False
        else:
            return self.to_dict() == value.to_dict()


def request(method, url, data=None, headers=None, context=SSL_BASIC_CTX, decoding='utf-8'):
    # type: (str, str, Optional[dict], Optional[Dict[str, str]], ssl.SSLContext, str) -> Response
    LOGGER.debug('%s %s', method, url)
    headers = headers or {}
    isinstance_raise(headers, dict)
    data = data or {}
    isinstance_raise(data, dict)
    # take {'key': 'value'} => 'key=value'
    # NOTE: this section demonstrates that its all bytes anyway.
    #   if you have a better encoding mechanism...
    #   JUST DO THAT...
    data_encoded = urllib.parse.urlencode(data).encode('utf-8') if data else None
    req = urllib.request.Request(url, data=data_encoded, headers=headers, method=method)
    with urllib.request.urlopen(req, context=context) as r:
        response_headers = dict(r.headers)
        if response_headers.get('Transfer-Encoding') == 'chunked':
            ba = bytearray()
            chunk = r.read(8192)
            while chunk:
                ba += chunk
                chunk = r.read(8192)
            content = bytes(ba)
        else:
            content = r.read()
        resp = Response(
            method=method,
            url=url,
            status_code=r.code,
            headers=dict(r.headers),
            body=content if not decoding else content.decode(decoding),
        )
    LOGGER.debug(resp)
    return resp


def get(url, headers=HEADERS, context=SSL_BASIC_CTX, decoding='utf-8'):
    # type: (str, Optional[Dict[str, str]], ssl.SSLContext, str) -> Response
    return request('GET', url, headers=headers, context=context, decoding=decoding)


def post(url, data, headers=HEADERS, context=SSL_BASIC_CTX, decoding='utf-8'):
    # type: (str, dict, Optional[Dict[str, str]], ssl.SSLContext, str) -> Response
    return request('POST', url, data=data, headers=headers, context=context, decoding=decoding)


def put(url, data, headers=HEADERS, context=SSL_BASIC_CTX, decoding='utf-8'):
    # type: (str, dict, Optional[Dict[str, str]], ssl.SSLContext, str) -> Response
    return request('PUT', url, data=data, headers=headers, context=context, decoding=decoding)


def delete(url, data, headers=HEADERS, context=SSL_BASIC_CTX, decoding='utf-8'):
    # type: (str, dict, Optional[Dict[str, str]], ssl.SSLContext, str) -> Response
    return request('DELETE', url, data=data, headers=headers, context=context, decoding=decoding)


def options(url, data=None, headers=HEADERS, context=SSL_BASIC_CTX, decoding='utf-8'):
    # type: (str, Optional[dict], Optional[Dict[str, str]], ssl.SSLContext, str) -> Response
    return request('OPTIONS', url, data=data, headers=headers, context=context, decoding=decoding)


def patch(url, data, headers=HEADERS, context=SSL_BASIC_CTX, decoding='utf-8'):
    # type: (str, dict, Optional[Dict[str, str]], ssl.SSLContext, str) -> Response
    return request('PATCH', url, data=data, headers=headers, context=context, decoding=decoding)


def head(url, data, headers=HEADERS, context=SSL_BASIC_CTX, decoding='utf-8'):
    # type: (str, dict, Optional[Dict[str, str]], ssl.SSLContext, str) -> Response
    return request('HEAD', url, data=data, headers=headers, context=context, decoding=decoding)
