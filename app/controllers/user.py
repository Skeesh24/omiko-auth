from classes.crypto import get_hashed
from classes.dependencies import get_current_user, get_message_broker, get_users
from classes.functions import to_dict
from classes.interfaces import IBroker, IRepository
from classes.validation import UserCreate, UserResponse
from classes.services import SettingsService
from database.postgres.entities import PostgresUser
from fastapi import APIRouter, Body, Depends, status

user_router = APIRouter(prefix="/user", tags=["user"])


@user_router.get("", response_model=list[UserResponse])
async def get_all_users(
    limit: int = 5, offset: int = 0, db: IRepository = Depends(get_users)
):
    users: list[PostgresUser] = [
        db.get(
            limit=limit,
            offset=offset,
        )
    ]

    return [to_dict(user) for user in users] if users[0] is not None else []


@user_router.get("/{email}", response_model=UserResponse)
async def get_user_by_email(email: str, db: IRepository = Depends(get_users)):
    user = db.get(limit=1, offset=0, username=email)
    return to_dict(user)


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
    result = to_dict(new_user)
    return result


@user_router.post("/recovery", status_code=status.HTTP_201_CREATED)
async def password_recovery(
    email: str = Body(),
    db: IRepository = Depends(get_users),
    broker: IBroker = Depends(get_message_broker),
):
    connection = broker.create_connection(SettingsService.BROKER_HOST, queue_name=SettingsService.RECOVERY_QUEUE)
    connection.publish(email)
    connection.close()


@user_router.delete("", status_code=status.HTTP_204_NO_CONTENT)
async def delete_account(
    user=Depends(get_current_user), db: IRepository = Depends(get_users)
):
    db.remove(user)
