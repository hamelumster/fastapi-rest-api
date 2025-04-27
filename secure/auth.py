import bcrypt
from fastapi import Header, HTTPException, Depends
from sqlalchemy import select

from db.dependency import SessionDependency
from db.models import User, Token


def hash_password(password: str) -> str:
    password = password.encode()
    password_hashed = bcrypt.hashpw(password, bcrypt.gensalt())
    return password_hashed.decode()


def check_password(password: str, password_hashed: str) -> bool:
    password = password.encode()
    password_hashed = password_hashed.encode()
    return bcrypt.checkpw(password, password_hashed)


async def get_current_user(
        authorization: str | None = Header(None),
        session: SessionDependency = Depends(),
) -> User | None:
    if not authorization:
        return None

    try:
        scheme, token = authorization.split()
        if scheme.lower() != "bearer":
            raise ValueError
    except ValueError:
        raise HTTPException(401, detail="Invalid auth scheme")

    stmt = select(Token).where(Token.token == token)
    token_obj = (await session.scalar(stmt)).scalar_one_or_none()
    if not token_obj:
        raise HTTPException(401, detail="Invalid token")
    return token_obj.user