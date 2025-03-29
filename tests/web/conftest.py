import time

import pytest
from httpx import ASGITransport, AsyncClient

from src.core.settings import settings
from src.domain.repositories.hero import HeroRepository
from src.web.deps import get_db_session
from src.web.main import app
from tests.utils.signing import generate_signature


@pytest.fixture
async def client():
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        yield client
        await client.aclose()


@pytest.fixture(autouse=True)
async def override_db_session(db_session):
    async def _override():
        yield db_session

    app.dependency_overrides[get_db_session] = _override
    yield
    app.dependency_overrides.clear()


@pytest.fixture()
def auth_headers():
    def _auth_headers(method, body):
        timestamp = str(int(time.time() * 1000))
        signature = generate_signature(method, body, timestamp, settings.secret_key)

        return {
            "x-signature": signature,
            "x-timestamp": timestamp,
            "Content-Type": "application/json",
        }

    return _auth_headers


@pytest.fixture()
def hero_repository(db_session):
    return HeroRepository(session=db_session)
