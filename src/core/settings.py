from pydantic import Field, PostgresDsn, computed_field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        env_prefix="APP_",
        extra="ignore",
        env_ignore_empty=True,
        case_sensitive=False,
        populate_by_name=True,
        alias_generator=str.upper,
    )

    # Database
    db_user: str = Field(default="postgres", title="Database user")
    db_name: str = Field(default="app", title="Database name")
    db_host: str = Field(default="localhost", title="Database host")
    db_port: int = Field(default=5432, title="Database port")
    db_password: str = Field(default="password", title="Database password")

    # Api
    timestamp_signing_threshold: int = Field(default=60000, title="Timestamp signing threshold")
    secret_key: str = Field(default="secret", title="Secret key for signing")

    @computed_field
    @property
    def db_dsn_sync(self) -> PostgresDsn:
        return PostgresDsn.build(
            scheme="postgresql+psycopg",
            username=self.db_user,
            password=self.db_password,
            host=self.db_host,
            port=self.db_port,
            path=self.db_name,
        )

    @computed_field
    @property
    def db_dsn_async(self) -> PostgresDsn:
        return PostgresDsn.build(
            scheme="postgresql+asyncpg",
            username=self.db_user,
            password=self.db_password,
            host=self.db_host,
            port=self.db_port,
            path=self.db_name,
        )


settings = Settings()
