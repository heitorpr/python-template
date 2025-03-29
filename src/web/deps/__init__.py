from typing import Annotated

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.deps.db import get_db_session
from src.web.deps.services import get_hero_service
from src.web.services import HeroService

SessionDep = Annotated[AsyncSession, Depends(get_db_session)]
HeroServiceDep = Annotated[HeroService, Depends(get_hero_service)]
