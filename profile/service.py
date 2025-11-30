from sqlalchemy.orm import Session
from typing import List
from auth.models import User, Follow
from activity.models import Activity
from .schemas import FollowersList, FollowingList
from auth.service import get_user_from_user_id, existing_user


async def follow_svc(db: Session, follower: str, following: str):
    db_follower = await existing_user(db, follower, "")
    db_following = await existing_user(db, following, "")
    if not db_follower or not db_following:
        return False

    db_follow = db.query(Follow).filter_by(follower_id = db_follower.id,
                                           following_id = db_following.id).first()
    if db_follow:
        return False

    db_follow = Follow(follower_id=db_follower.id, following_id = db_following.id)
    db.add(db_follow)

    db_follower.following_count += 1
    db_following.followers_count += 1

    follow_activity = Activity(
        username=following,
        followed_username=db_follower.username,
        followed_user_pic=db_follower.profile_pic,
    )
    db.add(follow_activity)
    db.commit()
    return True


async def unfollow_svc(db: Session, unfollower: str, unfollowing: str, db_follower=None):
    db_unfollower = await existing_user(db, unfollower, "")
    db_unfollowing = await existing_user(db, unfollowing, "")
    if not db_unfollower or not db_unfollowing:
        return False

    db_follow = db.query(Follow).filter_by(follower_id = db_unfollower.id,
                                           following_id = db_unfollowing.id).first()
    if not db_follow:
        return False

    db.delete(db_follow)

    db_unfollower.following_count -= 1
    db_unfollowing.followers_count -= 1
    db.commit()
    return True


async def get_followers_svc(db: Session, user_id: int) -> List[FollowersList]:
    db_user = await get_user_from_user_id(db, user_id)
    if not db_user:
        return False

    db_followers = db.query(Follow).filter_by(following_id=user_id).join(User, User.id == Follow.follower_id)
    return db_followers


async def get_following_svc(db: Session, user_id: int) -> List[FollowingList]:
    db_user = await get_user_from_user_id(db, user_id)
    if not db_user:
        return []

    db_followings = (
        db.query(Follow)
        .filter_by(follower_id=user_id)
        .join(User, User.id == Follow.following_id)
    )
    return db_followings


async def check_follow_svc(db: Session, current_user: str, user: str):
    db_follower = await existing_user(db, current_user, "")
    db_following = await existing_user(db, user, "")
    if not db_follower or not db_following:
        return False
    db_following = db.query(Follow).filter_by(follower_id = db_follower.id,
                                              following_id = db_following.id).first()
    if not db_following:
        return False

    return True
