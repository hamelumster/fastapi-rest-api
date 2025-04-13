from fastapi import FastAPI
from schema import CreateAdvRequest, UpdateAdvRequest

app = FastAPI(
    title="Purchase and Sale Service",
    description="List of advertisements",
)


@app.post("/api/v1/advertisement/", tags=["advertisements"])
async def create_advertisement(adv: CreateAdvRequest):
    return {"message": "Hello World"}


@app.get("/api/v1/advertisement/{adv_id}", tags=["advertisements"])
async def get_advertisement(adv_id: int):
    return {"message": "Hello World"}


@app.get("/api/v1/advertisement/{adv_id}?{query_string}", tags=["advertisements"])
async def search_advertisement(title: str = None, description: str = None,
                               price: float = None, author: str = None):
    return {"message": "Hello World"}


@app.patch("/api/v1/advertisement/{adv_id}", tags=["advertisements"])
async def update_advertisement(adv_id: int, adv_data: UpdateAdvRequest):
    return {"message": "Hello World"}


@app.delete("/api/v1/advertisement/{adv_id}", tags=["advertisements"])
async def delete_advertisement(adv_id: int):
    return {"message": "Hello World"}
