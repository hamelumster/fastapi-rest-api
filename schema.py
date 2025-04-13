from pydantic import BaseModel
from datetime import datetime


class CreateAdvRequest(BaseModel):
    title: str
    description: str
    price: float
    author: str
    created_at: datetime


class UpdateAdvRequest(BaseModel):
    title: str | None = None
    description: str | None = None
    price: float | None = None
