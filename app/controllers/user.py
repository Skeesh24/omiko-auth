from os import environ
from typing import List

from classes.crypto import get_hashed
from classes.dependencies import (
    get_caching_service,
    get_current_user,
    get_message_broker,
    get_users,
)
from classes.functions import to_dict
from classes.interfaces import IBroker, ICacheService, IRepository
from classes.services import SettingsService
from classes.settings import sett
from classes.validation import UserCreate, UserResponse
from database.entities import DatabaseUser, DatabaseUserInsert
from fastapi import APIRouter, Body, Depends, HTTPException, status
from sqlalchemy.exc import NoInspectionAvailable

user_router = APIRouter(prefix="/user", tags=["user"])


@user_router.get("", response_model=List[UserResponse])
async def get_all_users(
    limit: int = 5, offset: int = 0, db: IRepository = Depends(get_users)
):
    users: List[DatabaseUser] = db.get(
        limit=limit,
        offset=offset,
    )

    if not isinstance(users, list) or len(users) == 0:
        users = [users]

    try:
        res = [to_dict(user) for user in users] if users[0] is not None else []
    except NoInspectionAvailable:
        res = []

    return res


@user_router.get("/{email}", response_model=UserResponse)
async def get_user_by_email(email: str, db: IRepository = Depends(get_users)):
    user = db.get(limit=1, offset=0, username=email)
    try:
        res = to_dict(user)
    except NoInspectionAvailable:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

    return res


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
    new_user: DatabaseUserInsert = DatabaseUserInsert(**user.__dict__)
    new_user = db.add(new_user)
    result = to_dict(new_user)
    return result


@user_router.post("/recovery", status_code=status.HTTP_201_CREATED)
async def password_recovery(
    msg: str,
    to: str = sett.SENDER_TO,
    subject: str = sett.SENDER_SUBJECT,
    db: IRepository = Depends(get_users),
    broker: IBroker = Depends(get_message_broker),
):
    broker.create_connection(sett.BROKER_HOST, sett.RECOVERY_QUEUE)
    broker.publish(str({"to": to, "subject": subject, "msg": msg}))
    broker.close()


@user_router.post("/whoiam", response_model=UserResponse)
async def whoiam(
    me: IRepository = Depends(get_current_user),
):
    return me.__dict__


@user_router.delete("", status_code=status.HTTP_204_NO_CONTENT)
async def delete_account(
    user=Depends(get_current_user),
    db: IRepository = Depends(get_users),
    cache: ICacheService = Depends(get_caching_service),
):
    db.remove(user)
    cache.remove(user.username + "_profile")
    cache.remove(user.username + "_token")
