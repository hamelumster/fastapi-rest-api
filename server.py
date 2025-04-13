from fastapi import FastAPI

app = FastAPI(
    title="Purchase and Sale Service",
    description="List of advertisements",
)

@app.post("/api/v1/advertisement/")
async def create_advertisement():
    return {"message": "Hello World"}