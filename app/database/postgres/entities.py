from database.postgres.config import sett
from database.postgres.postgres import metadata, session
from sqlalchemy import UUID, Column, String, Table, text
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class PostgresUser(Base):
    __tablename__ = "user"
    id = Column(
        UUID(False),
        nullable=False,
        primary_key=True,
        server_default=text(sett.ID_SERVER_DEFAULT),
    )
    username: str = Column(String(length=50), nullable=False, unique=True)
    password: str = Column(String(length=100), nullable=False)
