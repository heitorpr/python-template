from fastapi import Depends

from src.domain.repositories import HeroRepository, TeamRepository
from src.web.deps.repositories import get_hero_repository, get_team_repository
from src.web.services import HeroService, TeamService


def get_hero_service(
    hero_repository: HeroRepository = Depends(get_hero_repository),
    team_repository: TeamRepository = Depends(get_team_repository),
) -> HeroService:
    return HeroService(hero_repository=hero_repository, team_repository=team_repository)


def get_team_service(
    team_repository: TeamRepository = Depends(get_team_repository),
    hero_repository: HeroRepository = Depends(get_hero_repository),
) -> TeamService:
    return TeamService(team_repository=team_repository, hero_repository=hero_repository)
