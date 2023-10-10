from database.postgres.config import sett
from sqlalchemy import MetaData, create_engine, text
from sqlalchemy.orm import sessionmaker

engine = create_engine(
    f"{sett.PROVIDER}+{sett.DRIVER}://{sett.POSTGRES_USER}:{sett.POSTGRES_PASSWORD}@{sett.POSTGRES_HOST}:{sett.POSTGRES_PORT}/{sett.POSTGRES_DBNAME}"
)

metadata = MetaData()
metadata.create_all(engine)
Session = sessionmaker(bind=engine)
session = Session()


def get_session():
    return session
