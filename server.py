from typing import Annotated

from fastapi import FastAPI, HTTPException, Depends
from sqlalchemy import select

from secure.auth import hash_password, check_password, get_current_user
from constants import SUCCESS_RESPONSE
from crud.crud_token import add_token
from db.models import User, Advertisement, Token
from schemas.user_schema import (CreateUserRequest, CreateUserResponse, GetUserResponse,
                                 LoginResponse, LoginRequest, UpdateUserRequest, DeleteUserResponse)
from schemas.adv_schema import (CreateAdvRequest, UpdateAdvRequest, CreateAdvResponse,
                                GetAdvResponse, SearchAdvResponse, UpdateAdvResponse, DeleteAdvResponse)
from db.lifespan import lifespan
from db.dependency import SessionDependency
from crud.crud_user import get_user_by_id, add_user, delete_user
from crud.crud_advertisement import get_adv_by_id, add_advertisement, delete_adv
from secure.check_rights import require_role

app = FastAPI(
    title="Purchase and Sale Service",
    description="List of advertisements",
    lifespan=lifespan
)

required_role_user = require_role("user")
USER_ROLE = Annotated[User, Depends(required_role_user)]

required_role_admin = require_role("admin")
ADMIN_ROLE = Annotated[User, Depends(required_role_admin)]

@app.post("/api/v1/login", tags=["login"], response_model=LoginResponse)
async def login(login_data: LoginRequest, session: SessionDependency):
    stmt = select(User).where(User.username == login_data.username)
    user = await session.scalar(stmt)
    if not user or not check_password(login_data.password, user.password):
        raise HTTPException(401, "Incorrect username or password")
    token = Token(user_id=user.id)
    await add_token(session, token)
    return token.to_dict


@app.post("/api/v1/user/",
          tags=["users"],
          response_model=CreateUserResponse)
async def create_user(user: CreateUserRequest, session: SessionDependency):
    user_dict = user.model_dump(exclude_unset=True)
    user_dict["password"] = hash_password(user_dict["password"])
    user_orm_obj = User(**user_dict)
    await add_user(session, user_orm_obj)
    return user_orm_obj.id_dict


@app.get("/api/v1/user/{user_id}",
         tags=["users"],
         response_model=GetUserResponse)
async def get_user(user_id: int, session: SessionDependency):
    user_orm_obj = await get_user_by_id(session, User, user_id)
    return user_orm_obj.to_dict


@app.patch("/api/v1/user/{user_id}",
           tags=["users"],
           response_model=GetUserResponse)
async def patch_user(
        user_id: int,
        user_in: UpdateUserRequest,
        session: SessionDependency,
        current_user: USER_ROLE
):
    r_names = [r.name for r in current_user.roles]

    if user_id != current_user.id:
        if "admin" not in r_names:
            raise HTTPException(403, detail="Forbidden")

    user_obj = await get_user_by_id(session, User, user_id)

    data = user_in.model_dump(exclude_unset=True)
    if data.get("password"):
        data["password"] = hash_password(data["password"])

    for field, value in data.items():
        setattr(user_obj, field, value)

    await session.commit()
    await session.refresh(user_obj)
    return user_obj.to_dict


@app.delete("/api/v1/user/{user_id}",
            tags=["users"],
            response_model=DeleteUserResponse)
async def delete_user(
        user_id: int,
        session: SessionDependency,
        current_user: USER_ROLE
):
    if user_id != current_user.id:
        raise HTTPException(403, detail="Forbidden")

    await delete_user(session, user_id)
    return SUCCESS_RESPONSE


@app.post("/api/v1/advertisement/",
          tags=["advertisements"],
          response_model=CreateAdvResponse)
async def create_advertisement(adv: CreateAdvRequest,
                               session: SessionDependency,
                               current_user: USER_ROLE):
    adv_dict = adv.model_dump(exclude_unset=True)
    adv_dict["author_id"] = current_user.id
    adv_orm_obj = Advertisement(**adv_dict)
    await add_advertisement(session, adv_orm_obj)
    return adv_orm_obj.to_dict


@app.get("/api/v1/advertisement/{adv_id}",
         tags=["advertisements"],
         response_model=GetAdvResponse)
async def get_advertisement(adv_id: int, session: SessionDependency):
    adv_orm_obj = await get_adv_by_id(session, Advertisement, adv_id)
    return adv_orm_obj.to_dict


@app.get("/api/v1/advertisement",
         tags=["advertisements"],
         response_model=SearchAdvResponse)
async def search_advertisement(session: SessionDependency,
                               title: str = None, description: str = None,
                               price: float = None, author: str = None):
    # Если не введен ни один из параметров, то вернем пустой список
    if not (title or description or price or author):
        return {"results": []}

    query = select(Advertisement)

    if title:
        query = query.where(Advertisement.title == title)
    if description:
        query = query.where(Advertisement.description == description)
    if price:
        query = query.where(Advertisement.price == price)
    if author:
        query = query.join(Advertisement.user).where(User.username == author)

    query = query.limit(10000)
    advs = await session.scalars(query)
    return {"results": [adv.to_dict for adv in advs]}


@app.patch("/api/v1/advertisement/{adv_id}",
           tags=["advertisements"],
           response_model=UpdateAdvResponse)
async def update_advertisement(adv_id: int,
                               adv_data: UpdateAdvRequest,
                               session: SessionDependency,
                               current_user: USER_ROLE):
    adv = await get_adv_by_id(session, Advertisement, adv_id)

    if adv.author_id != current_user.id:
        raise HTTPException(status_code=403, detail="Forbidden")

    adv_dict = adv_data.model_dump(exclude_unset=True)

    if adv_dict.get("title"):
        adv.title = adv_dict["title"]
    if adv_dict.get("description"):
        adv.description = adv_dict["description"]
    if adv_dict.get("price"):
        adv.price = adv_dict["price"]

    await session.commit()
    await session.refresh(adv)

    return SUCCESS_RESPONSE


@app.delete("/api/v1/advertisement/{adv_id}",
            tags=["advertisements"],
            response_model=DeleteAdvResponse)
async def delete_advertisement(adv_id: int,
                               session: SessionDependency,
                               current_user: USER_ROLE):
    adv_orm_obj = await get_adv_by_id(session, Advertisement, adv_id)
    if adv_orm_obj.author_id != current_user.id:
        raise HTTPException(403, detail="Forbidden")
    await delete_adv(session, adv_orm_obj)
    return SUCCESS_RESPONSE
