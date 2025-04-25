import pytest

from src.domain.models.hero import HeroPublic, HeroUpdate
from src.domain.models.team import TeamPublic, TeamUpdate
from src.domain.repositories.exceptions import NoTeamFound
from src.web.services import TeamService


@pytest.fixture()
def team_service(team_repository, hero_repository):
    return TeamService(team_repository=team_repository, hero_repository=hero_repository)


@pytest.mark.asyncio(loop_scope="session")
async def test_create_team(team_service, team_create):
    team = await team_service.create_team(team_create)

    assert isinstance(team, TeamPublic)
    assert team.name == team_create.name


@pytest.mark.asyncio(loop_scope="session")
async def test_get_team(team_service, team):
    found_team = await team_service.get_team(team.uuid)

    assert isinstance(found_team, TeamPublic)
    assert found_team.name == team.name


@pytest.mark.asyncio(loop_scope="session")
async def test_update_team(team_service, team):
    update_data = TeamUpdate(name="New Name")
    updated_team = await team_service.update_team(team.uuid, update_data)

    assert isinstance(updated_team, TeamPublic)
    assert updated_team.name == update_data.name


@pytest.mark.asyncio(loop_scope="session")
async def test_delete_team(team_service, team):
    await team_service.delete_team(team.uuid)

    with pytest.raises(NoTeamFound):
        await team_service.get_team(team.uuid)


@pytest.mark.asyncio(loop_scope="session")
async def test_get_team_heroes(team_service, hero_repository, team, hero):
    await hero_repository.update(hero, HeroUpdate(team_uuid=team.uuid), team=team)

    heroes = await team_service.get_heroes(team.uuid)

    assert len(heroes) == 1
    assert isinstance(heroes[0], HeroPublic)
    assert heroes[0].name == hero.name
