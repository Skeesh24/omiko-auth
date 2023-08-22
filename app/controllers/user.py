from typing import List, Union
from fastapi.responses import JSONResponse
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm

from app.classes.crypto import get_hashed
from app.classes.dependencies import get_current_user, get_users
from app.database.firebase.repository import UserFirebase
from app.classes.validation import FilterModel, UserCreate, UserResponse


user_router = APIRouter(prefix="/user", tags=["user"])


@user_router.get("", response_model=Union[List[UserResponse], UserResponse])
async def get_all_users(
    limit: int = 5, offset: int = 0, db: UserFirebase = Depends(get_users)
):
    users = db.get(limit=limit, offset=offset)
    return users


@user_router.get("/{email}", response_model=UserResponse)
async def get_user_by_email(email: str, db: UserFirebase = Depends(get_users)):
    user = db.get(limit=1, where=FilterModel.fast("email", email))
    return user


@user_router.post(
    "",
    status_code=status.HTTP_201_CREATED,
    response_model=UserResponse,
)
async def registration_and_authorization(
    credentials: OAuth2PasswordRequestForm = Depends(),
    db: UserFirebase = Depends(get_users),
):
    try:
        user = UserCreate(username=credentials.username, password=credentials.password)
        user.password = get_hashed(user.password)

        print(user.__dict__)
        response = db.add(user)

        return response
    except Exception as e:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, detail=str(e))


@user_router.delete("", status_code=status.HTTP_204_NO_CONTENT)
async def delete_account(
    user=Depends(get_current_user), db: UserFirebase = Depends(get_users)
):
    db.remove(user)
