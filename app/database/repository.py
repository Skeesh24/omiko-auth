from typing import Union

from classes.interfaces import IRepository
from classes.validation import FilterModel, UserCreate, UserResponse
from database.firebase.entities import FireUser
from database.firebase.firebase import get_db
from database.postgres.entities import PostgresUser
from database.postgres.postgres import get_session
from fastapi import HTTPException, status
from google.cloud.firestore_v1.base_document import DocumentSnapshot
from sqlalchemy import text

CREATE_USER_TABLE = "CALL create_user_table()"


class UserFirebase(IRepository):
    def __init__(self) -> None:
        self.users = get_db().collection("user")
        self.db = get_db()

    def get(self, limit: int = 5, offset: int = 0, **kwargs) -> dict:
        """
        ## Gets a document by id

        1. param limit - the number of documents to retrieve
        2. param offset - the offset to get the document
        3. param document_id: the id of the document from the generic collection
        4. param where - the filter to get the document

        ### returns a list of documents
        """
        query = self.users

        where = None  # where parameter needs to be constructed automatically
        raise NotImplementedError()

        try:
            if where:
                query = query.where(**where.d())
            query = query.limit(limit).offset(offset)
        except Exception as e:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

        elements = query.get()

        if len(elements) == 0:
            return {}

        if limit == 1:
            res: dict = elements[0].to_dict()
            res.update({"id": elements[0].id})
            return res

        if isinstance(elements, DocumentSnapshot):
            res: dict = elements._data
            res.update({"id": elements.id})
            return res

        res: list[dict] = [e._data for e in elements]

        for i in range(len(res)):
            res[i].update({"id": elements[i].id})

        return res

    def add(self, element: UserCreate) -> UserResponse:
        """
        ## Adds a document to the generic collection

        1. param element: the document to add

        ### returns None or raises exception
        """
        # need to cache
        users = self.get(limit=1, where=FilterModel.fast("username", element.username))
        if users.get("username"):
            raise HTTPException(
                status.HTTP_409_CONFLICT, "this username is already in use"
            )

        new_elem = FireUser(**element.dict(exclude_defaults=True))
        new_elem.save()
        return new_elem.to_dict()

    def update(self, user: UserResponse) -> None:
        """
        ## Updates document by the document's id

        1. param document_id: the id of the document from the generic collection
        2. param element: the source document for the update

        ### returns None or raises exception
        """

        pass

        # try:
        #     self.remove(user)
        #     UserCreate(**user.model_dump(exclude_defaults=True)).save()
        #     return user

        # except Exception as e:
        #     raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST)

    def remove(self, user: UserResponse) -> None:
        """
        ## Removes document by the document's id

        1. param document_id: the id of the document from the generic collection

        ### returns None or raises exception
        """

        self.db.recursive_delete(self.users.document(user.id))


class UserPostgres(IRepository):
    def __init__(self) -> None:
        self.db = get_session()

    def get_users(self):
        self.db.execute(text(CREATE_USER_TABLE))
        return self.db.query(PostgresUser)

    def get(
        self, limit: int = 5, offset: int = 0, **kwargs
    ) -> Union[list[PostgresUser], PostgresUser]:
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
