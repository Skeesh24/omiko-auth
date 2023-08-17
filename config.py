from dataclasses import dataclass
from os import environ


@dataclass
class config:
    JWT_SECRET_KEY: str = environ.get("JWT_SECRET_KEY")
    JWT_ALGORYTHM: str = environ.get("JWT_ALGORYTHM")
    JWT_TOKEN_EXPIRATION_MINUTES: float = float(
        environ.get("JWT_TOKEN_EXPIRATION_MINUTES")
    )
