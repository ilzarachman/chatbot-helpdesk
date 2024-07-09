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
    async with AsyncClient(
        transport=ASGITransport(app=server), base_url="http://test"
    ) as ac:
        response = await ac.post(
            server.url_path_for("create_user"),
            json=user,
        )
        print(response.json())
        yield response


@pytest.mark.order(1)
@pytest.mark.asyncio(scope="session")
async def test_create_user_returns_user(server, user_creation):
    response = user_creation

    assert response.status_code == 201
    assert response.json()["data"]["student_number"] == "123456789"
    assert response.json()["data"]["name"] == "John Doe"
    assert response.json()["data"]["email"] == "6O5yK@example.com"


@pytest.mark.order(2)
@pytest.mark.asyncio(scope="session")
async def test_update_user_returns_user(server, user_creation):
    user_id = user_creation.json()["data"]["id"]

    async with AsyncClient(
        transport=ASGITransport(app=server), base_url="http://test"
    ) as ac:
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
        assert response.json()["data"]["student_number"] == "123456789"
        assert response.json()["data"]["name"] == "Johan"
        assert response.json()["data"]["email"] == "johan009@example.com"


@pytest.mark.order(3)
@pytest.mark.asyncio(scope="session")
async def test_get_user_returns_user(server, user_creation):
    user_id = user_creation.json()["data"]["id"]

    async with AsyncClient(
        transport=ASGITransport(app=server), base_url="http://test"
    ) as ac:
        response = await ac.get(
            server.url_path_for("get_user", user_id=user_id),
        )

        user_id = response.json()["data"]["id"]

        response = await ac.get(
            server.url_path_for("get_user", user_id=user_id),
        )

        assert response.status_code == 200
        assert response.json()["data"]["student_number"] == "123456789"
        assert response.json()["data"]["name"] == "Johan"
        assert response.json()["data"]["email"] == "johan009@example.com"


@pytest.mark.order(4)
@pytest.mark.asyncio(scope="session")
async def test_get_all_users_returns_users(server, user_creation):
    async with AsyncClient(
        transport=ASGITransport(app=server), base_url="http://test"
    ) as ac:
        response = await ac.get(
            server.url_path_for("get_all_users"),
        )

        assert response.status_code == 200
        assert isinstance(response.json()["data"], list)


@pytest.mark.order(5)
@pytest.mark.asyncio(scope="session")
async def test_search_user_returns_users(server, user_creation):
    async with AsyncClient(
        transport=ASGITransport(app=server), base_url="http://test"
    ) as ac:
        response = await ac.get(
            f"{server.url_path_for('search_user')}?query=123456789",
        )

        assert response.status_code == 200
        assert isinstance(response.json()["data"], list)
        assert response.json()["data"][0]["student_number"] == "123456789"


@pytest.mark.order(6)
@pytest.mark.asyncio(scope="session")
async def test_delete_user_returns_user_deleted(server, user_creation):
    user_id = user_creation.json()["data"]["id"]
    async with AsyncClient(
        transport=ASGITransport(app=server), base_url="http://test"
    ) as ac:
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
