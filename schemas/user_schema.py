import uuid

from pydantic import BaseModel
from datetime import datetime
from typing import Literal


class CreateUserRequest(BaseModel):
    username: str
    password: str


class CreateUserResponse(BaseModel):
    id: int


class GetUserResponse(BaseModel):
    id: int
    username: str


class SuccessUserResponse(BaseModel):
    status: Literal["success"]


class LoginResponse(BaseModel):
    token: uuid.UUID
