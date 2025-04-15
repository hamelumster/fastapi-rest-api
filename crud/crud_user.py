from fastapi import HTTPException
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from db.models import ORM_OBJ_USR_CLS, ORM_OBJ_USR


async def add_user(session: AsyncSession, user: ORM_OBJ_USR):
    session.add(user)
    try:
        await session.commit()
    except IntegrityError:
        HTTPException(409, detail="User already exists")

async def get_user_by_id(session: AsyncSession, user_orm_cls: ORM_OBJ_USR_CLS, user_id: int):
    user_orm_obj = await session.get(user_orm_cls, user_id)
    if user_orm_obj is None:
        raise HTTPException(404, detail="User not found")
    return user_orm_obj
