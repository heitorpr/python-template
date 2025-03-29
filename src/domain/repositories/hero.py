from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import select

from src.domain.models import Hero
from src.domain.models.hero import HeroCreate, HeroUpdate


class HeroRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create(self, hero_create: HeroCreate) -> Hero:
        hero = Hero(**hero_create.model_dump(exclude_unset=True))

        self.session.add(hero)
        await self.session.flush()

        return hero

    async def get(self, hero_id: int | UUID) -> Hero:
        statement = select(Hero)

        if isinstance(hero_id, int):
            statement = statement.where(Hero.id == hero_id)
        else:
            statement = statement.where(Hero.uuid == hero_id)

        result = await self.session.execute(statement)
        return result.scalar_one()

    async def update(self, hero: Hero, hero_update: HeroUpdate) -> Hero:
        for key, value in hero_update.model_dump(exclude_unset=True).items():
            setattr(hero, key, value)

        self.session.add(hero)
        await self.session.flush()
        return hero

    async def delete(self, hero: Hero) -> None:
        await self.session.delete(hero)
        await self.session.flush()
