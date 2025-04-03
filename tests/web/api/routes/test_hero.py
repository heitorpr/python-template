import pytest
from fastapi import status
from sqlalchemy.exc import NoResultFound

from src.domain.models.hero import HeroPublic, HeroUpdate
from src.web.deps.services import get_hero_service
from src.web.main import app
from src.web.services.hero import HeroService


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
    service_mock.get_hero.side_effect = NoResultFound()

    def _override():
        return service_mock

    app.dependency_overrides[get_hero_service] = _override

    non_existent_uuid = "123e4567-e89b-12d3-a456-426614174000"

    response = await client.get(
        f"/api/heroes/{non_existent_uuid}", headers=auth_headers("GET", {})
    )
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json() == {"detail": "Hero not found"}

    app.dependency_overrides.clear()
