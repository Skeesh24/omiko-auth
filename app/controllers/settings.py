from dataclasses import dataclass
from os import environ


@dataclass
class sett:
    DEBUG: str = environ.get("DEBUG")
    BROKER_HOST: str = environ.get("BROKER_HOST")
    RECOVERY_QUEUE: str = environ.get("RECOVERY_QUEUE")
    SENDER_TO: str = environ.get("SENDER_TO")
    SENDER_SUBJECT: str = environ.get("SENDER_SUBJECT")

    INVALID_TOKEN_DETAIL: str = "received invalid token"
    TOKEN_NOT_FOUND_DETAIL: str = "token not found"
    DELETE_ERROR_DETAIL: str = "error deleting token"

    AUTH_PREFIX: str = "auth"
    USER_PREFIX: str = "user"
    CACHE_TOKEN_SUFFIX: str = "_token"
    CACHE_PROFILE_SUFFIX: str = "_profile"

    LOGIN_ROUTE: str = "login"
    LOGOUT_ROUTE: str = "logout"
    REFRESH_ROUTE: str = "refresh"
    RECOVERY_ROUTE: str = "recovery"
    WHOIAM_ROUTE: str = "whoiam"
