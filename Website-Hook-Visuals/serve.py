import os
import http.server
import socketserver

os.chdir("/Users/lauramehler/Documents/GitHub/Hook-Visuals/Website-Hook-Visuals")

PORT = 3000
Handler = http.server.SimpleHTTPRequestHandler

with socketserver.TCPServer(("", PORT), Handler) as httpd:
    httpd.serve_forever()
