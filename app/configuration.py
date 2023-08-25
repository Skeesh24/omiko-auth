from pydantic import BaseModel
from os import environ


class Settings(BaseModel):
    def __init__(self) -> None:
        self.authjwt_secret_key: str = environ.get("JWT_SECRET_KEY")
        self.authjwt_algorithm = environ.get("JWT_ALGORYTHM")
        self.authjwt_access_token_expires: int = int(
            environ.get("JWT_TOKEN_EXPIRATION_MINUTES")
        )
        self.authjwt_refresh_token_expires: int = int(
            environ.get("JWT_TOKEN_EXPIRATION_DAYS")
        )
