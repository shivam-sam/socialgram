import re
from sqlalchemy.orm import Session
from sqlalchemy import desc
from typing import List
from datetime import datetime

from .schemas import PostCreate, Post as PostSchema, Hashtag as HashtagSchema
from .models import Post, Hashtag, post_hashtags
from auth.models import User
from auth.schemas import User as UserSchema


async def create_hashtags_svc(db: Session, post: Post):
    regex = r"#\w+"
    matches = re.findall(regex, post.content)
    for match in matches:
        name = match[1:]
        hashtag = db.query(Hashtag).filter(Hashtag.name == name).first()
        if not hashtag:
            hashtag = Hashtag(name=name)
            db.add(hashtag)
            db.commit()
        post.hashtags.append(hashtag)


async def create_post_svc(db: Session, post: PostCreate, user_id: int):
    db_post = Post(
        content = post.content,
        image = post.image,
        location = post.location,
        author_id = user_id
    )
    db.add(db_post)
    db.commit()
    return db_post


async def get_user_posts_svc(db: Session, user_id: int) -> List[PostSchema]:
    posts = db.query(Post).filter(Post.author_id == user_id).order_by(desc(Post.created_dt)).all()
    return posts


async def get_posts_from_hashtag_svc(db: Session, hashtag_name: str):
    hashtag = db.query(Hashtag).filter_by(name=hashtag_name).first()
    if not hashtag:
        return None

    return hashtag.posts


async def get_random_posts_svc(db: Session, page: int=1, limit: int=10, hashtag: str=None):
    total_posts = db.query(Post).count()
    offset = (page - 1) * limit
    if offset >= total_posts:
        return []

    posts = db.query(Post, User.username).join(User).order_by(desc(Post.created_dt))
    if hashtag:
        posts = posts.join(post_hashtags).join(Hashtag).filter(Hashtag.name == hashtag)

    posts = posts.offset(offset).limit(limit).all()
    result = []
    for post, username in posts:
        post_dict = post.__dict__
        post_dict["username"] = username
        result.append(post_dict)

    return result


async def get_post_from_post_id_svc(db: Session, post_id: int) -> PostSchema:
    return db.query(Post).filter(Post.id == post_id).first()


async def delete_post_svc(db: Session, post_id: int):
    post = await get_post_from_post_id_svc(db, post_id)
    db.delete(post)
    db.commit()


async def like_post_svc(db: Session, post_id: int, username: str):
    post = await get_post_from_post_id_svc(db, post_id)
    if not post:
        return False, "invalid post_id"

    user = db.query(User).filter(User.username == username).first()
    if not user:
        return False, "invalid username"

    if user in post.liked_by_users:
        return False, "already_liked"

    post.liked_by_users.append(user)
    post.likes_count = len(post.liked_by_users)
    db.commit()
    return True, "done"


async def unlike_post_svc(db: Session, post_id: int, username: str):
    post = await get_post_from_post_id_svc(db, post_id)
    if not post:
        return False, "invalid post_id"

    user = db.query(User).filter(User.username == username).first()
    if not user:
        return False, "invalid username"

    if user not in post.liked_by_users:
        return False, "not_liked"

    post.liked_by_users.remove(user)
    post.likes_count = len(post.liked_by_users)
    db.commit()
    return True


async def post_liked_by_users_svc(db: Session, post_id: int) -> List[UserSchema]:
    post = await get_post_from_post_id_svc(db, post_id)
    if not post:
        return []

    liked_users = post.liked_by_users
    return liked_users
