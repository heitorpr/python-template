from fastapi import Depends

from src.domain.repositories import HeroRepository
from src.web.deps.repositories import get_hero_repository
from src.web.services import HeroService


def get_hero_service(
    hero_repository: HeroRepository = Depends(get_hero_repository),
) -> HeroService:
    return HeroService(hero_repository=hero_repository)
