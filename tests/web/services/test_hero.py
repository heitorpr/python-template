import pytest

from src.domain.models.hero import HeroPublic, HeroUpdate
from src.domain.repositories.exceptions import NoHeroFound
from src.web.services import HeroService


@pytest.fixture()
def hero_service(hero_repository, team_repository):
    return HeroService(hero_repository=hero_repository, team_repository=team_repository)


@pytest.mark.asyncio(loop_scope="session")
async def test_create_hero(hero_service, hero_create):
    hero = await hero_service.create_hero(hero_create)

    assert isinstance(hero, HeroPublic)
    assert hero.secret_name == hero_create.secret_name


@pytest.mark.asyncio(loop_scope="session")
async def test_get_hero(hero_service, hero):
    found_hero = await hero_service.get_hero(hero.uuid)

    assert isinstance(found_hero, HeroPublic)
    assert found_hero.secret_name == hero.secret_name


@pytest.mark.asyncio(loop_scope="session")
async def test_update_hero(hero_service, hero):
    update_data = HeroUpdate(name="New Name")
    updated_hero = await hero_service.update_hero(hero.uuid, update_data)

    assert isinstance(updated_hero, HeroPublic)
    assert updated_hero.name == update_data.name


@pytest.mark.asyncio(loop_scope="session")
async def test_delete_hero(hero_service, hero):
    await hero_service.delete_hero(hero.uuid)

    with pytest.raises(NoHeroFound):
        await hero_service.get_hero(hero.uuid)


@pytest.mark.asyncio(loop_scope="session")
async def test_create_hero_with_team(hero_service, hero_create, team):
    hero_create.team_uuid = team.uuid
    hero = await hero_service.create_hero(hero_create)

    assert isinstance(hero, HeroPublic)
    assert hero.team_uuid == team.uuid


@pytest.mark.asyncio(loop_scope="session")
async def test_update_hero_with_team(hero_service, hero, team):
    update_data = HeroUpdate(team_uuid=team.uuid)
    updated_hero = await hero_service.update_hero(hero.uuid, update_data)

    assert isinstance(updated_hero, HeroPublic)
    assert updated_hero.team_uuid == team.uuid
