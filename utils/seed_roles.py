from sqlalchemy import select
import asyncio
from db.dependency import get_session
from db.models import Role

ROLES = ["user", "admin"]

async def seed_roles():
    async for session in get_session():
        for name in ROLES:
            exists = await session.scalar(select(Role).where(Role.name == name))
            if not exists:
                session.add(Role(name=name))
        await session.commit()
        print(f"Roles {ROLES} created")


if __name__ == "__main__":
    asyncio.run(seed_roles())