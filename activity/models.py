from sqlalchemy import Column, Date, DateTime, Integer, String, Enum, ForeignKey
from datetime import datetime
from sqlalchemy.orm import relationship

from src.database import Base


class Activity(Base):
    __tablename__ = "activities"

    id = Column(Integer, primary_key=True)
    username = Column(String, nullable=False)
    timestamp = Column(DateTime, nullable=False, default=datetime.utcnow())

    liked_post_id = Column(Integer)
    liked_by = Column(String)
    liked_post_image = Column(String)

    followed_username = Column(String)
    followed_user_pic = Column(String)
