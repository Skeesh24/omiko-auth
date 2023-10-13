from database.config import sett
from database.database import metadata, session
from sqlalchemy import UUID, Column, String, Table, text
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class DatabaseUser(Base):
    __tablename__ = sett.USER_TABLENAME
    id = Column(
        UUID(False),
        nullable=False,
        primary_key=True,
        server_default=text(sett.ID_SERVER_DEFAULT),
    )
    username: str = Column(String(length=50), nullable=False, unique=True)
    password: str = Column(String(length=100), nullable=False)


class DatabaseUserInsert(Base):
    __tablename__ = sett.USER_INSERT_TABLENAME
    id = Column(
        UUID(False),
        nullable=True,
    )
    username: str = Column(String(length=50), nullable=False, unique=True)
    password: str = Column(String(length=100), nullable=False)
