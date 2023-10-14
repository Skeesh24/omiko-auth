from os import environ

from pydantic import BaseModel


class Settings(BaseModel):
    authjwt_secret_key: str = environ.get("JWT_SECRET_KEY")
    authjwt_algorithm: str = environ.get("JWT_ALGORYTHM")
    authjwt_access_token_expires: int = int(environ.get("JWT_TOKEN_EXPIRATION_MINUTES"))
    authjwt_refresh_token_expires: int = int(environ.get("JWT_TOKEN_EXPIRATION_DAYS"))
    authjwt_token_type: str = environ.get("JWT_TOKEN_TYPE")
