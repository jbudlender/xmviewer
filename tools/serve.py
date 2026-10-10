#!/usr/bin/env python3
"""
Preview the site locally, the way GitHub Pages serves it (with HTTP range
requests, which the PMTiles files need). Standard library only.

    python3 tools/serve.py              # http://localhost:8000
    python3 tools/serve.py --lan        # also reachable from a phone on the same Wi-Fi
    python3 tools/serve.py --port 8001

Python's built-in `python3 -m http.server` does NOT support range requests, so
the map would stay empty with it.
"""

import os
import re
import socket
import sys
from http import HTTPStatus
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
RANGE = re.compile(r"bytes=(\d*)-(\d*)$")


class Handler(SimpleHTTPRequestHandler):
    def __init__(self, *a, **kw):
        super().__init__(*a, directory=str(ROOT), **kw)

    def log_message(self, *a):
        pass

    def end_headers(self):
        self.send_header("Accept-Ranges", "bytes")
        self.send_header("Cache-Control", "no-cache")
        super().end_headers()

    def do_GET(self):
        m = RANGE.match(self.headers.get("Range", ""))
        path = Path(self.translate_path(self.path))
        if not m or not path.is_file():
            return super().do_GET()
        size = path.stat().st_size
        start = int(m.group(1)) if m.group(1) else max(0, size - int(m.group(2)))
        end = int(m.group(2)) if m.group(1) and m.group(2) else size - 1
        end = min(end, size - 1)
        if start > end:
            self.send_response(HTTPStatus.REQUESTED_RANGE_NOT_SATISFIABLE)
            self.send_header("Content-Range", f"bytes */{size}")
            self.end_headers()
            return
        self.send_response(HTTPStatus.PARTIAL_CONTENT)
        self.send_header("Content-Type", self.guess_type(str(path)))
        self.send_header("Content-Range", f"bytes {start}-{end}/{size}")
        self.send_header("Content-Length", str(end - start + 1))
        self.end_headers()
        with open(path, "rb") as f:
            f.seek(start)
            self.wfile.write(f.read(end - start + 1))


def lan_ip() -> str:
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
        s.connect(("10.255.255.255", 1))        # picks the outgoing interface; sends nothing
        return s.getsockname()[0]


if __name__ == "__main__":
    port = int(sys.argv[sys.argv.index("--port") + 1]) if "--port" in sys.argv else 8000
    lan = "--lan" in sys.argv
    srv = ThreadingHTTPServer(("0.0.0.0" if lan else "127.0.0.1", port), Handler)
    print(f"Serving {ROOT} at http://localhost:{port}  (Ctrl+C to stop)", flush=True)
    if lan:
        print(f"On your phone (same Wi-Fi): http://{lan_ip()}:{port}", flush=True)
    try:
        srv.serve_forever()
    except KeyboardInterrupt:
        pass
