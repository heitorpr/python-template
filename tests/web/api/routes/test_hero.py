import pytest

from src.domain.models.hero import HeroCreate, HeroPublic, HeroUpdate


@pytest.fixture()
async def hero_create():
    return HeroCreate(
        name="Test Hero",
        secret_name="Test Secret Name",
        age=30,
    )


@pytest.fixture()
async def hero(hero_repository, hero_create):
    return await hero_repository.create(hero_create)


@pytest.mark.asyncio(loop_scope="session")
async def test_create_hero(client, hero_create, auth_headers):
    body = hero_create.model_dump(mode="json")
    response = await client.post("/api/heroes/", json=body, headers=auth_headers("POST", body))
    assert response.status_code == 201

    hero = HeroPublic(**response.json())

    assert hero.uuid
    assert hero.name == hero_create.name
    assert hero.secret_name == hero_create.secret_name
    assert hero.age == hero_create.age


@pytest.mark.asyncio(loop_scope="session")
async def test_get_hero(client, hero, auth_headers):
    response = await client.get(f"/api/heroes/{hero.uuid}", headers=auth_headers("GET", ""))
    assert response.status_code == 200

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
    assert response.status_code == 200

    hero_from_response = HeroPublic(**response.json())

    assert hero_from_response.age == hero_update.age


@pytest.mark.asyncio(loop_scope="session")
async def test_delete_hero(client, hero, auth_headers):
    response = await client.delete(f"/api/heroes/{hero.uuid}", headers=auth_headers("DELETE", ""))
    assert response.status_code == 204

    response = await client.get(f"/api/heroes/{hero.uuid}", headers=auth_headers("GET", ""))
    assert response.status_code == 404
