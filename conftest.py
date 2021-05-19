import pytest
from fastapi.testclient import TestClient
from src.main import APP
from src.services.database import run_migration, MigrationType, SESSION


@pytest.fixture
def web_client():
    client = TestClient(APP)
    yield client


@pytest.fixture
def database_client():
    run_migration(migration_type=MigrationType.DOWNGRADE, revision='base')
    run_migration(migration_type=MigrationType.UPGRADE, revision='head')
    session = SESSION()
    yield session
    session.close()


@pytest.fixture
@pytest.mark.parametrize('username,provider,repository', [('HectorMenezes', 'github', 'Captalys'),
                                               ('BabarZahoor', 'gitlab', 'Airflow')])
def create_user(web_client, username, provider, repository):
    web_client.get(f'/repository/{username}/{repository}?',
                   params={'provider': provider,
                           'save_data': True})
