import pytest
import pytest_asyncio
from httpx import AsyncClient, ASGITransport
from fastapi.testclient import TestClient
from chatbot.app import get_application
from chatbot.main import setup_server
from faker import Faker

pytestmark = pytest.mark.integration

faker = Faker()

user = {
    "student_number": faker.passport_number(),
    "name": faker.name(),
    "email": faker.email(),
    "password": "password",
}


@pytest.fixture(scope="module")
def server():
    return setup_server()


@pytest.fixture(scope="module")
def user_creation(server, client, login):
    response = client.post(
        server.url_path_for("create_user"),
        json=user,
    )
    print(response.json())
    yield response


@pytest.fixture(scope="module")
def login(server, client):
    response = client.post(
        server.url_path_for("staff_login"),
        json={
            "staff_number": "1234",
            "password": user["password"],
        },
    )
    yield response


@pytest.fixture(scope="module")
def client(server):
    client = TestClient(server, base_url="http://test")
    yield client


@pytest.mark.order(1)
def test_create_user_returns_user(server, login, user_creation):
    response = user_creation

    assert response.status_code == 201
    assert response.json()["data"]["student_number"] == user["student_number"]
    assert response.json()["data"]["name"] == user["name"]
    assert response.json()["data"]["email"] == user["email"]


@pytest.mark.order(2)
def test_update_user_returns_user(server, user_creation, login, client):
    user_id = user_creation.json()["data"]["id"]

    response = client.put(
        server.url_path_for("update_user", user_id=user_id),
        json={
            "name": "Johan",
        },
    )

    assert response.status_code == 200
    assert response.json()["data"]["name"] == "Johan"


@pytest.mark.order(3)
def test_get_user_returns_user(server, user_creation, client):
    user_id = user_creation.json()["data"]["id"]

    response = client.get(
        server.url_path_for("get_user", user_id=user_id),
    )

    user_id = response.json()["data"]["id"]

    response = client.get(
        server.url_path_for("get_user", user_id=user_id),
    )

    assert response.status_code == 200
    assert response.json()["data"]["student_number"] == user["student_number"]
    assert response.json()["data"]["name"] == "Johan"
    assert response.json()["data"]["email"] == user["email"]


@pytest.mark.order(4)
def test_get_all_users_returns_users(server, user_creation, client):

    response = client.get(
        server.url_path_for("get_all_users"),
    )

    assert response.status_code == 200
    assert isinstance(response.json()["data"], list)


@pytest.mark.order(5)
def test_search_user_returns_users(server, user_creation, client):
    response = client.get(
        f"{server.url_path_for('search_user')}?query={user['student_number']}",
    )

    assert response.status_code == 200
    assert isinstance(response.json()["data"], list)
    assert response.json()["data"][0]["student_number"] == user["student_number"]


@pytest.mark.order(6)
def test_delete_user_returns_user_deleted(server, user_creation, client):
    user_id = user_creation.json()["data"]["id"]

    response = client.delete(
        server.url_path_for("delete_user", user_id=user_id),
    )

    assert response.status_code == 200
    assert response.json()["message"] == f"User with ID:{user_id} deleted"
