from uuid import UUID

from src.domain.models import Hero
from src.domain.models.hero import HeroCreate, HeroPublic, HeroUpdate
from src.domain.repositories import HeroRepository


class HeroService:
    def __init__(self, hero_repository: HeroRepository):
        self.hero_repository = hero_repository

    async def _parse_to_public(self, hero: Hero) -> HeroPublic:
        return HeroPublic(**hero.model_dump())

    async def create_hero(self, hero_create: HeroCreate) -> HeroPublic:
        hero = await self.hero_repository.create(hero_create)
        return await self._parse_to_public(hero)

    async def get_hero(self, uuid: UUID) -> HeroPublic:
        hero = await self.hero_repository.get(uuid)
        return await self._parse_to_public(hero)

    async def update_hero(self, uuid: UUID, hero_update: HeroUpdate) -> HeroPublic:
        hero = await self.hero_repository.get(uuid)
        hero = await self.hero_repository.update(hero, hero_update)
        return await self._parse_to_public(hero)

    async def delete_hero(self, uuid: UUID) -> None:
        hero = await self.hero_repository.get(uuid)
        await self.hero_repository.delete(hero)
