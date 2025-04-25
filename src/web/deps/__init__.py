from typing import Annotated

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.deps.db import get_db_session
from src.web.deps.services import get_hero_service, get_team_service
from src.web.services import HeroService, TeamService

SessionDep = Annotated[AsyncSession, Depends(get_db_session)]
HeroServiceDep = Annotated[HeroService, Depends(get_hero_service)]
TeamServiceDep = Annotated[TeamService, Depends(get_team_service)]
