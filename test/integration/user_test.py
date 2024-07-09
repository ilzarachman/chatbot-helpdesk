import pytest
from httpx import AsyncClient, ASGITransport
from chatbot.app import get_application
from chatbot.main import setup_server

pytestmark = pytest.mark.integration


user = {
    "student_number": "123456789",
    "name": "John Doe",
    "email": "6O5yK@example.com",
    "password": "password",
}


@pytest.fixture(scope="module")
def server():
    return setup_server()


@pytest.fixture(scope="module")
async def user_creation(server):
    async with AsyncClient(transport=ASGITransport(app=server), base_url="http://test") as ac:
        response = await ac.post(
            server.url_path_for("create_user"),
            json=user,
        )
        yield response


@pytest.mark.asyncio(scope="session")
async def test_root(server):
    async with AsyncClient(transport=ASGITransport(app=server), base_url="http://test") as ac:
        response = await ac.get(server.url_path_for("root"))
        assert response.status_code == 200


@pytest.mark.order(1)
@pytest.mark.asyncio(scope="session")
async def test_create_user_returns_user(server, user_creation):
    response = user_creation

    assert response.status_code == 201
    assert response.json()["user"]["student_number"] == "123456789"
    assert response.json()["user"]["name"] == "John Doe"
    assert response.json()["user"]["email"] == "6O5yK@example.com"


@pytest.mark.order(2)
@pytest.mark.asyncio(scope="session")
async def test_update_user_returns_user(server, user_creation):
    user_id = user_creation.json()["user"]["id"]

    async with AsyncClient(transport=ASGITransport(app=server), base_url="http://test") as ac:
        response = await ac.put(
            server.url_path_for("update_user", user_id=user_id),
            json={
                "student_number": "123456789",
                "name": "Johan",
                "email": "johan009@example.com",
                "password": "password",
            },
        )

        assert response.status_code == 200
        assert response.json()["user"]["student_number"] == "123456789"
        assert response.json()["user"]["name"] == "Johan"
        assert response.json()["user"]["email"] == "johan009@example.com"


@pytest.mark.order(3)
@pytest.mark.asyncio(scope="session")
async def test_get_user_returns_user(server, user_creation):
    user_id = user_creation.json()["user"]["id"]

    async with AsyncClient(transport=ASGITransport(app=server), base_url="http://test") as ac:
        response = await ac.get(
            server.url_path_for("get_user", user_id=user_id),
        )

        user_id = response.json()["user"]["id"]

        response = await ac.get(
            server.url_path_for("get_user", user_id=user_id),
        )

        assert response.status_code == 200
        assert response.json()["user"]["student_number"] == "123456789"
        assert response.json()["user"]["name"] == "Johan"
        assert response.json()["user"]["email"] == "johan009@example.com"


@pytest.mark.order(4)
@pytest.mark.asyncio(scope="session")
async def test_delete_user_returns_user_deleted(server, user_creation):
    user_id = user_creation.json()["user"]["id"]
    async with AsyncClient(transport=ASGITransport(app=server), base_url="http://test") as ac:
        response = await ac.delete(
            server.url_path_for("delete_user", user_id=user_id),
        )

        assert response.status_code == 200
        assert response.json()["message"] == f"User with ID:{user_id} deleted"

        response = await ac.get(
            server.url_path_for("get_user", user_id=user_id),
        )

        assert response.status_code == 404
        assert response.json()["detail"] == "User not found"
