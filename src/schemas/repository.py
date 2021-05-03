from datetime import datetime

from pydantic import BaseModel, Field


class Repository(BaseModel):
    id: int = Field(...)
    name: str = Field(...)
    private: bool = Field(False)
    created_at: datetime = Field(...)
    updated_at: datetime = Field(...)
    size: int = Field(0)
    stars: int = Field(...)
    watchers: int = Field(0)
