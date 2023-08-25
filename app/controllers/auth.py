from datetime import timedelta
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from fastapi_another_jwt_auth import AuthJWT
from jwt import decode

from ..classes.interfaces import ICacheService
from ..classes.crypto import verify
from ..classes.dependencies import get_caching_service, get_users, get_settings

from app.database.firebase.repository import UserFirebase

from app.classes.validation import (
    AccessToken,
    FilterModel,
    TokenResponse,
    TokenType,
    UserResponse,
)


auth_router = APIRouter(
    prefix="/auth",
    tags=["auth"],
    dependencies=[Depends(get_caching_service), Depends(get_settings)],
)


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/token")


@auth_router.post("/login", response_model=TokenResponse)
async def login(
    credentials: OAuth2PasswordRequestForm = Depends(),
    Authorize: AuthJWT = Depends(),
    db: UserFirebase = Depends(get_users),
    cache: ICacheService = Depends(get_caching_service),
    settings=Depends(get_settings),
):
    # username checks here
    user, success = cache.elem_and_status(credentials.username)
    print(user, success)
    if not success:
        user = db.get(limit=1, where=FilterModel.fast("username", credentials.username))

    # pass checks here
    if not verify(credentials.password, user["password"]):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST)

    access_token = Authorize.create_access_token(
        subject=credentials.username,
        expires_time=timedelta(minutes=settings.authjwt_access_token_expires),
    )
    refresh_token = Authorize.create_refresh_token(
        subject=credentials.username,
        expires_time=timedelta(days=settings.authjwt_refresh_token_expires),
    )

    # caching is here
    if not success:
        cache.set(credentials.username + "_profile", user)
    cache.set(credentials.username + "_token", refresh_token)

    return TokenResponse(
        tokens=TokenType(
            accessToken=access_token,
            refreshToken=refresh_token,
            tokenType="Bearer",
        ),
        user=UserResponse(**user),
    )


@auth_router.post("/logout")
async def logout(
    Auhthorize: AuthJWT = Depends(), cache: ICacheService = Depends(get_caching_service)
):
    Auhthorize.jwt_refresh_token_required()

    # delete token from the database
    username = Auhthorize.get_jwt_subject()
    if not cache.remove(username + "_token"):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="error deleting token"
        )


@auth_router.post("/refresh", response_model=AccessToken)
async def refresh(
    Authorize: AuthJWT = Depends(),
    cache: ICacheService = Depends(get_caching_service),
    settings=Depends(get_settings),
):
    Authorize.jwt_refresh_token_required()

    # compare with the token in the database
    username = Authorize.get_jwt_subject()
    token, success = cache.elem_and_status(username + "_token")

    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="token not found"
        )

    received_token = Authorize.get_raw_jwt()
    if decode(token, settings.authjwt_secret_key, ["HS256"]) != received_token:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="received invalid token"
        )

    access_token = Authorize.create_access_token(username)
    return AccessToken(accessToken=access_token)
