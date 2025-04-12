from uuid import UUID

from fastapi import APIRouter, HTTPException, status
from sqlalchemy.exc import IntegrityError

from src.domain.models.hero import HeroCreate, HeroPublic, HeroUpdate
from src.domain.repositories.exceptions import NoHeroFound, NoTeamFound
from src.web.deps import HeroServiceDep

router = APIRouter()


@router.post(
    "/",
    summary="Create a hero",
    description="Create a hero with all the information",
    tags=["heroes"],
    response_model=HeroPublic,
    status_code=status.HTTP_201_CREATED,
    responses={
        status.HTTP_400_BAD_REQUEST: {"description": "Hero already exists"},
        status.HTTP_404_NOT_FOUND: {"description": "Team not found"},
    },
)
async def create_hero(hero_create: HeroCreate, service: HeroServiceDep):
    try:
        return await service.create_hero(hero_create)
    except IntegrityError as error:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Hero already exists"
        ) from error
    except NoTeamFound as error:
        raise HTTPException(status_code=404, detail=str(error)) from error


@router.get(
    "/{uuid}",
    summary="get a hero",
    description="Get a hero using the uuid",
    tags=["heroes"],
    response_model=HeroPublic,
    status_code=status.HTTP_200_OK,
    responses={
        status.HTTP_404_NOT_FOUND: {"description": "Hero not found"},
    },
)
async def get_hero(uuid: UUID, service: HeroServiceDep):
    try:
        return await service.get_hero(uuid)
    except NoHeroFound as error:
        raise HTTPException(status_code=404, detail=str(error)) from error


@router.put(
    "/{uuid}",
    summary="Update a hero",
    description="Update a hero using the uuid",
    tags=["heroes"],
    response_model=HeroPublic,
    status_code=status.HTTP_200_OK,
    responses={
        status.HTTP_400_BAD_REQUEST: {"description": "Hero already exists"},
        status.HTTP_404_NOT_FOUND: {"description": "Hero not found"},
    },
)
async def update_hero(uuid: UUID, hero_update: HeroUpdate, service: HeroServiceDep):
    try:
        return await service.update_hero(uuid, hero_update)
    except IntegrityError as error:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Hero already exists"
        ) from error
    except (NoHeroFound, NoTeamFound) as error:
        raise HTTPException(status_code=404, detail=str(error)) from error


@router.delete(
    "/{uuid}",
    summary="Delete a hero",
    description="Delete a hero using the uuid",
    tags=["heroes"],
    status_code=status.HTTP_204_NO_CONTENT,
    responses={
        status.HTTP_404_NOT_FOUND: {"description": "Hero not found"},
    },
)
async def delete_hero(uuid: UUID, service: HeroServiceDep):
    try:
        await service.delete_hero(uuid)
    except NoHeroFound as error:
        raise HTTPException(status_code=404, detail=str(error)) from error
