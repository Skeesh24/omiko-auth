from dataclasses import dataclass
from os import environ

env = lambda key: environ.get(key, "")


@dataclass
class sett:
    CACHE_HOST: str = environ.get("CACHE_HOST")
    BROKER_HOST: str = environ.get("BROKER_HOST")
    RECOVERY_QUEUE = environ.get("RECOVERY_QUEUE")
    DEBUG: str = environ.get("DEBUG")
    SENDER_TO: str = environ.get("SENDER_TO")
    SENDER_SUBJECT: str = environ.get("SENDER_SUBJECT")

    CACHE_PROFILE_SUFFIX: str = (
        "_profile" if not env("CACHE_PROFILE_SUFFIX") else env("CACHE_PROFILE_SUFFIX")
    )
    MEMCACHED_CLOSE_EXCEPTION: str = (
        "Error closing memcached session: "
        if not env("MEMCACHED_CLOSE_EXCEPTION")
        else env("MEMCACHED_CLOSE_EXCEPTION")
    )
    REDIS_CLOSE_EXCEPTION: str = (
        "Error closing redis session: "
        if not env("REDIS_CLOSE_EXCEPTION")
        else env("REDIS_CLOSE_EXCEPTION")
    )

    FIREBASE_EQUAL_SIGN: str = (
        "==" if not env("FIREBASE_EQUAL_SIGN") else env("FIREBASE_EQUAL_SIGN")
    )
