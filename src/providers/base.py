from abc import ABC, abstractmethod
from typing import Optional, List

from src.schemas.repository import Repository
from src.schemas.user import UserOutput


class BaseProvider(ABC):

    @classmethod
    @abstractmethod
    def get_user(cls, username: str) -> Optional[UserOutput]:
        ...

    @classmethod
    @abstractmethod
    def get_repository(cls, username: str, repository_name: str) -> Optional[Repository]:
        ...

    @classmethod
    @abstractmethod
    def get_all_repos(cls, username: str) -> List[Repository]:
        ...
