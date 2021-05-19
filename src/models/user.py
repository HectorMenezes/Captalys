from enum import Enum
from typing import Optional

from sqlalchemy import Column, String, Integer, Enum as AlchemyEnum
from sqlalchemy.orm import relationship

from src.models.base import BasicCrud
from src.services.database import BaseModel, SESSION


class ProviderType(Enum):
    gitlab = 'gitlab'
    github = 'github'


class User(BaseModel, BasicCrud):
    __tablename__ = 'user'
    id = Column(Integer, primary_key=True, autoincrement=False)
    login = Column(String(100), nullable=False)
    email = Column(String(100), nullable=True)
    twitter_username = Column(String(100), nullable=True)
    provider = Column(AlchemyEnum(ProviderType), primary_key=True)
    repositories = relationship('Repository', back_populates="user")

    @classmethod
    def get_user_by_id(cls, db_session: SESSION,
                       index: int, provider: ProviderType) -> Optional['User']:
        return db_session.query(cls).filter_by(id=index, provider=provider).first()

    @classmethod
    def get_user_by_username(cls, db_session: SESSION, username: str) -> Optional['User']:
        return db_session.query(cls).filter_by(login=username).first()
