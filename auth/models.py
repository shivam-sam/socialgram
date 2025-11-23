from sqlalchemy import Column, Date, DateTime, Integer, String, Enum
from datetime import datetime
from sqlalchemy.orm import relationship

from .enums import Gender
from src.database import Base
from post.models import post_likes


class User(Base):
    __tablename__ = "Users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True)
    username = Column(String, unique=True)
    name = Column(String)
    hashed_password = Column(String, nullable=False)
    created_dt = Column(DateTime, default=datetime.utcnow())

    dob = Column(Date)
    gender = Column(Enum(Gender))
    profile_pic = Column(String)            # Stores the link to the stored profile pic (S3, Server, Cloud)
    bio = Column(String)
    location = Column(String)

    posts = relationship("post.models.Post", back_populates="author")
    liked_posts = relationship("post.models.Post", secondary=post_likes, back_populates="liked_by_users")

