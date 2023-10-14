from dataclasses import dataclass
from os import environ


@dataclass
class sett:
    CACHE_HOST: str = environ.get("CACHE_HOST")
    BROKER_HOST: str = environ.get("BROKER_HOST")
    RECOVERY_QUEUE = environ.get("RECOVERY_QUEUE")
    DEBUG: str = environ.get("DEBUG")
    SENDER_TO: str = environ.get("SENDER_TO")
    SENDER_SUBJECT: str = environ.get("SENDER_SUBJECT")

    CACHE_PROFILE_SUFFIX: str = "_profile"
    MEMCACHED_CLOSE_EXCEPTION: str = "Error closing memcached session: "
    REDIS_CLOSE_EXCEPTION: str = "Error closing redis session: "