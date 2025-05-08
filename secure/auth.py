import bcrypt
from fastapi import Header, HTTPException, Depends
from sqlalchemy import select

from db.dependency import SessionDependency, TokenDependency
from db.models import User, Token


def hash_password(password: str) -> str:
    password = password.encode()
    password_hashed = bcrypt.hashpw(password, bcrypt.gensalt())
    return password_hashed.decode()


def check_password(password: str, password_hashed: str) -> bool:
    password = password.encode()
    password_hashed = password_hashed.encode()
    return bcrypt.checkpw(password, password_hashed)


async def get_current_user(token: TokenDependency) -> User:
    return token.user