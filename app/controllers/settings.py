from dataclasses import dataclass
from os import environ

env = lambda key: environ.get(key, "")


@dataclass
class sett:
    DEBUG: str = environ.get("DEBUG")
    BROKER_HOST: str = environ.get("BROKER_HOST")
    RECOVERY_QUEUE: str = environ.get("RECOVERY_QUEUE")
    SENDER_TO: str = environ.get("SENDER_TO")
    SENDER_SUBJECT: str = environ.get("SENDER_SUBJECT")

    INVALID_TOKEN_DETAIL: str = (
        "received invalid token"
        if not env("INVALID_TOKEN_DETAIL")
        else env("INVALID_TOKEN_DETAIL")
    )
    TOKEN_NOT_FOUND_DETAIL: str = (
        "token not found"
        if not env("TOKEN_NOT_FOUND_DETAIL")
        else env("TOKEN_NOT_FOUND_DETAIL")
    )
    DELETE_ERROR_DETAIL: str = (
        "error deleting token"
        if not env("DELETE_ERROR_DETAIL")
        else env("DELETE_ERROR_DETAIL")
    )

    AUTH_PREFIX: str = "auth" if not env("AUTH_PREFIX") else env("AUTH_PREFIX")
    USER_PREFIX: str = "user" if not env("USER_PREFIX") else env("USER_PREFIX")
    CACHE_TOKEN_SUFFIX: str = (
        "_token" if not env("CACHE_TOKEN_SUFFIX") else env("CACHE_TOKEN_SUFFIX")
    )
    CACHE_PROFILE_SUFFIX: str = (
        "_profile" if not env("CACHE_PROFILE_SUFFIX") else env("CACHE_PROFILE_SUFFIX")
    )

    LOGIN_ROUTE: str = "login" if not env("LOGIN_ROUTE") else env("LOGIN_ROUTE")
    LOGOUT_ROUTE: str = "logout" if not env("LOGOUT_ROUTE") else env("LOGOUT_ROUTE")
    REFRESH_ROUTE: str = "refresh" if not env("REFRESH_ROUTE") else env("REFRESH_ROUTE")
    RECOVERY_ROUTE: str = (
        "recovery" if not env("RECOVERY_ROUTE") else env("RECOVERY_ROUTE")
    )
    WHOIAM_ROUTE: str = "whoiam" if not env("WHOIAM_ROUTE") else env("WHOIAM_ROUTE")
