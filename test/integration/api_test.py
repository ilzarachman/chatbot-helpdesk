from fastapi.testclient import TestClient

from chatbot.app import get_application
from chatbot.main import setup_server

server = setup_server()

client = TestClient(server)

api_prefix = "/api/v1"


def test_application_singleton():
    app1 = get_application()
    app2 = get_application()
    assert app1 is app2


def test_root():
    response = client.get(f"{api_prefix}/")
    assert response.status_code == 200
    assert response.json() == {"message": "Server is running"}


def test_chat_prompt():
    response = client.get(f"{api_prefix}/chat/prompt", params={"message": "Di kampus ada fasilitas apa saja?"})
    assert response.status_code == 200
