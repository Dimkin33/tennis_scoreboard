import http.server
import socketserver
import os
import json
from jinja2 import Environment, FileSystemLoader
from urllib.parse import urlparse, parse_qs

PORT = 8000
TEMPLATE_DIR = "templates"

# Настройка Jinja2
env = Environment(loader=FileSystemLoader(TEMPLATE_DIR))

class CustomHandler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=TEMPLATE_DIR, **kwargs)

    def do_GET(self):
        parsed_path = urlparse(self.path)
        path = parsed_path.path

        if path.startswith('/api/'):
            self.handle_api()
        elif path.endswith('.html'):
            self.handle_template(path)
        else:
            super().do_GET()

    def handle_template(self, path):
        try:
            # Убираем начальный слеш
            template_path = path.lstrip('/')
            template = env.get_template(template_path)
            # Пример данных (замените на реальные)
            data = {
                "title": "Tennis Scoreboard",
                "message": "Welcome to the Tennis Scoreboard!"
            }
            content = template.render(**data)
            self.send_response(200)
            self.send_header("Content-type", "text/html")
            self.end_headers()
            self.wfile.write(content.encode())
        except Exception as e:
            self.send_error(500, f"Template error: {str(e)}")

    def handle_api(self):
        self.send_response(200)
        self.send_header("Content-type", "application/json")
        self.end_headers()
        response = {"message": "API endpoint not implemented"}
        self.wfile.write(json.dumps(response).encode())

with socketserver.TCPServer(("", PORT), CustomHandler) as httpd:
    print(f"Serving at http://localhost:{PORT}")
    httpd.serve_forever()
