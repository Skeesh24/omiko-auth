from dataclasses import dataclass
from os import environ


@dataclass
class sett:
    SERVER_PORT: int = int(environ.get("SERVER_PORT"))
    SERVER_HOST: str = environ.get("SERVER_HOST")
    SSL_KEYFILE: str = environ.get("SSL_KEYFILE")
    SSL_CERTFILE: str = environ.get("SSL_CERTFILE")
