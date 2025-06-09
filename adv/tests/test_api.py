import pytest
from adv.adv_repository.models import Base
from adv.web.app import create_app


@pytest.fixture(scope="session")
def app_instance():
    """Создает и возвращает экземпляр Flask-приложения для тестов."""
    app = create_app("testing")
    return app


@pytest.fixture(scope="function")
def client(app_instance):
    """Возвращает тестовый клиент Flask для отправки HTTP-запросов."""
    return app_instance.test_client()


@pytest.fixture(scope="function")
def app_context(app_instance):
    """Обеспечивает активный контекст приложения для каждого теста."""
    with app_instance.app_context():
        yield app_instance


@pytest.fixture(scope="function")
def setup_db(app_context):
    """
    Создает все таблицы БД перед тестом и удаляет их после.
    Использует in-memory SQLite для тестов.
    """
    engine = app_context.db_engine
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)


good_payload = {
    "name": "test_name",
    "chanel": "Google",
    "cost": 111.11,
    "product_id": 33,
}

updated_payload = {
    "name": "test_name_1",
    "chanel": "YouTube",
    "cost": 222.11,
    "product_id": 11,
}

bad_payload = {
    "name": "test_name",
    "chanel": "test_chan",
    "cost": "dd",
    "product_id": "ss",
}


def test_create_adv_success(client, setup_db):
    response = client.post("/ads", json=good_payload)
    assert response.status_code == 201
    assert response.json["name"] == "test_name"


def test_create_adv_fails(client, setup_db):
    response = client.post("/ads", json=bad_payload)
    assert response.status_code == 422


def test_get_adv_success(client, setup_db):
    created_product = client.post("/ads", json=good_payload)
    assert created_product.status_code == 201

    response = client.get(f"/ads/{created_product.json["id"]}")
    getting_adv = response.json
    assert response.status_code == 200
    assert getting_adv["name"] == good_payload["name"]
    assert getting_adv["cost"] == str(good_payload["cost"])
    assert getting_adv["chanel"] == good_payload["chanel"]
    assert getting_adv["product_id"] == good_payload["product_id"]


def test_update_adv_success(client, setup_db):
    post_response = client.post("/ads", json=good_payload)
    assert post_response.status_code == 201

    created_product = post_response.json
    response = client.put(f"/ads/{created_product["id"]}", json=updated_payload)
    assert response.status_code == 200

    updated_product_response = response.json
    assert updated_product_response["name"] != created_product["name"]
    assert updated_product_response["cost"] != created_product["cost"]


def test_update_ads_not_found(client, setup_db):
    non_existent_id = 999999999

    response = client.put(f"/ads/{non_existent_id}", json=good_payload)

    assert response.status_code == 404


def test_update_ads_validation_error(client, setup_db):
    post_response = client.post("/ads", json=good_payload)
    assert post_response.status_code == 201
    created_product = post_response.json

    response = client.put(f"/ads/{created_product["id"]}", json=bad_payload)
    assert response.status_code == 422


def test_delete_ads_success(client, setup_db):
    post_response = client.post("/ads", json=good_payload)
    assert post_response.status_code == 201

    response = client.delete(f"/ads/{post_response.json["id"]}")

    assert response.status_code == 204

    get_response = client.get(f"/products/{post_response.json["id"]}")
    assert get_response.status_code == 404
