from app.classes.repository import UserFirebase


async def get_users():
    return UserFirebase()