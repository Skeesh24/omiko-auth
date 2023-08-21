from datetime import datetime
from typing import Any
from pydantic import BaseModel


class TokenData(BaseModel):
    username: str
    created_at: datetime


class Token(BaseModel):
    access_token: str
    token_type: str


class FilterModel(BaseModel):
    field_path: str
    op_string: str
    value: Any

    def d(self) -> dict:
        return self.__dict__
    
    @staticmethod
    def fast(path: str, value):
        return FilterModel(field_path=path, op_string="==", value=value)
    

class UserCreate(BaseModel):
    username: str
    password: str


class UserBase(BaseModel):
    username: str


class UserResponse(BaseModel):
    id: str
    username: str


class TokenResponse(BaseModel):
    token: Token
    user: UserResponse