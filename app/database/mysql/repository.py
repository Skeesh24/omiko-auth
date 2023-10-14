from typing import List, Union

from classes.interfaces import IRepository
from classes.validation import FilterModel, UserCreate, UserResponse
from database.config import sett
from database.database import get_session
from database.entities import DatabaseUser, DatabaseUserInsert
from database.firebase.entities import FireUser
from database.firebase.firebase import get_db
from fastapi import HTTPException, status
from google.cloud.firestore_v1.base_document import DocumentSnapshot
from sqlalchemy import text


class UserMysql(IRepository):
    def __init__(self) -> None:
        self.db = get_session()

    def get_users(self):
        if sett.NOT_INTERNAL_DB:
            self.db.execute(text(f"CALL {sett.ID_SERVER_DEFAULT}"))
        return self.db.query(DatabaseUser)

    def get(
        self, limit: int = 5, offset: int = 0, **kwargs
    ) -> Union[List[DatabaseUser], DatabaseUser]:
        query = self.get_users()

        if len(kwargs) > 0:
            try:
                for k, v in kwargs.items():
                    query = query.filter(
                        DatabaseUser.__getattribute__(DatabaseUser, k) == v
                    )
            except AttributeError:
                return None

        return (
            query.limit(limit).offset(offset).all()
            if limit > 1
            else query.limit(limit).offset(offset).first()
        )

    def add(self, user: DatabaseUserInsert) -> DatabaseUser:
        try:
            self.db.add(user)
        except Exception as e:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST)
        self.db.commit()

    def update(self, update_user: DatabaseUser) -> DatabaseUser:
        user_id = self.get(1, 0, username=update_user.username)[0].id
        user = DatabaseUser(id=user_id, **update_user.__dict__)
        try:
            self.remove(update_user)
            self.add(user)
        except Exception as e:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST)
        self.db.commit()
        return user

    def remove(self, user: DatabaseUser) -> None:
        try:
            self.db.delete(user)
        except Exception as e:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST)
        self.db.commit()
