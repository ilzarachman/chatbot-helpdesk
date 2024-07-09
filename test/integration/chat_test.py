import asyncio
import pytest
from httpx import AsyncClient, ASGITransport
from chatbot.app import get_application
from chatbot.main import setup_server

pytestmark = pytest.mark.integration

@pytest.fixture(scope="module")
def server():
    return setup_server()


def test_application_singleton():
    app1 = get_application()
    app2 = get_application()
    assert app1 is app2


@pytest.mark.asyncio(scope="session")
async def test_root(server):
    async with AsyncClient(transport=ASGITransport(app=server), base_url="http://test") as ac:
        response = await ac.get(server.url_path_for("root"))
        assert response.status_code == 200


@pytest.mark.asyncio(scope="session")
async def test_chat_prompt(server):
    async with AsyncClient(transport=ASGITransport(app=server), base_url="http://test") as ac:
        response = await ac.post(
            server.url_path_for("chat_prompt"), json={"message": "hello"}
        )
        assert response.status_code == 200
