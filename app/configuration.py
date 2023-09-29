from pydantic import BaseModel
from os import environ


class Settings(BaseModel):
    authjwt_secret_key: str = environ.get("JWT_SECRET_KEY")
    authjwt_algorithm: str = environ.get("JWT_ALGORYTHM")
    authjwt_access_token_expires: int = int(environ.get("JWT_TOKEN_EXPIRATION_MINUTES"))
    authjwt_refresh_token_expires: int = int(environ.get("JWT_TOKEN_EXPIRATION_DAYS"))
    REDIS_EXTERNAL: str = environ.get("REDIS_EXTERNAL")
    RECOVERY_QUEUE: str = environ.get("RECOVERY_QUEUE")
    BROKER_HOST: str = environ.get("BROKER_HOST")
    DEBUG: str = environ.get("DEBUG")
