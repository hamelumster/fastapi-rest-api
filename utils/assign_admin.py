from db.dependency import SessionDependency
import asyncio
from db.models import User, Role, Session
from db.dependency import SessionDependency
from fastapi import HTTPException
from sqlalchemy import select
import sys


async def assign_admin(user_id: int, session):
    user = await session.get(User, user_id)
    if not user:
        raise HTTPException(404, detail="User not found")

    role = await session.scalar(select(Role).where(Role.name == "admin"))

    if not role:
        raise HTTPException(500, detail="Admin role not found")

    if role not in user.roles:
        user.roles.append(role)
        await session.commit()
        print(f"User {user_id} is now admin")
    else:
        print(f"User {user_id} is already admin")


async def start_roles():
    user_id = int(sys.argv[1])
    async with Session() as session:
        await assign_admin(user_id, session)


if __name__ == "__main__":
    asyncio.run(start_roles())
