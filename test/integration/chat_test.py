import asyncio
import pytest
import pytest_asyncio
from httpx import AsyncClient, ASGITransport
from fastapi.testclient import TestClient
from chatbot.app import get_application
from chatbot.main import setup_server

pytestmark = pytest.mark.integration

@pytest.fixture(scope="module")
def server():
    return setup_server()


@pytest.fixture(scope="module")
def client(server):
    client = TestClient(server, base_url="http://test")
    yield client


@pytest.fixture(scope="module")
def login(server, client):
    response = client.post(
        server.url_path_for("staff_login"),
        json={
            "staff_number": "1234",
            "password": "password",
        },
    )
    yield response


@pytest.mark.skip
def test_chat_prompt(server, login, client):
    response = client.get(server.url_path_for("get_conversations"))
    conversations = response.json()["data"]["conversations"]

    if len(conversations) == 0:
        assert True
        return

    response = client.post(
        server.url_path_for("chat_prompt"),
        json={"message": "hello", "conversation_uuid": conversations[0]["uuid"]},
    )

    assert response.status_code == 200
