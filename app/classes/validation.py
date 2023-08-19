from datetime import datetime
from typing import Any
from pydantic import BaseModel


class TokenData(BaseModel):
    email: str
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
    email: str
    password: str


class UserBase(BaseModel):
    email: str


class UserResponse(BaseModel):
    id: str
    email: str