import asyncio
import pytest
from fastapi.testclient import TestClient
from chatbot.app import get_application
from chatbot.main import setup_server


@pytest.mark.integration
class TestAPIIntegration:
    @pytest.fixture(scope="class")
    def server(self):
        return setup_server()

    @pytest.fixture(scope="class")
    def loop(self):
        loop = asyncio.new_event_loop()
        yield loop
        loop.close()

    @pytest.fixture(scope="class")
    def client(self, loop, server):
        asyncio.set_event_loop(loop)
        return TestClient(server)

    def test_application_singleton(self):
        app1 = get_application()
        app2 = get_application()
        assert app1 is app2

    def test_root(self, client):
        response = client.get(client.app.url_path_for("root"))
        assert response.status_code == 200
        assert response.json() == {"message": "Server is running"}

    @pytest.mark.asyncio(scope="session")
    async def test_chat_prompt(self, client):
        response = client.post(
            client.app.url_path_for("chat_prompt"), json={"message": "hello"}
        )
        assert response.status_code == 200
