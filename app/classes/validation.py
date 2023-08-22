from typing import Any
from pydantic import BaseModel


class UserCreate(BaseModel):
    username: str
    password: str


class UserResponse(BaseModel):
    id: str
    username: str


class FilterModel(BaseModel):
    field_path: str
    op_string: str
    value: Any

    def d(self) -> dict:
        return self.__dict__

    @staticmethod
    def fast(path: str, value):
        return FilterModel(field_path=path, op_string="==", value=value)


class TokenType(BaseModel):
    accessToken: str
    refreshToken: str
    tokenType: str


class TokenResponse(BaseModel):
    tokens: TokenType
    user: UserResponse


class AccessToken(BaseModel):
    accessToken: str
