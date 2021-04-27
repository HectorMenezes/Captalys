from typing import Literal, List
from datetime import datetime
from pydantic import BaseModel, Field, PositiveInt, AnyHttpUrl


class Repository(BaseModel):
    id: int = Field(...)
    user_id: int = Field(...)
    name: str = Field(...)
    private: bool = Field(...)
    created_at: datetime = Field(...)
    updated_at: datetime = Field(...)
    size: int = Field(...)
    stars: int = Field(...)
    watchers: int = Field(...)

    class Config:
        orm_mode = True


class User(BaseModel):
    id: int = Field(...)
    login: str = Field(...)
    twitter_username: str = Field()
    email: str = Field()
    repositories: str = Field()

    class Config:
        orm_mode = True


class UserOutput(BaseModel):
    id: int = Field(...)
    login: str = Field(...)
    twitter_username: str = Field()
    email: str = Field()
    repositories: str = Field()
