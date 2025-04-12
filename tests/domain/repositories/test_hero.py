import pytest
from sqlalchemy.exc import IntegrityError

from src.domain.models.hero import HeroUpdate
from src.domain.repositories.exceptions import NoHeroFound
from src.domain.repositories.hero import HeroRepository


@pytest.mark.asyncio(loop_scope="session")
async def test_create_hero(db_session, hero_create):
    repository = HeroRepository(session=db_session)

    hero = await repository.create(hero_create)

    assert hero.id is not None
    assert hero.name == "Test Hero"


@pytest.mark.asyncio(loop_scope="session")
async def test_get_hero(db_session, hero):
    repository = HeroRepository(session=db_session)
    hero_from_db = await repository.get(hero_id=hero.id)
    assert hero_from_db == hero


@pytest.mark.asyncio(loop_scope="session")
async def test_update_hero(db_session, hero):
    repository = HeroRepository(session=db_session)
    hero_update = HeroUpdate(name="New Name")

    updated_hero = await repository.update(hero, hero_update=hero_update)
    assert updated_hero.name == "New Name"


@pytest.mark.asyncio(loop_scope="session")
async def test_delete_hero(db_session, hero):
    repository = HeroRepository(session=db_session)
    await repository.delete(hero)

    with pytest.raises(NoHeroFound):
        await repository.get(hero_id=hero.id)


@pytest.mark.asyncio(loop_scope="session")
async def test_create_hero_unique_secret_name(db_session, hero_create):
    repository = HeroRepository(session=db_session)

    await repository.create(hero_create)

    with pytest.raises(IntegrityError):
        await repository.create(hero_create)


@pytest.mark.asyncio(loop_scope="session")
async def test_get_hero_using_uuid(db_session, hero):
    repository = HeroRepository(session=db_session)
    found_hero = await repository.get(hero_id=hero.uuid)

    assert found_hero == hero


@pytest.mark.asyncio(loop_scope="session")
async def test_create_hero_with_team(db_session, hero_create, team):
    repository = HeroRepository(session=db_session)

    hero_create.team_uuid = team.uuid
    hero = await repository.create(hero_create, team=team)

    assert hero.team_id == team.id
    assert hero.team_uuid == team.uuid


@pytest.mark.asyncio(loop_scope="session")
async def test_update_hero_with_team(db_session, hero, team):
    repository = HeroRepository(session=db_session)

    hero_update = HeroUpdate(team_uuid=team.uuid)
    updated_hero = await repository.update(hero, hero_update=hero_update, team=team)

    assert updated_hero.team_id == team.id
    assert updated_hero.team_uuid == team.uuid


@pytest.mark.asyncio(loop_scope="session")
async def test_get_hero_by_team(db_session, hero, team):
    repository = HeroRepository(session=db_session)

    await repository.update(hero, HeroUpdate(team_uuid=team.uuid), team=team)

    heroes = await repository.get_by_team(team_id=team.id)

    assert len(heroes) == 1
    assert heroes[0] == hero
