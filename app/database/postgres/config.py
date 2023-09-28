from dataclasses import dataclass
from os import environ


@dataclass
class sett:
    PROVIDER: str = "postgresql"
    DRIVER: str = "pg8000"
    USER: str = "postgres"
    PASSWORD: str = environ.get("POSTGRES_PASSWORD")
    HOST: str = "localhost"
    PORT: int = 5432
    DBNAME: str = "omiko-auth"
