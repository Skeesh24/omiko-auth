from dataclasses import dataclass
from os import environ


@dataclass
class sett:
    PROVIDER: str = environ.get("PROVIDER")
    DRIVER: str = environ.get("DRIVER")
    USER: str = environ.get("USER")
    PASSWORD: str = environ.get("PASSWORD")
    HOST: str = environ.get("HOST")
    PORT: str = environ.get("PORT")
    DBNAME: str = environ.get("DBNAME")
