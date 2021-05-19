from typing import List, Optional

from sqlalchemy import Column, String, Integer, \
    DateTime, Boolean, ForeignKey
from sqlalchemy.orm import relationship

from src.models.base import BasicCrud
from src.services.database import BaseModel, SESSION


class Repository(BaseModel, BasicCrud):
    __tablename__ = 'repository'
    id = Column(Integer, primary_key=True, autoincrement=False)
    user_id = Column(Integer, ForeignKey('user.id'))
    name = Column(String(100), nullable=False)
    private = Column(Boolean, nullable=False)
    created_at = Column(DateTime, nullable=False)
    updated_at = Column(DateTime, nullable=False)
    size = Column(Integer, nullable=True)
    stars = Column(Integer, nullable=False)
    watchers = Column(Integer, nullable=True)

    user = relationship('User', back_populates="repositories")

    @classmethod
    def get_all_from_local(cls, db_session: SESSION, user_id: int) -> List['Repository']:
        return db_session.query(cls).filter_by(user_id=user_id).all()

    @classmethod
    def get_by_id(cls, db_session: SESSION, index: int) -> Optional['Repository']:
        return db_session.query(cls).filter_by(id=index).first()
