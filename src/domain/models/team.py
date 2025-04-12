from uuid import UUID

from sqlmodel import Field, SQLModel
from uuid6 import uuid7


class TeamBase(SQLModel):
    name: str = Field(title="Team name", index=True, unique=True)
    headquarters: str = Field(title="Team headquarters")


class Team(TeamBase, table=True):
    id: int = Field(primary_key=True)
    uuid: UUID = Field(default_factory=uuid7, index=True, unique=True)


class TeamCreate(TeamBase):
    pass


class TeamUpdate(SQLModel):
    name: str | None = Field(default=None, title="Team name", index=True, unique=True)
    headquarters: str | None = Field(default=None, title="Team headquarters")


class TeamPublic(TeamBase):
    uuid: UUID = Field(title="Team UUID")
