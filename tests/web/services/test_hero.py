import pytest
from sqlalchemy.exc import NoResultFound

from src.domain.models.hero import HeroPublic, HeroUpdate
from src.web.services import HeroService


@pytest.mark.asyncio(loop_scope="session")
async def test_create_hero(hero_repository, hero_create):
    service = HeroService(hero_repository=hero_repository)
    hero = await service.create_hero(hero_create)

    assert isinstance(hero, HeroPublic)
    assert hero.secret_name == hero_create.secret_name


@pytest.mark.asyncio(loop_scope="session")
async def test_get_hero(hero_repository, hero):
    service = HeroService(hero_repository=hero_repository)
    found_hero = await service.get_hero(hero.uuid)

    assert isinstance(found_hero, HeroPublic)
    assert found_hero.secret_name == hero.secret_name


@pytest.mark.asyncio(loop_scope="session")
async def test_update_hero(hero_repository, hero):
    service = HeroService(hero_repository=hero_repository)

    update_data = HeroUpdate(name="New Name")
    updated_hero = await service.update_hero(hero.uuid, update_data)

    assert isinstance(updated_hero, HeroPublic)
    assert updated_hero.name == update_data.name


@pytest.mark.asyncio(loop_scope="session")
async def test_delete_hero(hero_repository, hero):
    service = HeroService(hero_repository=hero_repository)

    await service.delete_hero(hero.uuid)

    with pytest.raises(NoResultFound):
        await service.get_hero(hero.uuid)
