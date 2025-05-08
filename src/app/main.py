"""Точка входа в приложение."""

import logging

from server import run_server

if __name__ == "__main__":
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s [%(levelname)s] %(message)s"
    )
    logging.info("Запуск приложения...")
    run_server()
    logging.info("Приложение завершено.")
