import pytest
from httpx import ASGITransport, AsyncClient

from src.web.deps import get_db_session
from src.web.main import app


@pytest.mark.asyncio(loop_scope="session")
async def test_root_default(client, auth_headers):
    response = await client.get("/api/", headers=auth_headers("GET", {}))
    assert response.status_code == 200
    assert response.json() == "Hello, World!"


@pytest.mark.asyncio(loop_scope="session")
async def test_root_with_name(client, auth_headers):
    response = await client.get("/api/?name=ChatGPT", headers=auth_headers("GET", {}))
    assert response.status_code == 200
    assert response.json() == "Hello, ChatGPT!"


@pytest.mark.asyncio
async def test_health_check_error(mocker, auth_headers):
    mock_session = mocker.AsyncMock()

    mock_result = mocker.Mock()
    mock_result.first.return_value = None

    mock_session.execute.return_value = mock_result

    async def _override():
        yield mock_session

    app.dependency_overrides[get_db_session] = _override

    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        response = await client.get("/api/healthz", headers=auth_headers("GET", {}))

        assert response.status_code == 200
        assert response.json() == {
            "status": "error",
            "message": "No health status found",
        }
        await client.aclose()

    app.dependency_overrides.clear()


@pytest.mark.asyncio
async def test_health_check_with_valid_session(mocker, auth_headers):
    mock_session = mocker.AsyncMock()

    mock_result = mocker.Mock()
    mock_result.first.return_value = (1,)

    mock_session.execute.return_value = mock_result

    async def _override():
        yield mock_session

    app.dependency_overrides[get_db_session] = _override

    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        response = await client.get("/api/healthz", headers=auth_headers("GET", {}))

        assert response.status_code == 200
        assert response.json() == {"status": "ok"}
        await client.aclose()

    app.dependency_overrides.clear()
