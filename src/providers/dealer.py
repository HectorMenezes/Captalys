from typing import List, Optional

from src.models.user import ProviderType
from src.providers.github import GitHub
from src.providers.gitlab import GitLab
from src.schemas.repository import Repository
from src.schemas.user import UserOutput


class Dealer:

    @classmethod
    def get_user(cls, username: str, provider: ProviderType) -> Optional[UserOutput]:
        if provider == ProviderType.GITHUB:
            return GitHub.get_user(username=username)
        return GitLab.get_user(username=username)

    @classmethod
    def get_repository(cls, username: str, repository_name: str,
                       provider: ProviderType) -> Optional[Repository]:
        if provider == ProviderType.GITHUB:
            return GitHub.get_repository(username=username, repository_name=repository_name)
        return GitLab.get_repository(username=username, repository_name=repository_name)

    @classmethod
    def get_all_repos(cls, username: str, provider: ProviderType) -> List[Repository]:
        if provider == ProviderType.GITHUB:
            return GitHub.get_all_repos(username=username)
        return GitLab.get_all_repos(username=username)
