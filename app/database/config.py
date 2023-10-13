from dataclasses import dataclass
from os import environ


@dataclass
class sett:
    PROVIDER: str = environ.get("PROVIDER")
    DRIVER: str = environ.get("DRIVER")
    DB_USER: str = environ.get("DB_USER")
    DB_PASSWORD: str = environ.get("DB_PASSWORD")
    DB_HOST: str = environ.get("DB_HOST")
    DB_PORT: str = environ.get("DB_PORT")
    DB_DBNAME: str = environ.get("DB_DBNAME")
    ID_SERVER_DEFAULT: str = environ.get("ID_SERVER_DEFAULT")
    NOT_INTERNAL_DB: str = environ.get("NOT_INTERNAL_DB")
    USER_TABLENAME: str = environ.get("USER_TABLENAME")
