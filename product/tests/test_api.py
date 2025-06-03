from fastapi.testclient import TestClient

from product.web.main import app

test_client = TestClient(app=app)

good_payload = {"name": "test_name", "price": "100.13"}

updated_payload = {"name": "updated_product_name", "price": 150.50}

bad_payload = {"name": 1, "price": "price"}


def test_create_order_success():
    response = test_client.post("/products", json=good_payload)
    assert response.status_code == 201


def test_create_order_fails():
    response = test_client.post("/products", json=bad_payload)
    assert response.status_code == 422


def test_get_order_success():
    post_response = test_client.post("/products", json=good_payload)
    assert post_response.status_code == 201

    response = test_client.get(f"/products/{good_payload['name']}")
    getting_product = response.json()
    assert getting_product["name"] == good_payload["name"]
    assert getting_product["price"] == good_payload["price"]
    assert response.status_code == 200


def test_update_product_success():
    """Тест успешного обновления существующего продукта по ID."""
    post_response = test_client.post("/products", json=good_payload)
    assert post_response.status_code == 201

    created_product = post_response.json()

    response = test_client.put(
        f"/products/{created_product["name"]}", json=updated_payload
    )
    assert response.status_code == 200

    updated_product_response = response.json()
    assert updated_product_response["name"] != created_product["name"]
    assert updated_product_response["price"] != created_product["price"]


def test_update_product_not_found():
    """Тест попытки обновления несуществующего продукта."""
    non_existent_id = 999999999

    response = test_client.put(f"/products/{non_existent_id}", json=good_payload)

    assert response.status_code == 404


def test_update_product_validation_error():
    """Тест попытки обновления существующего продукта с невалидными данными."""
    post_response = test_client.post("/products", json=good_payload)
    assert post_response.status_code == 201
    created_product = post_response.json()
    product_id_to_update = created_product["id"]

    response = test_client.put(f"/products/{product_id_to_update}", json=bad_payload)

    assert response.status_code == 422


def test_delete_product_success():
    post_response = test_client.post("/products", json=good_payload)
    assert post_response.status_code == 201
    created_product = post_response.json()
    product_id_to_delete = created_product["id"]

    response = test_client.delete(f"/products/{product_id_to_delete}")

    assert response.status_code == 204

    get_response = test_client.get(f"/products/{product_id_to_delete}")
    assert get_response.status_code == 404
