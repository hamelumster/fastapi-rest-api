from fastapi import HTTPException
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from models import (User, ORM_OBJ_USR, ORM_OBJ_USR_CLS,
                    Advertisement, ORM_OBJ_ADV, ORM_OBJ_ADV_CLS)


async def add_user(session: AsyncSession, user: ORM_OBJ_USR_CLS):
    session.add(user)
    try:
        await session.commit()
    except IntegrityError:
        HTTPException(409, detail="User already exists")


