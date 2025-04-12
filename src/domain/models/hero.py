from uuid import UUID

from sqlmodel import Field, SQLModel
from uuid6 import uuid7


class HeroBase(SQLModel):
    name: str = Field(title="Hero name")
    secret_name: str = Field(title="Hero secret name", unique=True)
    age: int | None = Field(default=None, title="Hero age")


class Hero(HeroBase, table=True):
    id: int = Field(primary_key=True)
    uuid: UUID = Field(default_factory=uuid7, index=True, unique=True)
    team_id: int | None = Field(
        default=None, foreign_key="team.id", nullable=True, title="Team ID"
    )
    team_uuid: UUID | None = Field(default=None, nullable=True, title="Team UUID")


class HeroCreate(HeroBase):
    team_uuid: UUID | None = Field(default=None, description="Optional field to link to a team")


class HeroUpdate(SQLModel):
    name: str | None = Field(default=None, title="Hero name")
    secret_name: str | None = Field(default=None, title="Hero secret name")
    age: int | None = Field(default=None, title="Hero age")
    team_uuid: UUID | None = Field(default=None, description="Optional field to link to a team")


class HeroPublic(HeroBase):
    uuid: UUID = Field()
    team_uuid: UUID | None = Field(nullable=True)
