"""Create a simple HTTP server to handle requests for the tennis scoreboard app."""

import json
import logging
import os
from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import urlparse

from controllers import MatchController
from dotenv import load_dotenv
from jinja2 import Environment, FileSystemLoader

# Зависит от PYTHONPATH=src/app
from models.database import SessionLocal

# Загружаем .env
load_dotenv()

# Получаем настройки из .env
SERVER_HOST = os.getenv("SERVER_HOST", "localhost")
SERVER_PORT = int(os.getenv("SERVER_PORT", 8000))

# Настраиваем Jinja2
env = Environment(loader=FileSystemLoader("src/app/templates"))

# Настраиваем логирование
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s"
)

# Добавляем кастомные фильтры
def from_json(value):
    """Преобразовать JSON-строку в словарь."""
    return json.loads(value) if value else {}

def get_score(score_dict):
    """Получить счёт в формате 'player1:player2'."""
    return f"{score_dict.get('player1', 0)}:{score_dict.get('player2', 0)}"

env.filters["from_json"] = from_json
env.filters["get_score"] = get_score

class TennisScoreboardHandler(BaseHTTPRequestHandler):
    """HTTP handler for the tennis scoreboard app."""

    def do_GET(self):  # noqa: N802
        """Handle GET requests."""
        logging.info(f"GET {self.path}")
        parsed_url = urlparse(self.path)
        path = parsed_url.path

        db = SessionLocal()
        try:
            controller = MatchController(db)
            if path == "/matches":
                matches = controller.get_all_matches()
                template = env.get_template("matches.html")
                self.send_response(200)
                self.send_header("Content-type", "text/html")
                self.end_headers()
                self.wfile.write(template.render(matches=matches).encode())
                logging.info("Отправлен список матчей")
            else:
                self.send_response(404)
                self.end_headers()
                logging.warning(f"Страница не найдена: {self.path}")
        except Exception as e:
            logging.error(f"Ошибка при обработке GET: {e}")
            self.send_response(500)
            self.end_headers()
        finally:
            db.close()

    def do_POST(self):  # noqa: N802
        """Handle POST requests."""
        logging.info(f"POST {self.path}")
        parsed_url = urlparse(self.path)
        path = parsed_url.path

        content_length = int(self.headers["Content-Length"])
        post_data = self.rfile.read(content_length)
        data = json.loads(post_data.decode())

        db = SessionLocal()
        try:
            controller = MatchController(db)
            if path == "/new-match":
                match = controller.create_match(
                    data["player1_name"],
                    data["player2_name"]
                )
                self.send_response(201)
                self.send_header("Content-type", "application/json")
                self.end_headers()
                self.wfile.write(json.dumps(match.to_dict()).encode())
                logging.info(f"Создан новый матч: {match}")

            elif path == "/match-score":
                match = controller.update_score(
                    data["uuid"],
                    data["player_id"],
                    data["points"]
                )
                self.send_response(200)
                self.send_header("Content-type", "application/json")
                self.end_headers()
                self.wfile.write(json.dumps(match.to_dict()).encode())
                logging.info(f"Обновлён счёт матча: {match}")

            else:
                self.send_response(404)
                self.end_headers()
                logging.warning(f"Страница не найдена: {self.path}")
        except Exception as e:
            logging.error(f"Ошибка при обработке POST: {e}")
            self.send_response(500)
            self.end_headers()
        finally:
            db.close()

def run_server():
    """Run the HTTP server."""
    server_address = (SERVER_HOST, SERVER_PORT)
    httpd = HTTPServer(server_address, TennisScoreboardHandler)
    logging.info(f"Starting server on {SERVER_HOST}:{SERVER_PORT}...")
    httpd.serve_forever()

if __name__ == "__main__":
    run_server()
