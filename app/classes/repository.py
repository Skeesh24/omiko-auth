from typing import List, Union
from fastapi import HTTPException, status
from random import randint
from google.cloud.firestore_v1.base_document import DocumentSnapshot

from .validation import FilterModel, UserCreate, UserBase, UserResponse
from .firebase import get_db


class UserFirebase:
    def __init__(self) -> None:
        self.users = get_db().collection('user')
        self.db = get_db()

    def get(
        self, limit: int = 5, offset: int = 0, where: FilterModel = None
    ) -> Union[List[UserResponse], UserResponse]:
        """
        ## Gets a document by id

        1. param limit - the number of documents to retrieve
        2. param offset - the offset to get the document
        3. param document_id: the id of the document from the generic collection
        4. param where - the filter to get the document

        ### returns a list of documents
        """
        query = self.users

        try:
            if where:
                query = query.where(**where.d())
            query = query.limit(limit).offset(offset)
        except:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST)

        elements = query.get()

        if limit == 1:
            res: dict = elements[0].to_dict()
            res.update({"id":elements[0].id})
            return res

        res = [e._data for e in elements] \
              if not isinstance(elements, DocumentSnapshot) \
              else elements.to_dict()
        
        [e.update({"id": e.id}) for e in elements]

        return res

    def add(self, element: UserCreate) -> None:
        """
        ## Adds a document in the generic collection

        1. param element: the document to add

        ### returns None or raises exception
        """
        query = self.users

        try:
            query.add(document_data=element.model_dump(exclude_defaults=True))
        except Exception:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST)

    def update(self, user_id: str, element: UserBase) -> None:  
        """
        ## Updates document by the document's id

        1. param document_id: the id of the document from the generic collection
        2. param element: the source document for the update

        ### returns None or raises exception
        """

        try:
            self.remove(user_id)
            self.users.add(
                document_data=element.model_dump(exclude_defaults=True),
                document_id=user_id,
            )

        except Exception:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST)

    def remove(self, user: UserResponse) -> None:  
        """
        ## Removes document by the document's id

        1. param document_id: the id of the document from the generic collection

        ### returns None or raises exception
        """

        try:
            self.db.recursive_delete(self.users.document(user.id))
        except:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST)