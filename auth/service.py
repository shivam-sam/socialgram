from fastapi import Depends
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError
from datetime import timedelta, datetime
from argon2 import PasswordHasher
from .models import User
from .schemas import UserCreate, UserUpdate


password_hasher = PasswordHasher()
oauth2_bearer = OAuth2PasswordBearer(tokenUrl="v1/auth/token")
SECRET_KEY = "mysecretkey"
ALGORITHM = "HS256"
TOKEN_EXPIRE_MINS = 60 * 24 * 30        # 30 days


# check for existing user
async def existing_user(db: Session, username: str, email: str):
    db_user = db.query(User).filter(User.username == username).first()
    if db_user:
        return db_user

    db_user = db.query(User).filter(User.email == email).first()
    return db_user


# create access token
async def create_access_token(username: str, id: int):
    encode = {"sub": username, "id": id}
    expires = datetime.utcnow() + timedelta(minutes=TOKEN_EXPIRE_MINS)
    encode.update({"exp": int(expires.timestamp())})
    return jwt.encode(encode, SECRET_KEY, algorithm=ALGORITHM)


# get current user from token
async def get_current_user(db: Session, token: str = Depends(oauth2_bearer)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        id: str = payload.get("id")
        expires: datetime = datetime.fromtimestamp(payload.get("exp"))
        if expires < datetime.utcnow():
            return None
        if username is None or id is None:
            return None
        return db.query(User).filter(User.id == id).first()
    except JWTError as exc:
        print(exc)
        return None


async def get_user_from_user_id(db: Session, user_id: int):
    return db.query(User).filter(User.id == user_id).first()


async def create_user(db: Session, user: UserCreate):
    db_user = User(
        email = user.email.lower().strip(),
        username = user.username.lower().strip(),
        hashed_password = password_hasher.hash(user.password),
        dob = user.dob or None,
        gender = user.gender or None,
        bio = user.bio or None,
        location = user.location or None,
        profile_pic = user.profile_pic or None,
        name = user.name or None
    )
    db.add(db_user)
    db.commit()
    return db_user


async def authenticate(db: Session, username: str, password: str):
    db_user = await existing_user(db, username, "")
    if not db_user:
        return None

    if not password_hasher.verify(db_user.hashed_password, password):
        return None
    return db_user


async def update_user(db: Session, db_user: User, user_update: UserUpdate):
    db_user.bio = user_update.bio or db_user.bio
    db_user.name = user_update.name or db_user.name
    db_user.dob = user_update.dob or db_user.dob
    db_user.gender = user_update.gender or db_user.gender
    db_user.location = user_update.location or db_user.location
    db_user.profile_pic = user_update.profile_pic or db_user.profile_pic

    db.commit()
