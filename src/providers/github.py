from typing import List, Optional

import requests

from src.schemas.repository import Repository
from src.schemas.user import UserOutput


class GitHub:

    @classmethod
    def get_user(cls, username: str) -> Optional[UserOutput]:
        try:
            user = requests.get(f'https://api.github.com/users/{username}')
            user.raise_for_status()

            user = user.json()
            return UserOutput(id=user['id'],
                              login=user['login'],
                              twitter_username=user['twitter_username'],
                              email=user['email'])
        except requests.exceptions.HTTPError:
            return None

    @classmethod
    def get_repository(cls, username: str, repository_name: str) -> Optional[Repository]:
        repository = requests.get(f'https://api.github.com/repos/{username}/{repository_name}')
        if repository.status_code == 404:
            return None
        repository = repository.json()

        return Repository(id=repository['id'],
                          name=repository['name'],
                          private=repository['private'],
                          created_at=repository['created_at'],
                          updated_at=repository['updated_at'],
                          size=repository['size'],
                          stars=repository['stargazers_count'],
                          watchers=repository['watchers_count'])

    @classmethod
    def get_all_repos(cls, username: str) -> List[Repository]:
        repo_request = requests.get(f'https://api.github.com/users/{username}/repos')
        repositories = []
        try:
            repo_request.raise_for_status()
            for repository in repo_request.json():
                repositories.append(Repository(id=repository['id'],
                                               name=repository['name'],
                                               private=repository['private'],
                                               created_at=repository['created_at'],
                                               updated_at=repository['updated_at'],
                                               size=repository['size'],
                                               stars=repository['stargazers_count'],
                                               watchers=repository['watchers_count']))
        except requests.exceptions.HTTPError:
            pass
        finally:
            return repositories
