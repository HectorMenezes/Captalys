from typing import List, Optional

from sqlalchemy import Column, String, Integer, CHAR, ForeignKey, Boolean, DateTime
from sqlalchemy.orm import relationship

from src.services.database import BaseModel, SESSION

from src.models.base import BasicCrud
import requests


class User(BaseModel, BasicCrud):
    __tablename__ = 'user'
    id = Column(Integer, primary_key=True, autoincrement=False)
    login = Column(String(100), nullable=False)
    email = Column(String(100), nullable=True)
    twitter_username = Column(String(100), nullable=True)
    repositories = relationship('Repository', back_populates="user")

    @classmethod
    def create_from_git(cls, username: str) -> Optional['User']:
        user_request = requests.get(f'https://api.github.com/users/{username}').json()
        return User(id=user_request['id'],
                    login=user_request['login'],
                    twitter_username=user_request['twitter_username'],
                    email=user_request['email'])

    # WHY DON'T THIS WORK???????????????????

    @classmethod
    def exists(cls, db_session: SESSION, index: int) -> 'bool':
        return db_session.query(cls).filter_by(id=index).first() is not None
