from urllib.parse import urlparse

import pytest
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.ext.asyncio.engine import AsyncEngine

from src.core.deps.db import get_db_session


async def test_get_db_session(db_url: str):
    async for session in get_db_session():
        assert isinstance(session, AsyncSession)

        bind = session.bind
        assert isinstance(bind, AsyncEngine)

        session_url = str(bind.url)

        parsed_session_url = urlparse(session_url)
        parsed_expected_url = urlparse(db_url)

        assert parsed_session_url.scheme == parsed_expected_url.scheme
        assert parsed_session_url.username == parsed_expected_url.username
        assert parsed_session_url.hostname == parsed_expected_url.hostname
        # Password is hidden, thus not compared
        assert parsed_session_url.port == parsed_expected_url.port
        assert parsed_session_url.path == parsed_expected_url.path


async def test_get_db_session_rollback(mocker):
    mock_session = mocker.AsyncMock()
    mocker.patch("src.core.deps.db.AsyncSessionLocal", return_value=mock_session)

    mock_session.__aenter__.return_value = mock_session
    mock_session.__aexit__.return_value = None

    mock_session.commit.side_effect = ValueError("Erro simulado")

    async def failing_usage():
        gen = get_db_session()
        await anext(gen)

        # wait the finalization of the session
        await anext(gen)

    with pytest.raises(ValueError, match="Erro simulado"):
        await failing_usage()

    mock_session.rollback.assert_awaited_once()
