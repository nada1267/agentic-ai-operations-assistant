from fastapi.testclient import TestClient
from api import app


client = TestClient(app)


def test_chat_endpoint():

    response = client.post(
        "/chat",
        json={
            "message": "Where is my order ORD-4582?"
        }
    )

    assert response.status_code == 200

    data = response.json()

    assert "response" in data