from datetime import timedelta
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi_jwt_auth import AuthJWT
from ..classes.crypto import verify
from ..classes.dependencies import get_users

from ..database.firebase.repository import UserFirebase

from ..classes.validation import (
    AccessToken,
    FilterModel,
    TokenResponse,
    TokenType,
    UserCreate,
    UserResponse,
)
from ..configuration import Settings


auth_router = APIRouter(prefix="/auth", tags=["auth"])


@auth_router.post("/login", response_model=TokenResponse)
async def login(
    new_user: UserCreate,
    Authorize: AuthJWT = Depends(),
    db: UserFirebase = Depends(get_users),
):
    # username checks here
    user = db.get(limit=1, where=FilterModel.fast("username", new_user.username))

    # pass checks here
    if not verify(new_user.password, user["password"]):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST)

    access_token = Authorize.create_access_token(
        subject=new_user.username,
        expires_time=timedelta(minutes=Settings().authjwt_access_token_expires),
    )
    refresh_token = Authorize.create_refresh_token(
        subject=new_user.username,
        expires_time=timedelta(minutes=Settings().authjwt_refresh_token_expires),
    )

    return TokenResponse(
        tokens=TokenType(
            access_token=access_token, refresh_token=refresh_token, token_type="Bearer"
        ),
        user=UserResponse(**user),
    )


@auth_router.post("/logout")
async def logout(Auhthorize: AuthJWT = Depends()):
    # delete token from the database
    pass


@auth_router.post("/refresh", response_model=AccessToken)
async def refresh(Auhthorize: AuthJWT = Depends()):
    Auhthorize.jwt_refresh_token_required()

    access_token = Auhthorize.create_access_token(Auhthorize.get_jwt_subject())
    return AccessToken(access_token=access_token)
