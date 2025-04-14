from fastapi import FastAPI
from schema import (CreateAdvRequest, UpdateAdvRequest, CreateAdvResponse,
                    GetAdvResponse, SearchAdvResponse, UpdateAdvResponse,
                    DeleteAdvResponse)
from lifespan import lifespan

app = FastAPI(
    title="Purchase and Sale Service",
    description="List of advertisements",
    lifespan=lifespan
)


@app.post("/api/v1/advertisement/",
          tags=["advertisements"],
          response_model=CreateAdvResponse)
async def create_advertisement(adv: CreateAdvRequest):
    return {"message": "Hello World"}


@app.get("/api/v1/advertisement/{adv_id}",
         tags=["advertisements"],
         response_model=GetAdvResponse)
async def get_advertisement(adv_id: int):
    return {"message": "Hello World"}


@app.get("/api/v1/advertisement/{adv_id}?{query_string}",
         tags=["advertisements"],
         response_model=SearchAdvResponse)
async def search_advertisement(title: str = None, description: str = None,
                               price: float = None, author: str = None):
    return {"message": "Hello World"}


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
