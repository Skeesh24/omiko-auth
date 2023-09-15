from fastapi import Depends
from fastapi_another_jwt_auth import AuthJWT

from ..classes.services import MemcachedService, SettingsService
from ..database.firebase.repository import UserFirebase
from ..classes.validation import FilterModel, UserResponse


async def get_users():
    return UserFirebase()


async def get_current_user(
    authorization: AuthJWT = Depends(), db: UserFirebase = Depends(get_users)
) -> UserResponse:
    authorization.jwt_required()

    username = authorization.get_jwt_subject()

    user = db.get(limit=1, where=FilterModel.fast("username", username))

    return UserResponse(**user)


async def get_caching_service():
    service = MemcachedService(["localhost:11211"])
    
    try:
        yield service
    finally:
        service.close()


async def get_settings():
    try:
        return SettingsService
    finally:
        pass