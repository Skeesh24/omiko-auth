from json import loads
from os import environ

from classes.interfaces import ICacheService
from classes.services import RedisService, SettingsService
from classes.validation import UserResponse
from database.repository import UserFirebase, UserPostgres
from fastapi import Depends
from fastapi_another_jwt_auth import AuthJWT


async def get_users():
    return UserPostgres()


async def get_caching_service():
    service = RedisService(environ.get("REDIS_EXTERNAL"))

    try:
        yield service
    finally:
        service.close()


async def get_current_user(
    authorization: AuthJWT = Depends(),
    db: UserFirebase = Depends(get_users),
    cache: ICacheService = Depends(get_caching_service),
) -> UserPostgres:
    authorization.jwt_required()

    username = authorization.get_jwt_subject()

    if not bool(environ.get("DEBUG")):
        user, success = cache.elem_and_status(username + "_profile")
        user = loads(user.replace('"', "*").replace("'", '"').replace("*", "'"))

        if not success:
            user = db.get(limit=1, offset=0, username=username)
            cache.set(username + "_profile", str(user))
    else:
        user = db.get(limit=1, offset=0, username=username)

    return user


async def get_settings():
    try:
        return SettingsService
    finally:
        pass
