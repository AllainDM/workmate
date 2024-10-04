import pytest
from fastapi.testclient import TestClient
from sqlalchemy.orm import sessionmaker


import models
from main import app
from database import get_db, Base, create_engine

@pytest.fixture(scope="module")
def test_engine():
    # Создание временной базы данных
    test_engine = create_engine("sqlite:///:memory:")
    Base.metadata.create_all(bind=test_engine)
    return test_engine


@pytest.fixture(scope="module")
def test_app(test_engine):
    # Замена функции get_db на тестовую
    app.dependency_overrides[get_db] = lambda: sessionmaker(bind=test_engine)()

    with TestClient(app) as client:
        yield client

@pytest.fixture(scope="module")
def init_database(test_app):
    # Создаем временную базу данных
    test_session = next(get_db(testing=True))  # Получаем сессию для тестирования
    Base.metadata.create_all(bind=test_session.bind)  # Создаем все таблицы

    # Создание пород
    siamese = models.Breed(name="Сиамская")
    persian = models.Breed(name="Персидская")
    maine_coon = models.Breed(name="Мейн-Кун")
    sphinx = models.Breed(name="Сфинкс")

    test_session.bulk_save_objects([siamese, persian, maine_coon, sphinx])
    test_session.commit()

    # Создание кошек.
    siamese_kittens = [
        models.Kitten(name="Симба", age_months=21, color="Белый", breed=siamese),
        models.Kitten(name="Бублик", age_months=11, color="Рыжый", breed=siamese),
    ]
    persian_kittens = [
        models.Kitten(name="Пушистик", age_months=34, breed=persian),
        models.Kitten(name="Снежок", age_months=23, color="Черный", breed=persian),
        models.Kitten(name="Уголек", age_months=18, color="Белый", breed=persian),
    ]
    maine_coon_kittens = [
        models.Kitten(name="Тигр", age_months=45, breed=maine_coon),
        models.Kitten(name="Быська", age_months=36, breed=maine_coon),
    ]
    sphinx_kittens = [
        models.Kitten(name="Бриз", age_months=41, description="Соседский стремный кот", breed=sphinx),
        models.Kitten(name="Амонет", age_months=32, description="Родственник соседского стремного кота", breed=sphinx),
    ]

    test_session.bulk_save_objects(siamese_kittens + persian_kittens + maine_coon_kittens + sphinx_kittens)
    test_session.commit()

    yield test_session  # Возвращаем сессию для тестов

    # Удаляем данные после тестов
    test_session.query(models.Breed).delete()  # Удаляем все данные из тестовой модели
    test_session.commit()  # Коммитим изменения
    Base.metadata.drop_all(bind=test_session.bind)  # Удаляем таблицы


def test_get_breeds(test_app, init_database):
    response = test_app.get("/breeds/")

    assert response.status_code == 200
    assert len(response.json()) > 0

def test_get_kittens(test_app, init_database):
    response = test_app.get("/kittens/")

    assert response.status_code == 200
    assert len(response.json()) > 0

def test_create_kitten(test_app, init_database):
    response = test_app.post("/kittens/",
        json={
            "name": "Мила",
            "color": "Коричневый",
            "age_months": 22,
            "description": "Кошечка для тестов",
            "breed_id": 1
        })

    assert response.status_code == 200
    assert response.json()["name"] == "Мила"

def test_update_kitten(test_app, init_database):
    kittens = test_app.get("/kittens/").json()
    last_kitten_id = kittens[-1]["id"]

    response = test_app.put(f"/kitten/{last_kitten_id}",
        json={
            "name": "Мила версия 2.0",
            "color": "string",
            "age_months": 0,
            "description": "string",
            "breed_id": 0
        })

    assert response.status_code == 200
    assert response.json()["name"] == "Мила версия 2.0"
    assert response.json()["color"] == "Коричневый"

def test_delete_kitten(test_app, init_database):
    kittens = test_app.get("/kittens/").json()
    last_kitten_id = kittens[-1]["id"]

    response = test_app.delete(f"/kittens/{last_kitten_id}")

    assert response.status_code == 200



