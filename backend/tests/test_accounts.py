import pytest
import pytest_asyncio
from httpx import ASGITransport, AsyncClient

from app.main import app


@pytest_asyncio.fixture
async def client():
    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://test"
    ) as ac:
        yield ac


@pytest.mark.asyncio
async def test_get_accounts_returns_list(client: AsyncClient):
    response = await client.get("/accounts")
    assert response.status_code == 200
    assert isinstance(response.json(), list)
