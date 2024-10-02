import os

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv


# Настройки базы данных.
# Загружаем переменные окружения из .env файла
load_dotenv()
DATABASE_URL = os.getenv("DATABASE_URL")

# Использование SQLite в памяти для тестирования
SQLALCHEMY_TEST_DATABASE_URL = "sqlite:///:memory:"

# Создание SQLAlchemy движка и сессии.
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()  # declarative_base()


def get_db(testing=False):
    global engine
    if testing:
        engine = create_engine(SQLALCHEMY_TEST_DATABASE_URL)
    else:
        engine = create_engine(DATABASE_URL)

    db = sessionmaker(autocommit=False, autoflush=False, bind=engine)()
    try:
        yield db
    finally:
        db.close()
