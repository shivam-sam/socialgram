from pydantic import BaseModel
from datetime import datetime
from typing import Optional


class Hashtag(BaseModel):
    id: int
    name: str


class PostCreate(BaseModel):
    content: Optional[str] = None
    image: str
    location: Optional[str] = None


class Post(PostCreate):
    id: int
    author_id: int
    likes_count: int
    created_dt: datetime

    class Config:
        from_attributes = True
