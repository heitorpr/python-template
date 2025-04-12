import pytest
from fastapi import status
from sqlalchemy.exc import IntegrityError
from uuid6 import uuid7

from src.domain.models.hero import HeroPublic, HeroUpdate
from src.domain.repositories.exceptions import NoHeroFound, NoTeamFound
from src.web.deps.services import get_hero_service
from src.web.main import app
from src.web.services import HeroService


@pytest.mark.asyncio(loop_scope="session")
async def test_create_hero(client, hero_create, auth_headers):
    body = hero_create.model_dump(mode="json")
    response = await client.post("/api/heroes/", json=body, headers=auth_headers("POST", body))
    assert response.status_code == status.HTTP_201_CREATED

    hero = HeroPublic(**response.json())

    assert hero.uuid
    assert hero.name == hero_create.name
    assert hero.secret_name == hero_create.secret_name
    assert hero.age == hero_create.age


@pytest.mark.asyncio(loop_scope="session")
async def test_get_hero(client, hero, auth_headers):
    response = await client.get(f"/api/heroes/{hero.uuid}", headers=auth_headers("GET", {}))
    assert response.status_code == status.HTTP_200_OK

    hero_from_response = HeroPublic(**response.json())

    assert hero_from_response.uuid == hero.uuid
    assert hero_from_response.name == hero.name
    assert hero_from_response.secret_name == hero.secret_name
    assert hero_from_response.age == hero.age


@pytest.mark.asyncio(loop_scope="session")
async def test_update_hero(client, hero, auth_headers):
    hero_update = HeroUpdate(age=22)

    body = hero_update.model_dump(mode="json", exclude_unset=True)
    response = await client.put(
        f"/api/heroes/{hero.uuid}", json=body, headers=auth_headers("PUT", body)
    )
    assert response.status_code == status.HTTP_200_OK

    hero_from_response = HeroPublic(**response.json())

    assert hero_from_response.age == hero_update.age


@pytest.mark.asyncio(loop_scope="session")
async def test_delete_hero(client, hero, auth_headers):
    response = await client.delete(f"/api/heroes/{hero.uuid}", headers=auth_headers("DELETE", {}))
    assert response.status_code == status.HTTP_204_NO_CONTENT

    response = await client.get(f"/api/heroes/{hero.uuid}", headers=auth_headers("GET", {}))
    assert response.status_code == status.HTTP_404_NOT_FOUND


@pytest.mark.asyncio(loop_scope="session")
async def test_get_hero_not_found(client, auth_headers, mocker):
    service_mock = mocker.MagicMock(HeroService)
    service_mock.get_hero.side_effect = NoHeroFound("Hero not found")

    def _override():
        return service_mock

    app.dependency_overrides[get_hero_service] = _override

    response = await client.get(f"/api/heroes/{uuid7()}", headers=auth_headers("GET", {}))
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json() == {"detail": "Hero not found"}

    app.dependency_overrides.clear()


@pytest.mark.asyncio(loop_scope="session")
async def test_create_hero_integrity_error(client, hero_create, auth_headers, mocker):
    service_mock = mocker.MagicMock(HeroService)
    service_mock.create_hero.side_effect = IntegrityError(
        statement="insert into heroes ...", params=None, orig=Exception()
    )

    def _override():
        return service_mock

    app.dependency_overrides[get_hero_service] = _override

    body = hero_create.model_dump(mode="json")
    response = await client.post("/api/heroes/", json=body, headers=auth_headers("POST", body))
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.json() == {"detail": "Hero already exists"}

    app.dependency_overrides.clear()


@pytest.mark.asyncio(loop_scope="session")
async def test_update_hero_not_found(client, auth_headers, mocker):
    service_mock = mocker.MagicMock(HeroService)
    service_mock.update_hero.side_effect = NoHeroFound("Hero not found")

    def _override():
        return service_mock

    app.dependency_overrides[get_hero_service] = _override
    body = HeroUpdate(age=22).model_dump(mode="json", exclude_unset=True)

    response = await client.put(
        f"/api/heroes/{uuid7()}", json=body, headers=auth_headers("PUT", body)
    )
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json() == {"detail": "Hero not found"}

    app.dependency_overrides.clear()


@pytest.mark.asyncio(loop_scope="session")
async def test_update_hero_integrity_error(client, auth_headers, mocker):
    service_mock = mocker.MagicMock(HeroService)
    service_mock.update_hero.side_effect = IntegrityError(
        statement="update heroes ...", params=None, orig=Exception()
    )

    def _override():
        return service_mock

    app.dependency_overrides[get_hero_service] = _override

    hero_update = HeroUpdate(age=22)
    body = hero_update.model_dump(mode="json", exclude_unset=True)

    response = await client.put(
        "/api/heroes/123e4567-e89b-12d3-a456-426614174000",
        json=body,
        headers=auth_headers("PUT", body),
    )
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.json() == {"detail": "Hero already exists"}

    app.dependency_overrides.clear()


@pytest.mark.asyncio(loop_scope="session")
async def test_delete_hero_not_found(client, auth_headers, mocker):
    service_mock = mocker.MagicMock(HeroService)
    service_mock.delete_hero.side_effect = NoHeroFound("Hero not found")

    def _override():
        return service_mock

    app.dependency_overrides[get_hero_service] = _override

    response = await client.delete(f"/api/heroes/{uuid7()}", headers=auth_headers("DELETE", {}))
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json() == {"detail": "Hero not found"}

    app.dependency_overrides.clear()


@pytest.mark.asyncio(loop_scope="session")
async def test_create_hero_with_team(client, hero_create, team, auth_headers):
    hero_create.team_uuid = team.uuid
    body = hero_create.model_dump(mode="json")

    response = await client.post("/api/heroes/", json=body, headers=auth_headers("POST", body))
    assert response.status_code == status.HTTP_201_CREATED

    hero = HeroPublic(**response.json())

    assert hero.team_uuid == team.uuid


@pytest.mark.asyncio(loop_scope="session")
async def test_create_hero_no_team_result_error(client, hero_create, auth_headers, mocker):
    service_mock = mocker.MagicMock(HeroService)
    service_mock.create_hero.side_effect = NoTeamFound("Team not found")

    def _override():
        return service_mock

    app.dependency_overrides[get_hero_service] = _override

    body = hero_create.model_dump(mode="json")
    response = await client.post("/api/heroes/", json=body, headers=auth_headers("POST", body))
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json() == {"detail": "Team not found"}

    app.dependency_overrides.clear()


@pytest.mark.asyncio(loop_scope="session")
async def test_update_hero_with_team(client, hero, team, auth_headers):
    hero_update = HeroUpdate(team_uuid=team.uuid)

    body = hero_update.model_dump(mode="json", exclude_unset=True)
    response = await client.put(
        f"/api/heroes/{hero.uuid}", json=body, headers=auth_headers("PUT", body)
    )
    assert response.status_code == status.HTTP_200_OK

    hero_from_response = HeroPublic(**response.json())

    assert hero_from_response.team_uuid == team.uuid


@pytest.mark.asyncio(loop_scope="session")
async def test_update_hero_with_team_not_found(client, hero, auth_headers):
    hero_update = HeroUpdate(team_uuid=uuid7())

    body = hero_update.model_dump(mode="json", exclude_unset=True)
    response = await client.put(
        f"/api/heroes/{hero.uuid}", json=body, headers=auth_headers("PUT", body)
    )
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json() == {"detail": "Team not found"}
