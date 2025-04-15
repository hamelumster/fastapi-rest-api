from fastapi import FastAPI
from sqlalchemy import select

from db import models
from schema import (CreateAdvRequest, UpdateAdvRequest, CreateAdvResponse,
                    GetAdvResponse, SearchAdvResponse, UpdateAdvResponse,
                    DeleteAdvResponse)
from lifespan import lifespan
from dependency import SessionDependency
from crud.crud_user import get_user_by_id, add_user
from crud.crud_advertisement import get_adv_by_id, add_advertisement


app = FastAPI(
    title="Purchase and Sale Service",
    description="List of advertisements",
    lifespan=lifespan
)


@app.post("/api/v1/advertisement/",
          tags=["advertisements"],
          response_model=CreateAdvResponse)
async def create_advertisement(adv: CreateAdvRequest, session: SessionDependency):
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
async def search_advertisement(title: str = None, description: str = None,
                               price: float = None, author: str = None,
                               session: SessionDependency):
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
async def update_advertisement(adv_id: int, adv_data: UpdateAdvRequest):
    return {"message": "Hello World"}


@app.delete("/api/v1/advertisement/{adv_id}",
            tags=["advertisements"],
            response_model=DeleteAdvResponse)
async def delete_advertisement(adv_id: int):
    return {"message": "Hello World"}
