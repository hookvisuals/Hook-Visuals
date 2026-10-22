#!/usr/bin/env python3
"""Lokaler Server für den Akquise-Briefgenerator – OHNE Caching, MIT Range-Support.

- Cache-Header auf "nicht cachen" → jeder Reload holt die aktuelle Datei.
- HTTP-Range-Requests (206 Partial Content) → Audio kann springen/fortsetzen
  (nötig, damit die Hintergrundmusik nach einem Reload an der Stelle weitermacht).
- Threaded → Audio-Streaming blockiert nicht die übrigen Anfragen.
"""
import sys
import os
import re
import http.server

PORT = int(sys.argv[1]) if len(sys.argv) > 1 else 8000


class Handler(http.server.SimpleHTTPRequestHandler):
    def end_headers(self):
        self.send_header('Cache-Control', 'no-store, no-cache, must-revalidate, max-age=0')
        self.send_header('Pragma', 'no-cache')
        self.send_header('Expires', '0')
        self.send_header('Accept-Ranges', 'bytes')
        super().end_headers()

    def log_message(self, *args):
        pass  # keine Server-Logs im Terminal

    def do_GET(self):
        rng = self.headers.get('Range')
        if not rng:
            return super().do_GET()

        path = self.translate_path(self.path)
        if os.path.isdir(path) or not os.path.isfile(path):
            return super().do_GET()

        try:
            fsize = os.path.getsize(path)
            m = re.match(r'bytes=(\d*)-(\d*)', rng.strip())
            if not m:
                return super().do_GET()
            g1, g2 = m.group(1), m.group(2)
            if g1 == '':                      # "bytes=-N" → letzte N Bytes
                length = int(g2 or 0)
                start = max(0, fsize - length)
                end = fsize - 1
            else:
                start = int(g1)
                end = int(g2) if g2 else fsize - 1
            if start >= fsize or start > end:
                self.send_response(416)
                self.send_header('Content-Range', 'bytes */%d' % fsize)
                self.end_headers()
                return
            end = min(end, fsize - 1)
            length = end - start + 1
            self.send_response(206)
            self.send_header('Content-Type', self.guess_type(path))
            self.send_header('Content-Range', 'bytes %d-%d/%d' % (start, end, fsize))
            self.send_header('Content-Length', str(length))
            self.end_headers()
            with open(path, 'rb') as f:
                f.seek(start)
                remaining = length
                while remaining > 0:
                    chunk = f.read(min(65536, remaining))
                    if not chunk:
                        break
                    try:
                        self.wfile.write(chunk)
                    except (BrokenPipeError, ConnectionResetError):
                        break
                    remaining -= len(chunk)
        except Exception:
            try:
                self.send_error(500)
            except Exception:
                pass


# ThreadingHTTPServer: mehrere Anfragen parallel (Seite + Audio-Stream gleichzeitig)
server = http.server.ThreadingHTTPServer
server.allow_reuse_address = True
server.daemon_threads = True
with server(("", PORT), Handler) as httpd:
    httpd.serve_forever()
