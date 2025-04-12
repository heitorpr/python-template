from uuid import UUID

from fastapi import APIRouter, HTTPException, status
from sqlalchemy.exc import IntegrityError

from src.domain.models.hero import HeroPublic
from src.domain.models.team import TeamCreate, TeamPublic, TeamUpdate
from src.domain.repositories.exceptions import NoTeamFound
from src.web.deps import TeamServiceDep

router = APIRouter()


@router.post(
    "/",
    summary="Create a team",
    description="Create a team with all the information",
    tags=["teams"],
    response_model=TeamPublic,
    status_code=status.HTTP_201_CREATED,
    responses={
        status.HTTP_400_BAD_REQUEST: {"description": "Team already exists"},
    },
)
async def create_team(team_create: TeamCreate, service: TeamServiceDep):
    try:
        return await service.create_team(team_create)
    except IntegrityError as error:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Team already exists"
        ) from error


@router.get(
    "/{uuid}",
    summary="get a team",
    description="Get a team using the uuid",
    tags=["teams"],
    response_model=TeamPublic,
    status_code=status.HTTP_200_OK,
    responses={
        status.HTTP_404_NOT_FOUND: {"description": "Team not found"},
    },
)
async def get_team(uuid: UUID, service: TeamServiceDep):
    try:
        return await service.get_team(uuid)
    except NoTeamFound as error:
        raise HTTPException(status_code=404, detail=str(error)) from error


@router.put(
    "/{uuid}",
    summary="Update a team",
    description="Update a team using the uuid",
    tags=["teams"],
    response_model=TeamPublic,
    status_code=status.HTTP_200_OK,
    responses={
        status.HTTP_404_NOT_FOUND: {"description": "Team not found"},
    },
)
async def update_team(uuid: UUID, team_update: TeamUpdate, service: TeamServiceDep):
    try:
        return await service.update_team(uuid, team_update)
    except NoTeamFound as error:
        raise HTTPException(status_code=404, detail=str(error)) from error


@router.delete(
    "/{uuid}",
    summary="Delete a team",
    description="Delete a team using the uuid",
    tags=["teams"],
    status_code=status.HTTP_204_NO_CONTENT,
    responses={
        status.HTTP_404_NOT_FOUND: {"description": "Team not found"},
    },
)
async def delete_team(uuid: UUID, service: TeamServiceDep):
    try:
        return await service.delete_team(uuid)
    except NoTeamFound as error:
        raise HTTPException(status_code=404, detail=str(error)) from error


@router.get(
    "/{uuid}/heroes",
    summary="Get heroes from a team",
    description="Get heroes from a team using the uuid",
    tags=["teams"],
    response_model=list[HeroPublic],
    status_code=status.HTTP_200_OK,
    responses={
        status.HTTP_404_NOT_FOUND: {"description": "Team not found"},
    },
)
async def get_team_heroes(uuid: UUID, service: TeamServiceDep):
    try:
        return await service.get_heroes(uuid)
    except NoTeamFound as error:
        raise HTTPException(status_code=404, detail=str(error)) from error
