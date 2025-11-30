from pydantic import BaseModel
from datetime import datetime


class ActivityBase(BaseModel):
    username: str
    timestamp: datetime


class LikeActivityCreate(ActivityBase):
    liked_post_id: int
    liked_by: str


class FollowActivityCreate(ActivityBase):
    followed_username: str


class Activity(ActivityBase):
    class Config:
        from_attributes = True

