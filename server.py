from fastapi import FastAPI, HTTPException
from sqlalchemy import select

from constants import SUCCESS_RESPONSE
from db.models import User, Advertisement
from schemas.user_schema import (CreateUserRequest, CreateUserResponse, GetUserResponse)
from schemas.adv_schema import (CreateAdvRequest, UpdateAdvRequest, CreateAdvResponse,
                                GetAdvResponse, SearchAdvResponse, UpdateAdvResponse, DeleteAdvResponse)
from db.lifespan import lifespan
from db.dependency import SessionDependency
from crud.crud_user import get_user_by_id, add_user
from crud.crud_advertisement import get_adv_by_id, add_advertisement, delete_adv


app = FastAPI(
    title="Purchase and Sale Service",
    description="List of advertisements",
    lifespan=lifespan
)


@app.post("/api/v1/user/", tags=["users"], response_model=CreateUserResponse)
async def create_user(user: CreateUserRequest, session: SessionDependency):
    user_dict = user.model_dump(exclude_unset=True)
    user_orm_obj = User(**user_dict)
    await add_user(session, user_orm_obj)
    return user_orm_obj.id_dict


@app.get("/api/v1/user/{user_id}", tags=["users"], response_model=GetUserResponse)
async def get_user(user_id: int, session: SessionDependency):
    user_orm_obj = await get_user_by_id(session, User, user_id)
    return user_orm_obj.to_dict


@app.post("/api/v1/advertisement/",
          tags=["advertisements"],
          response_model=CreateAdvResponse)
async def create_advertisement(user_id: int, adv: CreateAdvRequest, session: SessionDependency):
    user = await get_user_by_id(session, User, user_id)

    adv_dict = adv.model_dump(exclude_unset=True)
    adv_dict["author_id"] = user.id
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
                               user_id: int,
                               adv_data: UpdateAdvRequest,
                               session: SessionDependency):
    # Проверка на сущестование пользователя
    user = await get_user_by_id(session, User, user_id)
    adv_orm_obj = await get_adv_by_id(session, Advertisement, adv_id)

    if adv_orm_obj.author_id != user.id:
        raise HTTPException(404, detail=f"User is not author of advertisement!")

    adv_dict = adv_data.model_dump(exclude_unset=True)

    if adv_dict.get("title"):
        adv_orm_obj.title = adv_dict["title"]
    if adv_dict.get("description"):
        adv_orm_obj.description = adv_dict["description"]
    if adv_dict.get("price"):
        adv_orm_obj.price = adv_dict["price"]
    await add_advertisement(session, adv_orm_obj)
    return SUCCESS_RESPONSE


@app.delete("/api/v1/advertisement/{adv_id}",
            tags=["advertisements"],
            response_model=DeleteAdvResponse)
async def delete_advertisement(adv_id: int, session: SessionDependency):
    adv_orm_obj = await get_adv_by_id(session, Advertisement, adv_id)
    await delete_adv(session, adv_orm_obj)
    return SUCCESS_RESPONSE
