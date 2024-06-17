from fastapi.testclient import TestClient

from chatbot.app import get_application
from chatbot.main import setup_server

server = setup_server()

client = TestClient(server)


def test_application_singleton():
    app1 = get_application()
    app2 = get_application()
    assert app1 is app2


def test_root():
    response = client.get(server.url_path_for("root"))
    assert response.status_code == 200
    assert response.json() == {"message": "Server is running"}


def test_chat_prompt():
    response = client.post(
        server.url_path_for("chat_prompt"), json={"message": "hello"}
    )
    print(response.json())
    assert response.status_code == 200
