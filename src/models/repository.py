from typing import List, Optional

from sqlalchemy import Column, String, Integer, CHAR, DateTime, Boolean, ForeignKey
from sqlalchemy.orm import relationship

from src.services.database import BaseModel, SESSION


class Repository(BaseModel):
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

    creator = relationship('User', back_populates="repositories")

