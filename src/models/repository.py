from typing import List, Optional

from sqlalchemy import Column, String, Integer, CHAR, DateTime, Boolean, ForeignKey
from sqlalchemy.orm import relationship

from src.services.database import BaseModel, SESSION
from src.models.base import BasicCrud
import requests


class Repository(BaseModel, BasicCrud):
    __tablename__ = 'repository'
    id = Column(Integer, primary_key=True, autoincrement=False)
    user_id = Column(Integer, ForeignKey('user.id'))
    name = Column(String(100), nullable=False)
    private = Column(Boolean, nullable=False)
    created_at = Column(DateTime, nullable=False)
    updated_at = Column(DateTime, nullable=False)
    size = Column(Integer, nullable=False)
    stars = Column(Integer, nullable=False)
    watchers = Column(Integer, nullable=False)

    user = relationship('User', back_populates="repositories")

    @classmethod
    def get_all_from_github(cls, username: str) -> List['Repository']:
        user_request = requests.get(f'https://api.github.com/users/{username}').json()
        user_id = user_request['id']

        repo_request = requests.get(f'https://api.github.com/users/{username}/repos').json()
        repositories = []
        for repository in repo_request:
            repositories.append(Repository(id=repository['id'],
                                           user_id=user_id,
                                           name=repository['name'],
                                           private=repository['private'],
                                           created_at=repository['created_at'],
                                           updated_at=repository['updated_at'],
                                           size=repository['size'],
                                           stars=repository['stargazers_count'],
                                           watchers=repository['watchers_count']))
        return repositories

    @classmethod
    def get_all_from_local(cls, db_session: SESSION, user_id: int) -> List['Repository']:
        return db_session.query(cls).all().filter_by(user_id=user_id)

    @classmethod
    def get_one_from_github(cls, username: str, reponame: str) -> Optional['Repository']:

        repo_request = requests.get(f'https://api.github.com/users/{username}/repos').json()

        for repository in repo_request:
            if repository['name'] == reponame:
                return Repository(id=repository['id'],
                                  user_id=requests.get(f'https://api.github.com/users/{username}').json()['id'],
                                  name=repository['name'],
                                  private=repository['private'],
                                  created_at=repository['created_at'],
                                  updated_at=repository['updated_at'],
                                  size=repository['size'],
                                  stars=repository['stargazers_count'],
                                  watchers=repository['watchers_count'])

    @classmethod
    def get_by_id(cls, db_session: SESSION, index: int) -> Optional['Repository']:
        return db_session.query(cls).filter_by(id=index).first()
