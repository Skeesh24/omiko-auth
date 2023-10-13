from typing import List, Union

from classes.interfaces import IRepository
from classes.validation import FilterModel, UserCreate, UserResponse
from database.firebase.entities import FireUser
from database.firebase.firebase import get_db
from database.postgres.config import sett
from database.postgres.entities import PostgresUser
from database.postgres.postgres import get_session
from fastapi import HTTPException, status
from google.cloud.firestore_v1.base_document import DocumentSnapshot
from sqlalchemy import text


class UserPostgres(IRepository):
    def __init__(self) -> None:
        self.db = get_session()

    def get_users(self):
        if sett.ID_SERVER_DEFAULT:
            self.db.execute(text(f"CALL {sett.ID_SERVER_DEFAULT}"))
        return self.db.query(PostgresUser)

    def get(
        self, limit: int = 5, offset: int = 0, **kwargs
    ) -> Union[List[PostgresUser], PostgresUser]:
        query = self.get_users()

        if len(kwargs) > 0:
            try:
                for k, v in kwargs.items():
                    query = query.filter(
                        PostgresUser.__getattribute__(PostgresUser, k) == v
                    )
            except AttributeError:
                return None

        return (
            query.limit(limit).offset(offset).all()
            if limit > 1
            else query.limit(limit).offset(offset).first()
        )

    def add(self, user: PostgresUser) -> PostgresUser:
        try:
            self.db.add(user)
        except Exception as e:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST)
        self.db.commit()
        return user

    def update(self, update_user: PostgresUser) -> PostgresUser:
        user_id = self.get(1, 0, username=update_user.username)[0].id
        user = PostgresUser(id=user_id, **update_user.__dict__)
        try:
            self.remove(update_user)
            self.add(user)
        except Exception as e:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST)
        self.db.commit()
        return user

    def remove(self, user: PostgresUser) -> None:
        try:
            self.db.delete(user)
        except Exception as e:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)
        self.db.commit()
