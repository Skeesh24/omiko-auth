from dataclasses import dataclass

from httpx import Client


@dataclass
class testconfig:
    BASE: str = "http://localhost:10000"
    REFRESH: str = "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJzdWIiOiJqZXN1cyIsImlhdCI6MTY5MjcxMzEwNSwibmJmIjoxNjkyNzEzMTA1LCJqdGkiOiI4NzdiNThkYS05Y2ZjLTRjMGEtYTQyOC1kZjg4ODc5MzBmYTkiLCJleHAiOjE2OTI3MTMxMjksInR5cGUiOiJhY2Nlc3MiLCJmcmVzaCI6ZmFsc2V9.cQffAlkxpyj2juAmQkANsSkDagLLC1R5-KKCokfOZg0"
    ACCESS: str = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJqb3NoIiwiaWF0IjoxNjkyOTY1MTk2LCJuYmYiOjE2OTI5NjUxOTYsImp0aSI6IjFlM2NhOTc5LTg4ZmQtNDgzNi1hZWExLTJjZGIzNDcxMGUxZCIsImV4cCI6MTY5Mjk2NjYzNiwidHlwZSI6ImFjY2VzcyIsImZyZXNoIjpmYWxzZX0.he03Qu0G3eV1V--A4iwI-nbXJsOn5nWIqdiXBrSWPXk"

    @classmethod
    def get_client(cls, prefix: str = ""):
        return Client(base_url=cls.BASE + prefix)
