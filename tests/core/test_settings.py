import os

import pytest

from src.core.settings import Settings


@pytest.fixture()
def set_envs(mocker):
    env_vars = {
        "APP_DB_USER": "testuser",
        "APP_DB_NAME": "testdb",
        "APP_DB_HOST": "testhost",
        "APP_DB_PORT": "1234",
        "APP_DB_PASSWORD": "testpassword",
        "APP_TIMESTAMP_SIGNING_THRESHOLD": "30000",
        "APP_SECRET_KEY": "banana",
        "APP_NAME": "test_app",
        "APP_NAMESPACE": "test_namespace",
    }
    mocker.patch.dict(os.environ, env_vars)
    return mocker


@pytest.mark.usefixtures("set_envs")
def test_case_insensitive_env_vars():
    settings = Settings()

    assert settings.db_user == "testuser"
    assert settings.db_name == "testdb"
    assert settings.db_host == "testhost"
    assert settings.db_port == 1234
    assert settings.db_password == "testpassword"
    assert settings.timestamp_signing_threshold == 30000
    assert settings.secret_key == "banana"
    assert settings.name == "test_app"
    assert settings.namespace == "test_namespace"


def test_invalid_port_value(mocker):
    mocker.patch.dict(os.environ, {"APP_DB_PORT": "invalid_port"})

    with pytest.raises(ValueError):
        Settings()


@pytest.mark.usefixtures("set_envs")
def test_db_dsn_sync():
    settings = Settings()

    assert (
        settings.db_dsn_sync == "postgresql+psycopg://testuser:testpassword@testhost:1234/testdb"
    )


@pytest.mark.usefixtures("set_envs")
def test_db_dsn_async():
    settings = Settings()

    assert (
        settings.db_dsn_async == "postgresql+asyncpg://testuser:testpassword@testhost:1234/testdb"
    )
