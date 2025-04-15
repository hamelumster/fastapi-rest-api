from fastapi import FastAPI, HTTPException
from sqlalchemy import select

from constants import SUCCESS_RESPONSE
from db import models
from schemas.user_schema import (CreateUserRequest, CreateUserResponse, GetUserResponse, SuccessUserResponse)
from schemas.adv_schema import (CreateAdvRequest, UpdateAdvRequest, CreateAdvResponse,
                                GetAdvResponse, SearchAdvResponse, UpdateAdvResponse, DeleteAdvResponse)
from lifespan import lifespan
from dependency import SessionDependency
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
    user_orm_obj = models.User(**user_dict)
    await add_user(session, user_orm_obj)
    return user_orm_obj.id_dict


@app.get("/api/v1/user/{user_id}", tags=["users"], response_model=GetUserResponse)
async def get_user(user_id: int, session: SessionDependency):
    user_orm_obj = await get_user_by_id(session, models.User, user_id)
    return user_orm_obj.to_dict


@app.post("/api/v1/advertisement/",
          tags=["advertisements"],
          response_model=CreateAdvResponse)
async def create_advertisement(adv: CreateAdvRequest, session: SessionDependency):
    # Проверка на существование пользователя
    user_from_db = select(models.User).where(models.User.username == adv.author)
    result = await session.execute(user_from_db)
    user = result.scalar_one_or_none()
    if user is None:
        raise HTTPException(404, detail=f"User {adv.author} not found")

    adv_dict = adv.model_dump(exclude_unset=True)
    adv_orm_obj = models.Advertisement(**adv_dict)
    await add_advertisement(session, adv_orm_obj)
    return adv_orm_obj.id_dict


@app.get("/api/v1/advertisement/{adv_id}",
         tags=["advertisements"],
         response_model=GetAdvResponse)
async def get_advertisement(adv_id: int, session: SessionDependency):
    adv_orm_obj = await get_adv_by_id(session, models.Advertisement, adv_id)
    return adv_orm_obj.to_dict


@app.get("/api/v1/advertisement/{adv_id}?{query_string}",
         tags=["advertisements"],
         response_model=SearchAdvResponse)
async def search_advertisement(session: SessionDependency,
                               title: str = None, description: str = None,
                               price: float = None, author: str = None,
                               ):

    if not title and not description and not price and not author:
        raise HTTPException(422, detail="For search you need to enter at least one parameter")

    query = (
        select(models.Advertisement)
        .where(models.Advertisement.title == title,
              models.Advertisement.description == description,
              models.Advertisement.price == price,
              models.Advertisement.author == author)
        .limit(10000)
    )
    advs = await session.scalars(query)
    return {"results": [adv.to_dict for adv in advs]}


@app.patch("/api/v1/advertisement/{adv_id}",
           tags=["advertisements"],
           response_model=UpdateAdvResponse)
async def update_advertisement(adv_id: int,
                               adv_data: UpdateAdvRequest,
                               session: SessionDependency):

    adv_orm_obj = await get_adv_by_id(session, models.Advertisement, adv_id)
    adv_dict = adv_data.model_dump(exclude_unset=True)

    if adv_dict.get("title"):
        adv_orm_obj.title = adv_dict["title"]
    if adv_dict.get("description"):
        adv_orm_obj.description = adv_dict["description"]
    if adv_dict.get("price"):
        adv_orm_obj.price = adv_dict["price"]
    await add_advertisement(session, adv_orm_obj)
    return SUCCESS_RESPONSE # adv_orm_obj.to_dict



@app.delete("/api/v1/advertisement/{adv_id}",
            tags=["advertisements"],
            response_model=DeleteAdvResponse)
async def delete_advertisement(adv_id: int, session: SessionDependency):
    adv_orm_obj = await get_adv_by_id(session, models.Advertisement, adv_id)
    await delete_adv(session, adv_orm_obj)
    return SUCCESS_RESPONSE
