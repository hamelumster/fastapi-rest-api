from pydantic import BaseModel
from datetime import datetime
from typing import Literal


class CreateUserRequest(BaseModel):
    username: str
    password: str
    created_at: datetime


class CreateUserResponse(BaseModel):
    id: int


class GetUserResponse(BaseModel):
    id: int
    username: str
    created_at: datetime


class SuccessUserResponse(BaseModel):
    status: Literal["success"]