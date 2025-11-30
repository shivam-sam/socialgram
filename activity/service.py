from sqlalchemy.orm import Session
from sqlalchemy import desc
from typing import List
from .models import Activity



async def get_activities_by_username(db: Session, username: str, page: int = 1, limit: int = 10) -> List[Activity]:
    offset = (page - 1) * limit
    return (
        db.query(Activity)
        .filter(Activity.username == username)
        .order_by(desc(Activity.timestamp))
        .offset(offset)
        .limit(limit)
        .all()
    )
