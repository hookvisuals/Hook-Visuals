#!/usr/bin/env python3
"""Lokaler Server für den Akquise-Briefgenerator – OHNE Caching.

Der Standard-Server (python3 -m http.server) schickt keine Cache-Header, weshalb
Safari/Chrome beim normalen Reload oft die ALTE Datei aus dem Cache anzeigen.
Dieser Server setzt bei jeder Antwort „nicht cachen" – so holt jeder Reload
garantiert die aktuelle Version.
"""
import sys
import http.server
import socketserver

PORT = int(sys.argv[1]) if len(sys.argv) > 1 else 8000


class NoCacheHandler(http.server.SimpleHTTPRequestHandler):
    def end_headers(self):
        self.send_header('Cache-Control', 'no-store, no-cache, must-revalidate, max-age=0')
        self.send_header('Pragma', 'no-cache')
        self.send_header('Expires', '0')
        super().end_headers()

    def log_message(self, *args):
        pass  # keine Server-Logs im Terminal


socketserver.TCPServer.allow_reuse_address = True
with socketserver.TCPServer(("", PORT), NoCacheHandler) as httpd:
    httpd.serve_forever()
