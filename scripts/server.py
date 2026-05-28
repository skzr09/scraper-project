"""
Run live localhost server
   Simple HTTP Server for serving HTML files
   Usage:
       python server.py
"""

import os
import http.server
import socketserver

PORT = 8001 # 8000 is being used for the api server

# Change to data directory to serve HTML files
os.chdir(os.path.join(os.path.dirname(__file__), '..', 'data'))

Handler = http.server.SimpleHTTPRequestHandler

with socketserver.TCPServer(("", PORT), Handler) as httpd:
    print(f"Serving at http://localhost:{PORT}")
    httpd.serve_forever()
