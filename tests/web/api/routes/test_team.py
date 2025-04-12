import pytest
from fastapi import status
from sqlalchemy.exc import IntegrityError
from uuid6 import uuid7

from src.domain.models.hero import HeroUpdate
from src.domain.models.team import TeamPublic, TeamUpdate
from src.domain.repositories.exceptions import NoTeamFound
from src.web.deps.services import get_team_service
from src.web.main import app
from src.web.services import TeamService


@pytest.fixture()
async def hero_with_team(hero, team, hero_repository):
    updated_hero = await hero_repository.update(hero, HeroUpdate(team_uuid=team.uuid), team=team)
    return updated_hero


@pytest.mark.asyncio(loop_scope="session")
async def test_create_team(client, team_create, auth_headers):
    body = team_create.model_dump(mode="json")
    response = await client.post("/api/teams/", json=body, headers=auth_headers("POST", body))
    assert response.status_code == status.HTTP_201_CREATED

    team = TeamPublic(**response.json())

    assert team.uuid
    assert team.name == team_create.name
    assert team.headquarters == team_create.headquarters


@pytest.mark.asyncio(loop_scope="session")
async def test_get_team(client, team, auth_headers):
    response = await client.get(f"/api/teams/{team.uuid}", headers=auth_headers("GET", {}))
    assert response.status_code == status.HTTP_200_OK

    team_from_response = TeamPublic(**response.json())

    assert team_from_response.uuid == team.uuid
    assert team_from_response.name == team.name
    assert team_from_response.headquarters == team.headquarters


@pytest.mark.asyncio(loop_scope="session")
async def test_update_team(client, team, auth_headers):
    team_update = TeamUpdate(name="New Name")

    body = team_update.model_dump(mode="json", exclude_unset=True)
    response = await client.put(
        f"/api/teams/{team.uuid}", json=body, headers=auth_headers("PUT", body)
    )
    assert response.status_code == status.HTTP_200_OK

    team_from_response = TeamPublic(**response.json())

    assert team_from_response.name == team_update.name


@pytest.mark.asyncio(loop_scope="session")
async def test_delete_team(client, team, auth_headers):
    response = await client.delete(f"/api/teams/{team.uuid}", headers=auth_headers("DELETE", {}))
    assert response.status_code == status.HTTP_204_NO_CONTENT

    response = await client.get(f"/api/teams/{team.uuid}", headers=auth_headers("GET", {}))
    assert response.status_code == status.HTTP_404_NOT_FOUND


@pytest.mark.asyncio(loop_scope="session")
async def test_get_team_not_found(client, auth_headers, mocker):
    service_mock = mocker.MagicMock(TeamService)
    service_mock.get_team.side_effect = NoTeamFound("Team not found")

    def _override():
        return service_mock

    app.dependency_overrides[get_team_service] = _override

    response = await client.get(f"/api/teams/{uuid7()}", headers=auth_headers("GET", {}))
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json() == {"detail": "Team not found"}

    app.dependency_overrides.clear()


@pytest.mark.asyncio(loop_scope="session")
async def test_create_team_integrity_error(client, team_create, auth_headers, mocker):
    service_mock = mocker.MagicMock(TeamService)
    service_mock.create_team.side_effect = IntegrityError(
        statement="insert into teams ...", params=None, orig=Exception()
    )

    def _override():
        return service_mock

    app.dependency_overrides[get_team_service] = _override

    body = team_create.model_dump(mode="json")
    response = await client.post("/api/teams/", json=body, headers=auth_headers("POST", body))
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.json() == {"detail": "Team already exists"}

    app.dependency_overrides.clear()


@pytest.mark.asyncio(loop_scope="session")
async def test_update_team_not_found(client, auth_headers, mocker):
    service_mock = mocker.MagicMock(TeamService)
    service_mock.update_team.side_effect = NoTeamFound("Team not found")

    def _override():
        return service_mock

    app.dependency_overrides[get_team_service] = _override
    body = TeamUpdate(name="New Name").model_dump(mode="json", exclude_unset=True)

    response = await client.put(
        f"/api/teams/{uuid7()}", json=body, headers=auth_headers("PUT", body)
    )
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json() == {"detail": "Team not found"}

    app.dependency_overrides.clear()


@pytest.mark.asyncio(loop_scope="session")
async def test_delete_team_not_found(client, auth_headers, mocker):
    service_mock = mocker.MagicMock(TeamService)
    service_mock.delete_team.side_effect = NoTeamFound("Team not found")

    def _override():
        return service_mock

    app.dependency_overrides[get_team_service] = _override

    response = await client.delete(f"/api/teams/{uuid7()}", headers=auth_headers("DELETE", {}))
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json() == {"detail": "Team not found"}

    app.dependency_overrides.clear()


@pytest.mark.asyncio(loop_scope="session")
async def test_get_team_heroes(client, hero_with_team, auth_headers):
    response = await client.get(
        f"/api/teams/{hero_with_team.team_uuid}/heroes", headers=auth_headers("GET", {})
    )
    assert response.status_code == status.HTTP_200_OK

    heroes = response.json()

    assert len(heroes) == 1
    assert heroes[0]["uuid"] == str(hero_with_team.uuid)
    assert heroes[0]["name"] == hero_with_team.name


@pytest.mark.asyncio(loop_scope="session")
async def test_get_team_heroes_not_found(client, auth_headers, mocker):
    service_mock = mocker.MagicMock(TeamService)
    service_mock.get_heroes.side_effect = NoTeamFound("Team not found")

    def _override():
        return service_mock

    app.dependency_overrides[get_team_service] = _override

    response = await client.get(f"/api/teams/{uuid7()}/heroes", headers=auth_headers("GET", {}))
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json() == {"detail": "Team not found"}

    app.dependency_overrides.clear()
