import pytest
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session
from unittest import mock


@pytest.mark.parametrize('username,provider', [('BabarZahoor', 'gitlab')])
def test_get_all_repositories_from_specific_valid_user(web_client, username, provider):
    result = web_client.get(f'/repository/repos/{username}',
                            params=dict(provider=provider))
    response = result.json()
    print(result)
    print(response)
    assert result.status_code == 200
    assert isinstance(response, list)
    assert list(response[0].keys()) == ['id', 'name', 'private', 'created_at',
                                        'updated_at', 'size', 'stars', 'watchers']


def test_get_all_repositories_from_specific_invalid_user(web_client):
    username = 'ввфцфвфвафацвфц'
    result = web_client.get(f'/repository/repos/{username}',
                            params=dict(provider='github'))
    print(result)
    response = result.json()
    assert result.status_code == 404
    assert response == 'User not found in remotely'


@pytest.mark.parametrize('username,provider', [('HectorMenezes', 'github'),
                                               ('BabarZahoor', 'gitlab')])
def test_get_user_from_remote_valid_user(web_client, username, provider):
    result = web_client.get(f'/repository/{username}?',
                            params={'provider': provider})
    response = result.json()

    assert result.status_code == 200
    assert list(response.keys()) == ['id', 'login', 'email', 'twitter_username', 'repos']


@pytest.mark.parametrize('username,provider', [('АВРЦВГВОФШГВРФЦ', 'github'), ('ФЫВЛДОФЫВ', 'gitlab')])
def test_get_user_from_remote_invalid_user(web_client, username, provider):
    result = web_client.get(f'/repository/{username}?',
                            params={'provider': provider})
    response = result.json()

    assert result.status_code == 404
    assert response == 'User not found remotely'


def test_get_user_from_local_invalid_user(web_client, database_client):
    username = 'RRRRRRR'
    result = web_client.get(f'/repository/{username}?',
                            params={'provider': 'github',
                                    'from_local': True})
    response = result.json()
    assert result.status_code == 404
    assert response == 'User not found in database'


@pytest.mark.parametrize('username,provider,repository', [('HectorMenezes', 'github', 'Captalys'),
                                                          ('BabarZahoor', 'gitlab', 'Airflow')])
def test_get_user_from_local_valid_user(web_client, database_client, create_user, username, provider, repository):
    result = web_client.get(f'/repository/{username}',
                            params={'provider': provider,
                                    'from_local': True})
    response = result.json()
    assert result.status_code == 200
    assert list(response.keys()) == ['id', 'login', 'email', 'twitter_username', 'repos']


@pytest.mark.parametrize('username,provider,repository', [('HectorMenezes', 'github', 'Captalys')])
def test_get_repository_from_remote_valid_repository_save_data_true_data_base_error_at_user(web_client, database_client,
                                                                                            username, provider,
                                                                                            repository):
    with mock.patch.object(Session, 'commit', side_effect=SQLAlchemyError):
        result = web_client.get(f'/repository/{username}/{repository}?',
                                params={'provider': provider,
                                        'save_data': True})
        response = result.json()
        assert result.status_code == 500
        assert 'message' in response
        assert 'details' in response
        assert response['message'] == 'Database error'


"""

@pytest.mark.parametrize('username,provider,repository', [('HectorMenezes', 'github', 'AffirmationsAndroid')])
def test_get_repository_from_remote_valid_repository_save_data_true_data_base_error_at_repository(web_client,
                                                                                                  database_client,
                                                                                                  create_user, username,
                                                                                                  provider, repository):
    # For some reason this simply doesn't work:
    with mock.patch.object(Session, 'commit', side_effect=SQLAlchemyError):
        result = web_client.get(f'/repository/{username}/{repository}?',
                                params={'provider': provider,
                                        'save_data': True})
        response = result.json()
        assert result.status_code == 500
        assert 'message' in response
        assert 'details' in response
        assert response['message'] == 'Database error'
"""


def test_delete_user_from_local_non_existing_user(web_client, database_client):
    username = 'JORGE'
    result = web_client.delete(f'/repository/{username}',
                               params={'provider': 'github'})
    response = result.json()
    assert result.status_code == 200
    assert response == 'User deleted'


@pytest.mark.parametrize('username,provider,repository', [('HectorMenezes', 'github', 'Captalys'),
                                                          ('BabarZahoor', 'gitlab', 'Airflow')])
def test_delete_user_from_local_valid_user(web_client, database_client, create_user, username, repository, provider):
    web_client.delete(f'/repository/{username}/{repository}',
                      params={'provider': provider})

    result = web_client.delete(f'/repository/{username}',
                               params={'provider': provider})

    response = result.json()

    assert result.status_code == 200
    assert response == 'User deleted'


@pytest.mark.parametrize('username,provider,repository', [('HectorMenezes', 'github', 'Captalys')])
def test_delete_user_from_local_valid_user_existing_repository_constraint_violation(web_client, database_client,
                                                                                    create_user, username,
                                                                                    repository, provider):
    result = web_client.delete(f'/repository/{username}',
                               params={'provider': provider})

    response = result.json()

    assert result.status_code == 400
    assert response['message'] == 'Constraint violation'


@pytest.mark.parametrize('username,provider,repository', [('HectorMenezes', 'github', 'Captalys')])
def test_delete_user_from_local_valid_data_base_error(web_client, database_client, create_user,
                                                      username, repository, provider):
    web_client.delete(f'/repository/{username}/{repository}',
                      params={'provider': provider})
    with mock.patch.object(Session, 'commit', side_effect=SQLAlchemyError):
        result = web_client.delete(f'/repository/{username}',
                                   params={'provider': provider})
        response = result.json()
        print(response)
        assert result.status_code == 500
        assert 'message' in response
        assert 'details' in response
        assert response['message'] == 'Database error'


def test_get_repository_remotely_not_found(web_client, database_client):
    username = 'HectorMenezes_'
    repository = 'abcdefg'
    result = web_client.get(f'/repository/{username}/{repository}',
                            params={'provider': 'github',
                                    'save_data': False})
    response = result.json()
    print(response)
    assert result.status_code == 404
    assert response['message'] == 'Repository not found'


@pytest.mark.parametrize('username,provider,repository', [('HectorMenezes', 'github', 'Captalys')])
def test_patch_user_valid_remotely_and_locally(web_client, database_client, create_user, username, provider):
    result = web_client.patch(f'/repository/{username}',
                              params={'provider': provider})
    response = result.json()
    assert result.status_code == 200
    assert response == 'User updated successfully'


def test_patch_user_invalid_remotely(web_client, database_client):
    username = 'ДФЦЬВЖЩФЗЩЛЧ'
    result = web_client.patch(f'/repository/{username}',
                              params={'provider': 'gitlab'})
    response = result.json()
    assert result.status_code == 404
    assert response['message'] == 'User not found remotely'


def test_patch_user_invalid_locally(web_client, database_client):
    username = 'joeydoesntsharefood'
    result = web_client.patch(f'/repository/{username}',
                              params={'provider': 'github'})
    response = result.json()
    assert result.status_code == 404
    assert response['message'] == 'User not found in database'


@pytest.mark.parametrize('username,provider,repository', [('HectorMenezes', 'github', 'Captalys')])
def test_patch_user_data_base_error(web_client, database_client, create_user, username):
    with mock.patch.object(Session, 'commit', side_effect=SQLAlchemyError):
        result = web_client.patch(f'/repository/{username}',
                                  params={'provider': 'github'})
        response = result.json()
        assert result.status_code == 500
        assert 'message' in response
        assert 'details' in response
        assert response['message'] == 'Database error'
