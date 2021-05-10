from typing import List, Optional

from src.models.user import ProviderType
from src.providers.base import BaseProvider
from src.providers.github import GitHub
from src.providers.gitlab import GitLab
from src.schemas.repository import Repository
from src.schemas.user import UserOutput


class Dealer:

    @classmethod
    def get_provider(cls, provider: ProviderType) -> Optional[BaseProvider]:
        if provider == ProviderType.GITHUB:
            return GitHub
        return GitLab
