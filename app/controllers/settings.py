from dataclasses import dataclass
from os import environ


@dataclass
class sett:
    DEBUG: str = environ.get("DEBUG")
    BROKER_HOST: str = environ.get("BROKER_HOST")
    RECOVERY_QUEUE: str = environ.get("RECOVERY_QUEUE")
    SENDER_TO: str = environ.get("SENDER_TO")
    SENDER_SUBJECT: str = environ.get("SENDER_SUBJECT")

    INVALID_TOKEN_DETAIL: str = (
        "received invalid token"
        if not environ.get("INVALID_TOKEN_DETAIL")
        else environ.get("INVALID_TOKEN_DETAIL")
    )
    TOKEN_NOT_FOUND_DETAIL: str = (
        "token not found"
        if not environ.get("TOKEN_NOT_FOUND_DETAIL")
        else environ.get("TOKEN_NOT_FOUND_DETAIL")
    )
    DELETE_ERROR_DETAIL: str = (
        "error deleting token"
        if not environ.get("DELETE_ERROR_DETAIL")
        else environ.get("DELETE_ERROR_DETAIL")
    )

    AUTH_PREFIX: str = (
        "auth" if not environ.get("AUTH_PREFIX") else environ.get("AUTH_PREFIX")
    )
    USER_PREFIX: str = (
        "user" if not environ.get("USER_PREFIX") else environ.get("USER_PREFIX")
    )
    CACHE_TOKEN_SUFFIX: str = (
        "_token"
        if not environ.get("CACHE_TOKEN_SUFFIX")
        else environ.get("CACHE_TOKEN_SUFFIX")
    )
    CACHE_PROFILE_SUFFIX: str = (
        "_profile"
        if not environ.get("CACHE_PROFILE_SUFFIX")
        else environ.get("CACHE_PROFILE_SUFFIX")
    )

    LOGIN_ROUTE: str = (
        "login" if not environ.get("LOGIN_ROUTE") else environ.get("LOGIN_ROUTE")
    )
    LOGOUT_ROUTE: str = (
        "logout" if not environ.get("LOGOUT_ROUTE") else environ.get("LOGOUT_ROUTE")
    )
    REFRESH_ROUTE: str = (
        "refresh" if not environ.get("REFRESH_ROUTE") else environ.get("REFRESH_ROUTE")
    )
    RECOVERY_ROUTE: str = (
        "recovery"
        if not environ.get("RECOVERY_ROUTE")
        else environ.get("RECOVERY_ROUTE")
    )
    WHOIAM_ROUTE: str = (
        "whoiam" if not environ.get("WHOIAM_ROUTE") else environ.get("WHOIAM_ROUTE")
    )
