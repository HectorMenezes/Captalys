from typing import List, Optional

from src.models.user import ProviderType
from src.providers.base import BaseProvider
from src.providers.github import GitHub
from src.providers.gitlab import GitLab
from src.schemas.repository import Repository
from src.schemas.user import UserOutput


class Dealer:
    def __init__(self):
        self.providers = dict(gitlab=GitLab, github=GitHub)

    def get_provider(self, provider: ProviderType) -> Optional[BaseProvider]:
        return self.providers.get(provider.value)


dealer = Dealer()

