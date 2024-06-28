import asyncio
import pytest
from httpx import AsyncClient
from chatbot.app import get_application
from chatbot.main import setup_server


@pytest.mark.integration
class TestAPIIntegration:
    @pytest.fixture(scope="class")
    def server(self):
        return setup_server()

    def test_application_singleton(self):
        app1 = get_application()
        app2 = get_application()
        assert app1 is app2

    @pytest.mark.asyncio(scope="session")
    async def test_root(self, server):
        async with AsyncClient(app=server, base_url="http://test") as ac:
            response = await ac.get(server.url_path_for("root"))
            assert response.status_code == 200

    @pytest.mark.asyncio(scope="session")
    async def test_chat_prompt(self, server):
        async with AsyncClient(app=server, base_url="http://test") as ac:
            response = await ac.post(
                server.url_path_for("chat_prompt"), json={"message": "hello"}
            )
            assert response.status_code == 200
