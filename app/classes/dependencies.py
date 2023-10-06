from ast import literal_eval
from os import environ

from classes.interfaces import ICacheService
from classes.services import RabbitMQBroker, RedisBroker, RedisService, SettingsService
from classes.settings import sett
from classes.validation import UserInternal
from database.repository import UserFirebase, UserPostgres
from fastapi import Depends
from fastapi_another_jwt_auth import AuthJWT


async def get_users():
    return UserPostgres()


async def get_message_broker():
    return RabbitMQBroker(sett.BROKER_HOST)


async def get_caching_service():
    service = RedisService(sett.CACHE_HOST)

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
    user = None
    if not bool(sett.DEBUG):
        user_dict, success = cache.elem_and_status(username + "_profile")

        if not success:
            user = db.get(limit=1, offset=0, username=username)
            cache.set(
                username + "_profile",
                str({k: v for k, v in user.__dict__.items() if not "_" in k}),
            )
        else:
            user = UserInternal(**literal_eval(user_dict.decode("utf-8")))
    else:
        user = db.get(limit=1, offset=0, username=username)

    return user


async def get_settings():
    try:
        return SettingsService
    finally:
        pass
