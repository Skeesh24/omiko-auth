from typing import List, Union
from fastapi import APIRouter, Depends
from fastapi import status

from app.classes.oauth2 import get_current_user, get_hashed
from app.classes.validation import UserCreate, UserBase, UserResponse
from app.classes.dependencies import get_users
from app.classes.repository import UserFirebase
from app.classes.validation import FilterModel


user_router = APIRouter(prefix="/user", tags=["user"])


@user_router.get("", response_model=Union[List[UserResponse], UserResponse])
async def get_all_users(limit: int = 5, offset: int = 0, db: UserFirebase = Depends(get_users)):
    users = db.get(limit=limit, offset=offset)
    return users


@user_router.get("/{email:str}", response_model=UserResponse)
async def get_user_by_email(email: str, db: UserFirebase = Depends(get_users)):
    user = db.get(limit=1, where=FilterModel.fast("email", email))
    return user


@user_router.post("", status_code=status.HTTP_201_CREATED, response_model=UserBase)
async def registration(user: UserCreate, db: UserFirebase = Depends(get_users)):
    user.password = get_hashed(user.password)
    return db.add(user)


@user_router.delete("", status_code=status.HTTP_204_NO_CONTENT)
async def delete_account(user=Depends(get_current_user), db: UserFirebase = Depends(get_users)):
    db.remove(user)
    