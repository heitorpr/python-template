import os

import pytest
from pydantic import ValidationError

from src.core.settings import Settings


@pytest.fixture()
def set_envs(mocker):
    env_vars = {
        "APP_DB_USER": "testuser",
        "APP_DB_NAME": "testdb",
        "APP_DB_HOST": "testhost",
        "APP_DB_PORT": "1234",
        "APP_DB_PASSWORD": "testpassword",
    }
    mocker.patch.dict(os.environ, env_vars)
    return mocker


def test_case_insensitive_env_vars(set_envs):
    settings = Settings()

    assert settings.db_user == "testuser"
    assert settings.db_name == "testdb"
    assert settings.db_host == "testhost"
    assert settings.db_port == 1234
    assert settings.db_password == "testpassword"


def test_invalid_port_value(mocker):
    mocker.patch.dict(os.environ, {"APP_DB_PORT": "invalid_port"})

    with pytest.raises(ValidationError):
        Settings()


def test_db_dsn_sync(set_envs):
    settings = Settings()

    assert (
        str(settings.db_dsn_sync)
        == "postgresql+psycopg://testuser:testpassword@testhost:1234/testdb"
    )


def test_db_dsn_async(set_envs):
    settings = Settings()

    assert (
        str(settings.db_dsn_async)
        == "postgresql+asyncpg://testuser:testpassword@testhost:1234/testdb"
    )
