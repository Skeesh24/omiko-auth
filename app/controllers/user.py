from typing import List, Union

from classes.crypto import get_hashed
from classes.dependencies import get_current_user, get_users
from classes.interfaces import IRepository
from classes.validation import UserCreate, UserResponse
from database.postgres.entities import PostgresUser
from fastapi import APIRouter, Depends, status
from fastapi_another_jwt_auth import AuthJWT

user_router = APIRouter(prefix="/user", tags=["user"])


@user_router.get("", response_model=Union[List[UserResponse], UserResponse])
async def get_all_users(
    limit: int = 5, offset: int = 0, db: IRepository = Depends(get_users)
):
    users: list[PostgresUser] = db.get(
        limit=limit,
        offset=offset,
    )

    return [user.__dict__ for user in users]


@user_router.get("/{email}", response_model=UserResponse)
async def get_user_by_email(email: str, db: IRepository = Depends(get_users)):
    user = db.get(limit=1, offset=0, username=email)
    return user.__dict__


@user_router.post(
    "",
    status_code=status.HTTP_201_CREATED,
    response_model=UserResponse,
)
async def registration(
    user: UserCreate,
    db: IRepository = Depends(get_users),
):
    user.password = get_hashed(user.password)
    new_user: PostgresUser = PostgresUser(**user.__dict__)

    db.add(new_user)
    d = {k: v for k, v in new_user.__dict__.items() if isinstance(v, str)}

    print("THERE IS RESPONSE MAPPING", d)
    return d


@user_router.delete("", status_code=status.HTTP_204_NO_CONTENT)
async def delete_account(
    user=Depends(get_current_user), db: IRepository = Depends(get_users)
):
    db.remove(user)
