import uuid

from fastapi import status
from fastapi.testclient import TestClient

from tests.conftest import DataManagement


def generate_hex():
    return uuid.uuid4().hex[:6]


def test_create_user(client_test: TestClient, data_management: DataManagement):
    payload = {
        "first_name": "Abd",
        "last_name": "Orabi",
        "email": f"user{generate_hex()}@example.com",
        "password": "string",
    }
    response = client_test.post(
        "/v1/users",
        json=payload,
    )
    assert response.status_code == status.HTTP_201_CREATED
    assert response.json()["status"] == status.HTTP_201_CREATED
    _data = response.json()["data"]
    _data["password"] = payload["password"]
    data_management.add("user", _data)


def test_user_login(client_test: TestClient, data_management: DataManagement):
    payload = {
        "email": data_management.get("user")["email"],
        "password": data_management.get("user")["password"],
    }
    response = client_test.post(
        "/v1/auth/login",
        json=payload,
    )
    assert response.status_code == status.HTTP_200_OK
    assert response.json()["status"] == status.HTTP_200_OK
    data_management.add("token", response.json()["data"])

    _data = {
        "access_token": response.json()["data"]["access_token"],
    }

    data_management.add("user_token", _data)


def test_invalid_user_login(client_test: TestClient, data_management: DataManagement):
    payload = {
        "email": data_management.get("user")["email"],
        "password": "invalid_password",
    }
    response = client_test.post(
        "/v1/auth/login",
        json=payload,
    )
    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    assert response.json()["status"] == status.HTTP_401_UNAUTHORIZED
