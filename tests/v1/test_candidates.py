import uuid

import pytest
from fastapi import status
from fastapi.testclient import TestClient

from tests.conftest import DataManagement


def generate_hex():
    return uuid.uuid4().hex[:6]


def test_get_all_candidates(client_test: TestClient, data_management: DataManagement):
    #  need to get user token first

    response = client_test.get(
        "/v1/candidates/all-candidates?page=1&page_size=10&order=asc",
        headers={
            "Authorization": f"{data_management.get('user_token')['access_token']}"
        },
    )
    assert response.status_code == status.HTTP_200_OK
    assert response.json()["status"] == status.HTTP_200_OK


# def test_generate_report(client_test: TestClient, data_management: DataManagement):
#     response = client_test.get(
#         "/v1/candidates/generate-report?page=1&page_size=10",
#         headers={
#             "Authorization": f"{data_management.get('user_token')['access_token']}"
#         },
#     )
#     assert response.status_code == status.HTTP_200_OK
#     assert response.headers["Content-Type"] == "text/csv; charset=utf-8"


def test_create_candidate(client_test: TestClient, data_management: DataManagement):
    payload = {
        "first_name": "Abdalkreem",
        "last_name": "Orabi",
        "email": f"user{generate_hex()}@example.com",
        "major": "Software Engineer",
        "years_of_experience": 5,
        "skills": ["Python", "FastAPI"],
        "nationality": "Syrian",
        "city": "Amman",
        "salary": 1111,
        "gender": "Male",
    }
    response = client_test.post(
        "/v1/candidates",
        json=payload,
        headers={
            "Authorization": f"{data_management.get('user_token')['access_token']}"
        },
    )

    assert response.status_code == status.HTTP_201_CREATED
    assert response.json()["status"] == status.HTTP_201_CREATED

    data_management.add("candidate", response.json()["data"])


def test_update_candidate(client_test: TestClient, data_management: DataManagement):
    payload = {
        "first_name": "test update",
    }
    response = client_test.patch(
        f"/v1/candidates/{data_management.get('candidate')['uuid']}",
        json=payload,
        headers={
            "Authorization": f"{data_management.get('user_token')['access_token']}"
        },
    )
    assert response.status_code == status.HTTP_202_ACCEPTED
    assert response.json()["status"] == status.HTTP_202_ACCEPTED


def test_delete_candidate(client_test: TestClient, data_management: DataManagement):
    response = client_test.delete(
        f"/v1/candidates/{data_management.get('candidate')['uuid']}",
        headers={"Authorization": data_management.get("user_token")["access_token"]},
    )
    assert response.status_code == status.HTTP_202_ACCEPTED
    assert response.json()["status"] == status.HTTP_202_ACCEPTED
