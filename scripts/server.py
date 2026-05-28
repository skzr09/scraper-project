
# server.py
#   Simple HTTP Server for serving HTML files
#   Usage:
#       python server.py

import http.server
import socketserver
import os

PORT = 8000

# Change to data directory to serve HTML files
os.chdir(os.path.join(os.path.dirname(__file__), '..', 'data'))

Handler = http.server.SimpleHTTPRequestHandler

with socketserver.TCPServer(("", PORT), Handler) as httpd:
    print(f"Serving at http://localhost:{PORT}")
    httpd.serve_forever()
