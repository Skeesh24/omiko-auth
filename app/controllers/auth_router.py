from fastapi import APIRouter, Depends, HTTPException
from fastapi import status
from fastapi.security import OAuth2PasswordRequestForm

from app.classes.repository import UserFirebase
from app.classes.dependencies import get_users
from app.classes.oauth2 import create_access_token, verify
from app.classes.validation import TokenResponse, Token, FilterModel



auth_router = APIRouter(prefix="/auth", tags=["auth"])


@auth_router.post("/login", status_code=status.HTTP_201_CREATED, response_model=TokenResponse)
async def login(credentials: OAuth2PasswordRequestForm = Depends(), db: UserFirebase = Depends(get_users)):
    user = db.get(limit=1, where=FilterModel.fast("email", credentials.username))

    if not verify(credentials.password, user["password"]):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST)

    access_token = create_access_token({"email": user["email"]})

    return TokenResponse(
            token=Token(access_token=access_token, token_type="Bearer"),
            user=user
        )