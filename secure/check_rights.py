from typing import Callable

from fastapi import Depends, HTTPException

from db.models import User
from secure.auth import get_current_user


def require_role(*allowed_roles: str):
    async def dependency(current_user: User = Depends(get_current_user)):
        names = [r.name for r in current_user.roles]
        if "admin" in names:
            return current_user
        if any(role in names for role in allowed_roles):
            return current_user
        raise HTTPException(403, detail="Not enough permissions")

    return dependency