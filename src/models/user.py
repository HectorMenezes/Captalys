from typing import List, Optional

from sqlalchemy import Column, String, Integer, CHAR

from src.services.database import BaseModel, SESSION


class User(BaseModel):
    __tablename__ = 'user'
    index = Column(Integer, primary_key=True, autoincrement=False)
    login = Column(String(100), nullable=False)
    email = Column(String(100), nullable=True)
    email = Column(String(100), nullable=True)
    repositories = Column(String(13), nullable=False)
