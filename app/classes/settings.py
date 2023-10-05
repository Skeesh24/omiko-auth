from dataclasses import dataclass
from os import environ


@dataclass
class sett:
    REDIS_HOST: str = environ.get("REDIS_HOST")
    BROKER_HOST: str = environ.get("BROKER_HOST")
    RECOVERY_QUEUE = environ.get("RECOVERY_QUEUE")
    DEBUG: str = environ.get("DEBUG")
    SENDER_TO: str = environ.get("SENDER_TO")
    SENDER_SUBJECT: str = environ.get("SENDER_SUBJECT")
