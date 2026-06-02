"""
Run live localhost server
   Simple HTTP Server for serving HTML files
Usage:
    python -m scripts.init_server
Notes:
    - This is used for testing the scraper against local HTML files.
    - Access the content at http://localhost:PORT/yourfile.html
    - The server will run indefinitely until you stop it (CTRL+C).
    (8000 port is used for the API server, so this will default to 8001)
"""

import os
import http.server
import socketserver

from config import config

def init_server():

    # Change to data directory to serve HTML files
    os.chdir(os.path.join(os.path.dirname(__file__), '..', 'data'))

    try:
        port = config.server.port
        Handler = http.server.SimpleHTTPRequestHandler

        with socketserver.TCPServer(("", port), Handler) as httpd:
            print("[INFO] Serving at http://localhost:{}".format(port))
            httpd.serve_forever()

    except Exception as e:
        print("[ERR ] Failed to start server: {}".format(e))


if __name__ == "__main__":
    init_server()
