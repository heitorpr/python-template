from uuid import UUID

from src.domain.models import Team
from src.domain.models.hero import HeroPublic
from src.domain.models.team import TeamCreate, TeamPublic, TeamUpdate
from src.domain.repositories.hero import HeroRepository
from src.domain.repositories.team import TeamRepository


class TeamService:
    def __init__(self, team_repository: TeamRepository, hero_repository: HeroRepository):
        self.team_repository = team_repository
        self.hero_repository = hero_repository

    async def _parse_to_public(self, team: Team) -> TeamPublic:
        return TeamPublic(**team.model_dump())

    async def create_team(self, team_create: TeamCreate) -> TeamPublic:
        team = await self.team_repository.create(team_create)
        return await self._parse_to_public(team)

    async def get_team(self, uuid: UUID) -> TeamPublic:
        team = await self.team_repository.get(uuid)
        return await self._parse_to_public(team)

    async def update_team(self, uuid: UUID, team_update: TeamUpdate) -> TeamPublic:
        team = await self.team_repository.get(uuid)
        team = await self.team_repository.update(team, team_update)
        return await self._parse_to_public(team)

    async def delete_team(self, uuid: UUID) -> None:
        team = await self.team_repository.get(uuid)
        await self.team_repository.delete(team)

    async def get_heroes(self, uuid: UUID) -> list[HeroPublic]:
        team = await self.team_repository.get(uuid)
        heroes = await self.hero_repository.get_by_team(team.id)
        return [HeroPublic(**hero.model_dump()) for hero in heroes]
