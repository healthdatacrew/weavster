import pytest
from fastapi.testclient import TestClient

from weavster.server import app


@pytest.fixture(name="client")
def _client():
    return TestClient(app)


def test_hello(client):
    """
    Root URL greets the world.
    """
    resp = client.get("/api/helloworld")

    assert resp.status_code == 200
    assert resp.json() == {"message": "Hello World"}


def test_dashboard(client):
    """
    Dashboard URL returns a welcome message.
    """
    resp = client.get("/")

    assert resp.status_code == 200
    assert resp.json() == {"message": "Welcome to the Weavster Dashboard!"}
