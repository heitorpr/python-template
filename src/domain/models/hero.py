from uuid import UUID

from sqlmodel import Field, SQLModel
from uuid6 import uuid7


class HeroBase(SQLModel):
    name: str = Field(title="Hero name")
    secret_name: str = Field(title="Hero secret name", unique=True)
    age: int | None = Field(default=None, title="Hero age")


class Hero(HeroBase, table=True):
    id: int = Field(primary_key=True)
    uuid: UUID = Field(default_factory=uuid7, title="Hero UUID", index=True, unique=True)


class HeroCreate(HeroBase):
    pass


class HeroUpdate(SQLModel):
    name: str | None = Field(default=None, title="Hero name")
    secret_name: str | None = Field(default=None, title="Hero secret name")
    age: int | None = Field(default=None, title="Hero age")


class HeroPublic(HeroBase):
    uuid: UUID = Field(title="Hero UUID")
