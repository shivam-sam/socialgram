from sqlalchemy import Column, Date, DateTime, Integer, String, Enum
from datetime import datetime

from .enums import Gender
from src.database import Base


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
