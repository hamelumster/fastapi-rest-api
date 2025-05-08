from sqlalchemy.ext.asyncio import AsyncSession

from db.models import ORM_OBJ


async def add_token(session: AsyncSession, adv: ORM_OBJ):
    session.add(adv)
    await session.commit()
