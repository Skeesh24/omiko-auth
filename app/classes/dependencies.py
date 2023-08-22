from fastapi import Depends
from fastapi_jwt_auth import AuthJWT

from ..database.firebase.repository import UserFirebase
from .validation import FilterModel, UserResponse


def get_users():
    return UserFirebase()


def get_current_user(
    authorization: AuthJWT = Depends(), db: UserFirebase = Depends(get_users)
) -> UserResponse:
    authorization.jwt_required()

    username = authorization.get_jwt_subject()

    user = db.get(limit=1, where=FilterModel.fast("username", username))

    return UserResponse(**user)
