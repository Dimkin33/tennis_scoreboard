"""Запуск HTTP-сервера с поддержкой шаблонов Jinja2 в отдельном потоке."""
import http.server
import json
import socketserver
import threading
from urllib.parse import urlparse

from jinja2 import Environment, FileSystemLoader

PORT = 8000
TEMPLATE_DIR = "templates"

# Настройка Jinja2
env = Environment(loader=FileSystemLoader(TEMPLATE_DIR))


class CustomHandler(http.server.SimpleHTTPRequestHandler):
    """Обработчик HTTP-запросов с поддержкой API и шаблонов."""

    def __init__(self, *args, **kwargs):
        """Инициализация обработчика."""
        super().__init__(*args, directory=TEMPLATE_DIR, **kwargs)

    def do_GET(self):  # noqa: N802
        """Обработка GET-запросов."""
        parsed_path = urlparse(self.path)
        path = parsed_path.path

        if path == '/' or path == '':
            self.path = 'index.html'
            super().do_GET()
        elif path.startswith('/api/'):
            self.handle_api()
        elif path == '/favicon.ico':
            self.send_response(204)
            self.end_headers()
        else:
            super().do_GET()

    def handle_api(self):
        """Обработка API-запросов."""
        self.send_response(200)
        self.send_header("Content-type", "application/json")
        self.end_headers()
        response = {"message": "API endpoint not implemented"}
        self.wfile.write(json.dumps(response).encode())


def run_server():
    """Запуск HTTP-сервера."""
    with socketserver.TCPServer(("", PORT), CustomHandler) as httpd:
        print(f"Serving at http://localhost:{PORT}")
        httpd.serve_forever()


# Запуск сервера в отдельном потоке
server_thread = threading.Thread(target=run_server, daemon=True)
server_thread.start()

# Можно выполнять другие задачи здесь
input("Сервер запущен. Нажмите Enter для завершения...\n")
