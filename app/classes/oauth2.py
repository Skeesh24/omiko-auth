from datetime import datetime
from datetime import timedelta
from typing import Optional
from fastapi import Depends, status, HTTPException
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError
from passlib.context import CryptContext
from jose.jwt import encode, decode

from config import config
from app.classes.validation import TokenData, FilterModel, UserResponse
from app.classes.dependencies import get_users
from app.classes.repository import UserFirebase


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")


def get_hashed(password: str) -> str:
    return CryptContext(schemes=["bcrypt"]).hash(password)


def verify(secret, password: str) -> bool:
    return CryptContext(schemes=["bcrypt"]).verify(secret, password)


def create_access_token(data: dict) -> str:
    to_encode = data.copy()
    expire = datetime.now() + timedelta(minutes=config.JWT_TOKEN_EXPIRATION_MINUTES)
    to_encode.update({"exp": expire})

    jwt = encode(to_encode, config.JWT_SECRET_KEY, config.JWT_ALGORYTHM)

    return jwt


def verify_access_token(access_token: str, credentials_execption):
    try:
        payload = decode(
            access_token, config.JWT_SECRET_KEY, algorithms=config.JWT_ALGORYTHM
        )

        email: Optional[str] = payload.get("email")

        if not email:
            raise credentials_execption

        data = TokenData(email=email, created_at=datetime.now())

        return data
    except JWTError:
        raise credentials_execption


def get_current_user(token: str = Depends(oauth2_scheme), db: UserFirebase = Depends(get_users)) -> UserResponse:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could't validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    data = verify_access_token(token, credentials_execption=credentials_exception)

    user = db.get(limit=1, where=FilterModel.fast("email", data.email))

    return UserResponse(**user)
