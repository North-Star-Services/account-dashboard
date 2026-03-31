from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_get_accounts_returns_list():
    response = client.get("/accounts")
    assert response.status_code == 200
    assert isinstance(response.json(), list)
