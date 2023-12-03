from src.db.configs import Base
from src.configs.test_config import mock_engine, client


def setup():
    Base.metadata.create_all(bind=mock_engine)


def teardown():
    Base.metadata.drop_all(bind=mock_engine)


def test_server_ok():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Hello World"}


def test_server_params_ok():
    response = client.get("/hello/Greg")
    assert response.status_code == 200
    assert response.json() == {"message": "Hello Greg"}


def test_create_user():
    test_data = {
        "name": "string_1",
        "username": "string_1",
        "family_name": "string_1",
        "password": "string_1",
    }

    response = client.post("/users", json=test_data)
    assert response.status_code == 201
    data = response.json()
    assert data.get("name") == test_data.get("name")
    assert "id" in data

    new_user_id = data.get("id")

    response = client.get(f"/users/{new_user_id}")
    assert response.status_code == 200
    assert response.json().get("family_name") == test_data.get("family_name")

    patch_test_data = {"name": "Greg"}
    response = client.patch(f"/users/{new_user_id}", json=patch_test_data)

    assert response.status_code == 200
    assert response.json().get("name") == "Greg"

    response = client.get("/users")
    assert response.status_code == 200
    assert isinstance(response.json(), list)
    assert len(response.json()) == 1

    response = client.delete(f"/users/{new_user_id}")
    assert response.status_code == 204

    response = client.get(f"/users/{new_user_id}")
    assert response.status_code == 404
