import http.server
import socketserver
import os
import json
from urllib.parse import urlparse

PORT = 8000
TEMPLATE_DIR = "templates"

class CustomHandler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=TEMPLATE_DIR, **kwargs)

    def do_GET(self):
        parsed_path = urlparse(self.path)
        path = parsed_path.path

        if path == '/' or path == '':
            # Перенаправляем корневой путь на index.html
            self.path = '/index.html'
            super().do_GET()
        elif path.startswith('/api/'):
            self.handle_api()
        elif path == '/favicon.ico':
            # Пустой ответ для favicon.ico
            self.send_response(204)
            self.end_headers()
        else:
            super().do_GET()

    def handle_api(self):
        self.send_response(200)
        self.send_header("Content-type", "application/json")
        self.end_headers()
        response = {"message": "API endpoint not implemented"}
        self.wfile.write(json.dumps(response).encode())

with socketserver.TCPServer(("", PORT), CustomHandler) as httpd:
    print(f"Serving at http://localhost:{PORT}")
    httpd.serve_forever()
