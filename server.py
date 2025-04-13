from fastapi import FastAPI
from pydantic import BaseModel

from datetime import datetime

app = FastAPI(
    title="Purchase and Sale Service",
    description="List of advertisements",
)

class CreateAdvRequest(BaseModel):
    title: str
    description: str
    price: float
    author: str
    created_at: datetime

@app.post("/api/v1/advertisement/", tags=["advertisements"])
async def create_advertisement(adv: CreateAdvRequest):
    return {"message": "Hello World"}


@app.get("/api/v1/advertisement/{adv_id}", tags=["advertisements"])
async def get_advertisement(adv: CreateAdvRequest):
    return {"message": "Hello World"}


@app.get("/api/v1/advertisement/{adv_id}?{query_string}", tags=["advertisements"])
async def search_advertisement(adv: CreateAdvRequest):
    return {"message": "Hello World"}


@app.patch("/api/v1/advertisement/{adv_id}", tags=["advertisements"])
async def update_advertisement(adv: CreateAdvRequest):
    return {"message": "Hello World"}


@app.delete("/api/v1/advertisement/{adv_id}", tags=["advertisements"])
async def delete_advertisement(adv: CreateAdvRequest):
    return {"message": "Hello World"}
