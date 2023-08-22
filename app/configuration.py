from pydantic import BaseModel
from os import environ


class Settings(BaseModel):
    authjwt_secret_key: str = environ.get("JWT_SECRET_KEY")
    authjwt_algorithm = environ.get("JWT_ALGORYTHM")
    authjwt_access_token_expires: float = float(
        environ.get("JWT_TOKEN_EXPIRATION_MINUTES")
    )
    authjwt_refresh_token_expires: float = float(
        environ.get("JWT_TOKEN_EXPIRATION_DAYS")
    )
