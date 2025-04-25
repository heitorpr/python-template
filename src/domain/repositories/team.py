from uuid import UUID

from sqlalchemy.exc import NoResultFound
from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import select, update

from src.domain.models import Hero, Team
from src.domain.models.team import TeamCreate, TeamUpdate
from src.domain.repositories.exceptions import NoTeamFound


class TeamRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create(self, team_create: TeamCreate) -> Team:
        team = Team(**team_create.model_dump(exclude_unset=True))

        self.session.add(team)
        await self.session.flush()

        return team

    async def get(self, team_id: int | UUID) -> Team:
        statement = select(Team)

        if isinstance(team_id, int):
            statement = statement.where(Team.id == team_id)
        else:
            statement = statement.where(Team.uuid == team_id)

        try:
            result = await self.session.execute(statement)
            return result.scalar_one()
        except NoResultFound as error:
            raise NoTeamFound("Team not found") from error

    async def update(self, team: Team, team_update: TeamUpdate) -> Team:
        for key, value in team_update.model_dump(exclude_unset=True).items():
            setattr(team, key, value)

        self.session.add(team)
        await self.session.flush()
        return team

    async def delete(self, team: Team) -> None:
        # Ensure consistency on database excluding team_id and team_uuid from heroes
        update_hero_stmt = (
            update(Hero).where(Hero.team_id == team.id).values(team_id=None, team_uuid=None)  # type: ignore
        )

        await self.session.execute(update_hero_stmt)

        await self.session.delete(team)
        await self.session.flush()
