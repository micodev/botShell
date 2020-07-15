import os
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, scoped_session
from utilities import utilities


def start() -> scoped_session:
    engine = create_engine(utilities.config["db"])
    Base.metadata.bind = engine
    Base.metadata.create_all(engine)
    return scoped_session(sessionmaker(bind=engine, autoflush=False))


try:
    Base = declarative_base()
    SESSION = start()
except AttributeError as e:
    print("db is not configured. Features depending on the database might have issues.")
    print(str(e))
