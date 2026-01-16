#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
Author:         Chris Carl
Email:          chrisbcarl@outlook.com
Date:           2026-01-16
Description:

core.lib.stdlib.http is not really about adding stuff, more like demoing http.server and customizing it to demo server requirements
core.lib are modules that contain code that is about (but does not modify) the library. somewhat referential to core.functor and core.types.

Examples:
    python -m chriscarl.core.lib.stdlib.http
    python -c "from chriscarl.core.lib.stdlib.urllib import get; print(get('http://localhost:8000').body)"

Updates:
    2026-01-16 - core.lib.stdlib.http - initial commit
'''

# stdlib imports
from __future__ import absolute_import, print_function, division, with_statement  # , unicode_literals
import os
import sys
import logging
import json
import datetime
import argparse
import urllib.parse
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from typing import Optional, Any, Dict

# third party imports

# project imports
from chriscarl.core.lib.stdlib.argparse import ArgparseNiceFormat
from chriscarl.core.lib.stdlib.logging import configure_ez

SCRIPT_RELPATH = 'chriscarl/core/lib/stdlib/http.py'
if not hasattr(sys, '_MEIPASS'):
    SCRIPT_FILEPATH = os.path.abspath(__file__)
else:
    SCRIPT_FILEPATH = os.path.abspath(os.path.join(sys._MEIPASS, SCRIPT_RELPATH))  # pylint: disable=no-member
SCRIPT_DIRPATH = os.path.dirname(SCRIPT_FILEPATH)
SCRIPT_NAME = os.path.splitext(os.path.basename(__file__))[0]
THIS_MODULE = sys.modules[__name__]
LOGGER = logging.getLogger(__name__)
LOGGER.addHandler(logging.NullHandler())

# project imports

MAX_BYTES = 10 * 1024 * 1024  # 10MB


class ExampleRequestHandler(BaseHTTPRequestHandler):

    def respond(self, status_code=200, headers=None, drained=False, **body_kwargs):
        # type: (int, Optional[Dict[str, str]], bool, Any) -> None
        '''
        Description:
            Not overloaded, custom func that lumps all the usual response stuff together
        '''
        LOGGER.info('%s %s:%d', self.command, *self.client_address)
        LOGGER.debug('%s %s:%d, %s', self.command, *self.client_address, json.dumps(dict(self.headers), indent=2))
        payload = {}
        if not drained:
            try:
                # NOTE: this section demonstrates that its all bytes anyway.
                #   if you have a better encoding mechanism...
                #   JUST DO THAT...
                raw = self.drain()
                if raw:
                    # take a b'key=value' => [('key', 'value')]
                    content = urllib.parse.parse_qsl(raw.decode('utf-8'))
                    payload.update(content)
            except Exception:
                LOGGER.info('%s %s:%d - 400 - Bad Request, could not read content as json', self.command, *self.client_address, exc_info=True)
                self.send_error(400, message='Bad Request', explain='could not read content as json')
                return

        self.send_response(status_code)

        # %H:%M:%S - for the test cases, just day is fine, that way you can compare put to post and they're the same
        body_dict = dict(now=datetime.datetime.now().strftime('%Y-%m-%d'), payload=payload, **body_kwargs)
        body_text = json.dumps(body_dict).encode("utf-8")

        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(body_text)))
        headers = headers or {}
        for k, v in headers.items():
            self.send_header(k, v)
        self.end_headers()

        self.wfile.write(body_text)

    def route(self, headers=None, drained=False, **body_kwargs):
        # type: (Optional[Dict[str, str]], bool, Any) -> None
        '''
        Description:
            Not overloaded, custom func that lumps all the usual stuff together.
            NOTE: you can see here how Flask improves on this model.
                - with http.server and BasicHTTPRequestHandler, you have to define all your routes here
                - but you define all your methods elsewhere... not intuitive.
        '''
        tokens = self.path.split('?')
        path = tokens[0]
        query = tokens[1] if len(tokens) > 1 else None
        if not path or path == '/':
            self.respond(status_code=200, headers=headers, drained=drained, path=path, query=query, **body_kwargs)
        else:
            self.respond(status_code=404, headers=headers, drained=drained, error=f'{path} invalid!', query=query, **body_kwargs)

    def drain(self, max_bytes=MAX_BYTES):
        # type: (int) -> bytes
        '''
        Description:
            ChatGPT: "Read and discard any request body (if Content-Length is provided), so clients that reuse connections don't get stuck."
            ChatGPT seems to think this is popular.
            ASP.NET Core mentions it, but I cant see it in other Python literature.
                - https://learn.microsoft.com/en-us/aspnet/core/fundamentals/servers/kestrel/request-draining?view=aspnetcore-10.0
        '''
        length = self.headers.get("Content-Length")
        if not length:
            return bytes()
        try:
            n = int(length)
        except ValueError:
            return bytes()
        if n <= 0:
            return bytes()
        return self.rfile.read(min(n, max_bytes))

    def do_GET(self):
        body = '<p>hello, world!</p>'
        self.send_response(200)
        self.send_header("Allow", "GET, POST, PUT, DELETE, OPTIONS")
        self.send_header("Content-Type", "text/html; charset=utf-8")
        # self.send_header("Content-Encoding", "gzip")  # this one is not gziped...
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body.encode('utf8'))

    def do_POST(self):
        self.route()

    def do_PUT(self):
        self.route()

    def do_DELETE(self):
        self.route()

    def do_OPTIONS(self):
        # type: () -> None
        '''
        Description:
            Overloaded from BaseHTTPRequestHandler, methods and routes are separated (unlike in Flask)...
        Returns:
            None
        '''
        self.drain()
        extra = {
            "Allow": "GET, POST, PUT, DELETE, OPTIONS",
            # Optional browser-friendly headers:
            "Access-Control-Allow-Methods": "GET, POST, PUT, DELETE, OPTIONS",
            "Access-Control-Allow-Origin": "*",
            "Access-Control-Allow-Headers": self.headers.get("Access-Control-Request-Headers", "Content-Type"),
        }
        self.route(headers=extra, drained=True)

    def send_error(self, code, message=None, explain=None):
        # type: (int, Optional[str], Optional[str]) -> None
        '''
        Description:
            Overloaded from BaseHTTPRequestHandler
            in THIS case I'm not doing anything that needs adjusting
        Returns:
            None
        '''
        return super().send_error(code, message=message, explain=explain)

    def log_message(self, format, *args):
        # type: (int, str, Any) -> None
        '''
        Description:
            Overloaded from BaseHTTPRequestHandler
        Returns:
            None
        '''
        LOGGER.info(format, *args)


HOSTNAME = '127.0.0.1'
PORT = 8000


def launch_example_server(hostname=HOSTNAME, port=PORT):
    # type: (str, int) -> None
    server = ThreadingHTTPServer((hostname, port), ExampleRequestHandler)
    LOGGER.info('Serving on http://%s:%d/  (Ctrl+C to stop)', hostname, port)
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        LOGGER.info('ctrl + c detected')
    finally:
        server.server_close()


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Single-route JSON timestamp server (http.server).", formatter_class=ArgparseNiceFormat)
    parser.add_argument('--hostname', default=HOSTNAME)
    parser.add_argument('--port', type=int, default=PORT)
    args = parser.parse_args()

    configure_ez(level='DEBUG')
    launch_example_server(hostname=args.hostname, port=args.port)
