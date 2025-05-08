"""Модуль для работы с базой данных SQLite с использованием SQLAlchemy."""

import os

from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Загружаем переменные из .env
load_dotenv()

# Создаём базовый класс для моделей SQLAlchemy
Base = declarative_base()

# Настраиваем подключение к SQLite базе данных
DATABASE_URL = os.getenv("DATABASE_URL")
engine = create_engine(DATABASE_URL, echo=False)

# Создаём фабрику сессий для работы с базой
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
