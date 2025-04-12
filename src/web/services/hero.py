from uuid import UUID

from src.domain.models import Hero
from src.domain.models.hero import HeroCreate, HeroPublic, HeroUpdate
from src.domain.repositories import HeroRepository, TeamRepository


class HeroService:
    def __init__(self, hero_repository: HeroRepository, team_repository: TeamRepository):
        self.hero_repository = hero_repository
        self.team_repository = team_repository

    async def _parse_to_public(self, hero: Hero) -> HeroPublic:
        return HeroPublic(**hero.model_dump())

    async def create_hero(self, hero_create: HeroCreate) -> HeroPublic:
        team = None
        if hero_create.team_uuid:
            team = await self.team_repository.get(hero_create.team_uuid)

        hero = await self.hero_repository.create(hero_create, team)
        return await self._parse_to_public(hero)

    async def get_hero(self, uuid: UUID) -> HeroPublic:
        hero = await self.hero_repository.get(uuid)
        return await self._parse_to_public(hero)

    async def update_hero(self, uuid: UUID, hero_update: HeroUpdate) -> HeroPublic:
        hero = await self.hero_repository.get(uuid)

        team = None
        if hero_update.team_uuid:
            team = await self.team_repository.get(hero_update.team_uuid)

        hero = await self.hero_repository.update(hero, hero_update, team)
        return await self._parse_to_public(hero)

    async def delete_hero(self, uuid: UUID) -> None:
        hero = await self.hero_repository.get(uuid)
        await self.hero_repository.delete(hero)
