from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from db.models import ORM_OBJ_ADV_CLS


async def add_advertisement(session: AsyncSession, adv: ORM_OBJ_ADV_CLS):
    session.add(adv)
    await session.commit()


async def get_adv_by_id(session: AsyncSession, adv_orm_cls: ORM_OBJ_ADV_CLS, adv_id: int):
    adv_orm_obj = await session.get(adv_orm_cls, adv_id)
    if adv_orm_obj is None:
        raise HTTPException(404, detail="Advertisement not found")
    return adv_orm_obj

async def delete_adv(session: AsyncSession, adv: ORM_OBJ_ADV_CLS):
    await session.delete(adv)
    await session.commit()

