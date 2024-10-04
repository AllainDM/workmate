import os

from sqlalchemy.orm import Session
from sqlalchemy import create_engine
from dotenv import load_dotenv


from app.models import Base, Breed, Kitten

# Настройки базы данных.
# Загружаем переменные окружения из .env файла
load_dotenv()
DATABASE_URL = os.getenv("DATABASE_URL")

# Создание SQLAlchemy движка и сессии.
engine = create_engine(DATABASE_URL)


def init_db():
    Base.metadata.create_all(bind=engine)

def create_data():
    # Стартовые данные для БД

    # Создание сессии
    session = Session(bind=engine)

    # Создание пород
    siamese = Breed(name="Сиамская")
    persian = Breed(name="Персидская")
    maine_coon = Breed(name="Мейн-Кун")
    sphinx = Breed(name="Сфинкс")

    session.add_all([siamese, persian, maine_coon, sphinx])
    session.commit()

    # Создание котят
    siamese_kittens = [
        Kitten(name="Симба", age_months=21, color="Белый", breed=siamese),
        Kitten(name="Бублик", age_months=11, color="Рыжый", breed=siamese),
    ]
    persian_kittens = [
        Kitten(name="Пушистик", age_months=34, breed=persian),
        Kitten(name="Снежок", age_months=23, color="Черный", breed=persian),
        Kitten(name="Уголек", age_months=18, color="Белый", breed=persian),
    ]
    maine_coon_kittens = [
        Kitten(name="Тигр", age_months=45, breed=maine_coon),
        Kitten(name="Быська", age_months=36, breed=maine_coon),
    ]
    sphinx_kittens = [
        Kitten(name="Бриз", age_months=41, description="Соседский стремный кот", breed=sphinx),
        Kitten(name="Амонет", age_months=32, description="Родственник соседского стремного кота", breed=sphinx),
    ]

    session.add_all(siamese_kittens + persian_kittens + maine_coon_kittens + sphinx_kittens)
    session.commit()

    session.close()

    print("Внесены предустановленные данные.")


def clear_data():
    # Создание сессии
    session = Session(bind=engine)

    # Удаляем все данные из базы
    Base.metadata.drop_all(bind=engine)

    # Восстанавливаем таблицы
    Base.metadata.create_all(bind=engine)

    session.close()
    print("База данных очищена.")


if __name__ == "__main__":
    # Очистим данные перед внесением, для исключения ошибок и дублей.
    clear_data()
    # Внесение предустановленных данных для тестов.
    init_db()
    create_data()

    