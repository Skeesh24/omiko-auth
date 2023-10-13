from dataclasses import dataclass
from os import environ


@dataclass
class sett:
    PROVIDER: str = environ.get("PROVIDER")
    DRIVER: str = environ.get("DRIVER")
    POSTGRES_USER: str = environ.get("POSTGRES_USER")
    POSTGRES_PASSWORD: str = environ.get("POSTGRES_PASSWORD")
    POSTGRES_HOST: str = environ.get("POSTGRES_HOST")
    POSTGRES_PORT: str = environ.get("POSTGRES_PORT")
    POSTGRES_DBNAME: str = environ.get("POSTGRES_DBNAME")
    CREATE_USER_TABLE: str = environ.get("CREATE_USER_TABLE")

