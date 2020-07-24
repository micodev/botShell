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


class MutePersonal(Base):
    __tablename__ = "mute"
    id = Column(Integer, primary_key=True, autoincrement=True)
    first_name = Column(String)
    chat_id = Column(Numeric)
    user_id = Column(Numeric)

    def __init__(self, id, chat_id, first_name, user_id):
        self.chat_id = chat_id
        self.first_name = utilities.markdown_escape(first_name)
        self.user_id = user_id
        self.id = id


MutePersonal.__table__.create(checkfirst=True)


def getMutedUser(chat_id, from_id):
    try:
        muteUser = (
            SESSION.query(MutePersonal)
            .filter(MutePersonal.chat_id == chat_id)
            .filter(MutePersonal.user_id == from_id)
            .one()
        )
        SESSION.close()
        return muteUser
    except:
        return None


def getMutedUsers(chat_id):
    try:
        return SESSION.query(MutePersonal).filter(MutePersonal.chat_id == chat_id).all()
    except:
        return None
    finally:
        SESSION.close()


def addMuteUser(chat_id, first_name, user_id):
    addUser = (
        SESSION.query(MutePersonal)
        .filter(MutePersonal.chat_id == chat_id)
        .filter(MutePersonal.user_id == user_id)
        .first()
    )
    if addUser:
        raise Exception("The user already muted.")
    else:
        addUser = MutePersonal(None, chat_id, first_name, user_id)
        SESSION.add(addUser)
        SESSION.commit()
        # SESSION.close()


def remMuteUser(chat_id, user_id):
    reUser = (
        SESSION.query(MutePersonal)
        .filter(MutePersonal.chat_id == chat_id)
        .filter(MutePersonal.user_id == user_id)
        .first()
    )
    if reUser:
        SESSION.delete(reUser)
        SESSION.commit()
    else:
        raise Exception("No user to remove.")

