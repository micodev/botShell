from sqlalchemy import (
    BigInteger,
    Boolean,
    Column,
    LargeBinary,
    Numeric,
    String,
    Integer,
    UnicodeText,
)
from utilities import utilities
from Db import SESSION, Base
import os


class DevUser(Base):
    __tablename__ = "dev_user"
    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Numeric)

    def __init__(self, id, user_id):
        self.user_id = user_id
        self.id = id


DevUser.__table__.create(checkfirst=True)


def getDevUser(from_id):
    try:
        devUser = SESSION.query(DevUser).filter(DevUser.user_id == from_id).one()
        SESSION.close()
        return devUser
    except:
        return None


def getDevsUsers():
    try:
        return SESSION.query(DevUser).all()
    except:
        return None
    finally:
        SESSION.close()


def addDevUser(user_id):
    addUser = SESSION.query(DevUser).filter(DevUser.user_id == user_id).first()
    if addUser:
        raise Exception("The user already added as Dev.")
    else:
        addUser = DevUser(None, user_id)
        SESSION.add(addUser)
        SESSION.commit()


def remDevUser(user_id):
    reUser = SESSION.query(DevUser).filter(DevUser.user_id == user_id).first()
    if reUser:
        SESSION.delete(reUser)
        SESSION.commit()
    else:
        raise Exception("No user to remove.")

