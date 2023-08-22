from passlib.context import CryptContext


def get_hashed(secret: str):
    return CryptContext(["bcrypt"]).hash(secret)


def verify(password: str, secret: str):
    return CryptContext(["bcrypt"]).verify(password, secret)