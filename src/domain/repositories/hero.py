from uuid import UUID

from sqlalchemy.exc import NoResultFound
from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import select

from src.domain.models import Hero, Team
from src.domain.models.hero import HeroCreate, HeroUpdate
from src.domain.repositories.exceptions import NoHeroFound


class HeroRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create(self, hero_create: HeroCreate, team: Team | None = None) -> Hero:
        hero = Hero(
            **hero_create.model_dump(exclude_unset=True),
            team_id=team.id if team else None,
        )

        self.session.add(hero)
        await self.session.flush()

        return hero

    async def get(self, hero_id: int | UUID) -> Hero:
        statement = select(Hero)

        if isinstance(hero_id, int):
            statement = statement.where(Hero.id == hero_id)
        else:
            statement = statement.where(Hero.uuid == hero_id)

        try:
            result = await self.session.execute(statement)
            return result.scalar_one()
        except NoResultFound as error:
            raise NoHeroFound("Hero not found") from error

    async def update(self, hero: Hero, hero_update: HeroUpdate, team: Team | None = None) -> Hero:
        for key, value in hero_update.model_dump(exclude_unset=True).items():
            setattr(hero, key, value)

        if team:
            hero.team_id = team.id

        self.session.add(hero)
        await self.session.flush()
        return hero

    async def delete(self, hero: Hero) -> None:
        await self.session.delete(hero)
        await self.session.flush()

    async def get_by_team(self, team_id: int) -> list[Hero]:
        statement = select(Hero).where(Hero.team_id == team_id)

        result = await self.session.execute(statement)
        return list(result.scalars().all())
