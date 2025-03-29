import pytest
from sqlalchemy.exc import IntegrityError, NoResultFound

from src.domain.models.hero import HeroCreate, HeroUpdate
from src.domain.repositories.hero import HeroRepository


@pytest.fixture()
async def hero_create():
    return HeroCreate(
        name="Test Hero",
        secret_name="Test Secret Name",
        age=30,
    )


@pytest.mark.asyncio(loop_scope="session")
async def test_create_hero(db_session, hero_create):
    repository = HeroRepository(session=db_session)

    hero = await repository.create(hero_create)

    assert hero.id is not None
    assert hero.name == "Test Hero"


@pytest.mark.asyncio(loop_scope="session")
async def test_get_hero(db_session, hero_create):
    repository = HeroRepository(session=db_session)

    hero = await repository.create(hero_create)
    hero_from_db = await repository.get(hero_id=hero.id)
    assert hero_from_db == hero


@pytest.mark.asyncio(loop_scope="session")
async def test_create_hero_unique_secret_name(db_session, hero_create):
    repository = HeroRepository(session=db_session)

    await repository.create(hero_create)

    with pytest.raises(IntegrityError):
        await repository.create(hero_create)


@pytest.mark.asyncio(loop_scope="session")
async def test_update_hero(db_session, hero_create):
    repository = HeroRepository(session=db_session)

    hero = await repository.create(hero_create)
    hero_update = HeroUpdate(name="New Name")

    updated_hero = await repository.update(hero, hero_update=hero_update)
    assert updated_hero.name == "New Name"


@pytest.mark.asyncio(loop_scope="session")
async def test_delete_hero(db_session, hero_create):
    repository = HeroRepository(session=db_session)

    hero = await repository.create(hero_create)
    await repository.delete(hero)

    with pytest.raises(NoResultFound):
        await repository.get(hero_id=hero.id)


@pytest.mark.asyncio(loop_scope="session")
async def test_get_hero_using_uuid(db_session, hero_create):
    repository = HeroRepository(session=db_session)

    hero = await repository.create(hero_create)
    found_hero = await repository.get(hero_id=hero.uuid)

    assert found_hero == hero
