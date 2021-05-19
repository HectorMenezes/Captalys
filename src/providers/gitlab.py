from typing import List, Optional

import requests

from src.providers.base import BaseProvider
from src.schemas.repository import Repository
from src.schemas.user import UserOutput


class GitLab(BaseProvider):

    @classmethod
    def get_user(cls, username: str) -> Optional[UserOutput]:
        try:
            user = requests.get(f'https://gitlab.com/api/v4/users?username={username}')
            user.raise_for_status()

            user = user.json()
            if not user:
                return None
            user = user[0]
            return UserOutput(id=user['id'],
                              login=user['username'])

        except requests.exceptions.HTTPError:
            return None

    @classmethod
    def get_repository(cls, username: str, repository_name: str) -> Optional[Repository]:
        repos = cls._get_all_repos(username=username)

        for repository in repos:
            if repository.name == repository_name:
                return repository
        return None

    @classmethod
    def _get_all_repos(cls, username: str) -> List[Repository]:
        repos = requests.get(f'https://gitlab.com/api/v4/users/{username}/projects')
        repos.raise_for_status()

        repositories = []
        for repository in repos.json():
            repositories.append(Repository(id=repository['id'],
                                           name=repository['name'],
                                           created_at=repository['created_at'],
                                           updated_at=repository['last_activity_at'],
                                           stars=repository['star_count']))
        return repositories

    @classmethod
    def get_all_repos(cls, username: str) -> List[Repository]:
        return cls._get_all_repos(username=username)
