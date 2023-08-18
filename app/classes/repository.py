from fastapi import HTTPException, status
from google.cloud.firestore_v1.base_document import DocumentSnapshot

from .validation import FilterModel, UserCreate, UserBase, UserResponse
from .firebase import get_db
from .entities import User


class UserFirebase:
    def __init__(self) -> None:
        self.users = get_db().collection('user')
        self.db = get_db()

    def get(
        self, limit: int = 5, offset: int = 0, where: FilterModel = None
    ) -> dict:
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
        except Exception as e:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

        elements = query.get()

        if len(elements) == 0: 
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

        if limit == 1:
            res: dict = elements[0].to_dict()
            res.update({"id":elements[0].id})
            return res
        
        if isinstance(elements, DocumentSnapshot):
            res: dict = elements._data
            res.update({"id":elements.id})
            return res

        res = [e._data for e in elements] 

        for i in range(len(res)):
            res[i].update({"id":elements[i].id})

        return res

    def add(self, element: UserCreate) -> UserBase:
        """
        ## Adds a document in the generic collection

        1. param element: the document to add

        ### returns None or raises exception
        """
        query = self.users

        try:
            new_elem = element.model_dump(exclude_defaults=True)
            query.add(document_data=new_elem)
            return new_elem
        except Exception:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST)

    def update(self, user: UserResponse) -> None:  
        """
        ## Updates document by the document's id

        1. param document_id: the id of the document from the generic collection
        2. param element: the source document for the update

        ### returns None or raises exception
        """

        try:
            self.remove(user)
            User(**user.model_dump(exclude_defaults=True)).save()
            return user


        except Exception as e:
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