from pydantic import BaseModel
from datetime import datetime
from typing import Literal


class CreateAdvRequest(BaseModel):
    title: str
    description: str
    price: float


class UpdateAdvRequest(BaseModel):
    title: str | None = None
    description: str | None = None
    price: float | None = None


class CreateAdvResponse(BaseModel):
    id: int


class GetAdvResponse(BaseModel):
    id: int
    title: str
    description: str
    price: float
    author: str
    created_at: datetime


class SearchAdvResponse(BaseModel):
    results: list[GetAdvResponse]


class SuccessAdvResponse(BaseModel):
    status: Literal["success"]


class UpdateAdvResponse(SuccessAdvResponse):
    pass


class DeleteAdvResponse(SuccessAdvResponse):
    pass
