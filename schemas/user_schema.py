import uuid

from pydantic import BaseModel
from datetime import datetime
from typing import Literal


class CreateUserRequest(BaseModel):
    username: str
    password: str


class UpdateUserRequest(BaseModel):
    username: str | None = None
    password: str | None = None


class CreateUserResponse(BaseModel):
    id: int


class GetUserResponse(BaseModel):
    id: int
    username: str


class SuccessUserResponse(BaseModel):
    status: Literal["success"]


class LoginRequest(CreateUserRequest):
    pass


class LoginResponse(BaseModel):
    token: uuid.UUID
