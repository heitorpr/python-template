from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.deps.db import get_db_session
from src.domain.repositories import HeroRepository


def get_hero_repository(db: AsyncSession = Depends(get_db_session)) -> HeroRepository:
    return HeroRepository(db)
