import pytest
from sqlalchemy.exc import IntegrityError

from src.domain.models.hero import HeroUpdate
from src.domain.models.team import TeamUpdate
from src.domain.repositories import HeroRepository, TeamRepository
from src.domain.repositories.exceptions import NoTeamFound


@pytest.mark.asyncio(loop_scope="session")
async def test_create_team(db_session, team_create):
    repository = TeamRepository(session=db_session)

    team = await repository.create(team_create)
    assert team.name == team_create.name
    assert team.headquarters == team_create.headquarters


@pytest.mark.asyncio(loop_scope="session")
async def test_get_team(db_session, team):
    repository = TeamRepository(session=db_session)
    team_from_db = await repository.get(team_id=team.id)
    assert team_from_db == team


@pytest.mark.asyncio(loop_scope="session")
async def test_update_team(db_session, team):
    repository = TeamRepository(session=db_session)

    team_update = TeamUpdate(name="New Name")
    updated_team = await repository.update(team, team_update)
    assert updated_team.name == "New Name"


@pytest.mark.asyncio(loop_scope="session")
async def test_delete_team(db_session, team):
    repository = TeamRepository(session=db_session)

    await repository.delete(team)

    with pytest.raises(NoTeamFound):
        await repository.get(team_id=team.id)


@pytest.mark.asyncio(loop_scope="session")
async def test_create_team_unique_name(db_session, team_create):
    repository = TeamRepository(session=db_session)

    await repository.create(team_create)

    with pytest.raises(IntegrityError):
        await repository.create(team_create)


@pytest.mark.asyncio(loop_scope="session")
async def test_get_team_using_uuid(db_session, team_create):
    repository = TeamRepository(session=db_session)

    team = await repository.create(team_create)
    team_from_db = await repository.get(team_id=team.uuid)
    assert team_from_db == team


@pytest.mark.asyncio(loop_scope="session")
async def test_delete_team_consistency_on_heroes(db_session, hero, team):
    repository = TeamRepository(session=db_session)
    hero_repository = HeroRepository(session=db_session)

    updated_hero = await hero_repository.update(
        hero=hero, hero_update=HeroUpdate(team_uuid=team.uuid), team=team
    )

    assert updated_hero.team_id == team.id
    assert updated_hero.team_uuid == team.uuid

    await repository.delete(team)

    get_hero = await hero_repository.get(hero_id=hero.id)
    assert get_hero.team_id is None
    assert get_hero.team_uuid is None
