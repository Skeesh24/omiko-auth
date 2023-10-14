from typing import Any

from pydantic import BaseModel
from settings import sett


class UserCreate(BaseModel):
    username: str
    password: str


class UserResponse(BaseModel):
    id: str
    username: str


class UserInternal(BaseModel):
    id: str
    username: str
    password: str


class FilterModel(BaseModel):
    field_path: str
    op_string: str
    value: Any

    def d(self) -> dict:
        return self.__dict__

    @staticmethod
    def fast(path: str, value):
        return FilterModel(
            field_path=path, op_string=sett.FIREBASE_EQUAL_SIGN, value=value
        )


class TokenType(BaseModel):
    accessToken: str
    refreshToken: str
    tokenType: str


class TokenResponse(BaseModel):
    tokens: TokenType
    user: UserResponse


class AccessToken(BaseModel):
    accessToken: str


class RefreshToken(BaseModel):
    refreshToken: str


class BrokerMessage:
    to: str
    subject: str
    msg: str

    @classmethod
    def default(cls, to: str, subject: str, msg: str):
        return dict(cls(to, subject, msg))
