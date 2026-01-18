r'''
2026-01-16
OpenAI ChatGPT 5.2-Pro:
    Create a web server application using the http.server module in Python.
    The web server has only 1 route, the root route at "/", which accepts all RESTful HTTP methods including GET, POST, PUT, DELETE, and OPTIONS.
    The body of all responses is a JSON dictionary with the current timestamp.
NOTE:
    - 4 mins 45 sec
'''
#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
from datetime import datetime, timezone
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from urllib.parse import urlparse


class TimestampHandler(BaseHTTPRequestHandler):
    """
    Single-route server:
      - Route: /
      - Methods: GET, POST, PUT, DELETE, OPTIONS
      - Response body: {"timestamp": "<UTC ISO-8601>"}
    """

    def _timestamp_body(self) -> bytes:
        payload = {"timestamp": datetime.now(timezone.utc).isoformat()}
        return json.dumps(payload, separators=(",", ":"), ensure_ascii=False).encode("utf-8")

    def _drain_request_body(self, max_bytes: int = 10 * 1024 * 1024) -> None:
        """
        Read and discard any request body (if Content-Length is provided),
        so clients that reuse connections don't get stuck.
        """
        length = self.headers.get("Content-Length")
        if not length:
            return
        try:
            n = int(length)
        except ValueError:
            return
        if n <= 0:
            return
        self.rfile.read(min(n, max_bytes))

    def _send_json(self, status: int = 200, extra_headers: dict[str, str] | None = None) -> None:
        body = self._timestamp_body()
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        if extra_headers:
            for k, v in extra_headers.items():
                self.send_header(k, v)
        self.end_headers()
        self.wfile.write(body)

    def _handle_root(self) -> None:
        self._drain_request_body()
        path = urlparse(self.path).path
        if path != "/":
            self.send_error(404)
            return
        self._send_json(200)

    # Root route supports the required methods.
    def do_GET(self) -> None:
        self._handle_root()

    def do_POST(self) -> None:
        self._handle_root()

    def do_PUT(self) -> None:
        self._handle_root()

    def do_DELETE(self) -> None:
        self._handle_root()

    def do_OPTIONS(self) -> None:
        self._drain_request_body()
        path = urlparse(self.path).path
        if path != "/":
            self.send_error(404)
            return

        extra = {
            "Allow": "GET, POST, PUT, DELETE, OPTIONS",
            # Optional browser-friendly headers:
            "Access-Control-Allow-Methods": "GET, POST, PUT, DELETE, OPTIONS",
            "Access-Control-Allow-Origin": "*",
            "Access-Control-Allow-Headers": self.headers.get("Access-Control-Request-Headers", "Content-Type"),
        }
        self._send_json(200, extra_headers=extra)

    # Ensure *all* responses (including errors) are JSON with a timestamp.
    def send_error(self, code: int, message: str | None = None, explain: str | None = None) -> None:
        self._send_json(status=code)

    # Silence default stderr logging (optional).
    def log_message(self, fmt: str, *args) -> None:
        return


def main() -> None:
    parser = argparse.ArgumentParser(description="Single-route JSON timestamp server (http.server).")
    parser.add_argument("--host", default="127.0.0.1")
    parser.add_argument("--port", type=int, default=8000)
    args = parser.parse_args()

    # ThreadingHTTPServer handles concurrent connections using threads. :contentReference[oaicite:1]{index=1}
    server = ThreadingHTTPServer((args.host, args.port), TimestampHandler)

    print(f"Serving on http://{args.host}:{args.port}/  (Ctrl+C to stop)")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass
    finally:
        server.server_close()


if __name__ == "__main__":
    main()
r'''
Google Gemini 3 Pro:
    Create a web server application using the http.server module in Python.
    The web server has only 1 route, the root route at "/", which accepts all RESTful HTTP methods including GET, POST, PUT, DELETE, and OPTIONS.
    The body of all responses is a JSON dictionary with the current timestamp.
NOTE:
    - doesnt work out of the box if you supply w/ params
    - you have to parse self.path.

'''
from http.server import HTTPServer, BaseHTTPRequestHandler
import json
import time

# Define the server address and port
HOST = "127.0.0.1"
PORT = 8000


class TimestampHandler(BaseHTTPRequestHandler):
    """
    Custom handler to return a JSON timestamp for specific HTTP methods.
    """

    def _send_timestamp_response(self):
        # Strictly handle only the root path "/"
        if self.path != '/':
            self.send_error(404, "Not Found")
            return

        # Prepare the JSON body
        response_data = {'timestamp': time.time()}
        response_body = json.dumps(response_data).encode('utf-8')

        # Send Status Code
        self.send_response(200)

        # Send Headers
        self.send_header('Content-Type', 'application/json')
        self.send_header('Content-Length', str(len(response_body)))
        self.end_headers()

        # Write the body to the output stream
        self.wfile.write(response_body)

    # Map all required RESTful methods to the helper function
    def do_GET(self):
        self._send_timestamp_response()

    def do_POST(self):
        self._send_timestamp_response()

    def do_PUT(self):
        self._send_timestamp_response()

    def do_DELETE(self):
        self._send_timestamp_response()

    def do_OPTIONS(self):
        self._send_timestamp_response()


if __name__ == "__main__":
    server = HTTPServer((HOST, PORT), TimestampHandler)
    print(f"Server started http://{HOST}:{PORT}")

    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nServer stopping...")
        server.server_close()
