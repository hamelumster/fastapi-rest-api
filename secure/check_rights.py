from typing import Callable

from fastapi import Depends, HTTPException

from db.models import User
from secure.auth import get_current_user


def require_role(*allowed_roles: str) -> Callable:
    async def dependency(current_user: User | None = Depends(get_current_user)):
        if current_user is None:
            if not allowed_roles:
                return None
            raise HTTPException(401, detail="Authentication required")

        user_roles = [r.name for r in current_user.roles]
        if "admin" in user_roles:
            return current_user

        if any(role in user_roles for role in allowed_roles):
            return current_user

        raise HTTPException(403, detail="Not enough permissions")
    return Depends(dependency)