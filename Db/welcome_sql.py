from sqlalchemy import (
    BigInteger,
    Boolean,
    Column,
    LargeBinary,
    Numeric,
    String,
    UnicodeText,
)
from Db import SESSION, Base
import os


class Welcome(Base):
    __tablename__ = "welcome"
    chat_id = Column(Numeric, primary_key=True)
    file_id = Column(String)
    msg_type = Column(String)
    msg_content = Column(String)

    def __init__(self, chat_id, msg_type, msg_content, file_id):
        self.chat_id = chat_id
        self.msg_type = msg_type
        self.file_id = file_id
        self.msg_content = msg_content


Welcome.__table__.create(checkfirst=True)


def getWelcomeSettings(chat_id):
    try:
        return SESSION.query(Welcome).filter(Welcome.chat_id == chat_id).one()
    except:
        return None
    finally:
        SESSION.close()


def addWelcomeSetting(chat_id, msg_type, msg_content="", file_id=""):
    addwel = SESSION.query(Welcome).get(chat_id)
    if addwel:
        addwel.msg_type = msg_type
        addwel.msg_content = msg_content
        try:
            os.remove(addwel.file_id)
        except Exception as e:
            print("addWelcomeSetting : %s" % (e))
        addwel.file_id = file_id
    else:
        addwel = Welcome(chat_id, msg_type, msg_content, file_id)
    SESSION.add(addwel)
    SESSION.commit()


def remWelcomeSetting(chat_id):
    remwel = SESSION.query(Welcome).get(chat_id)
    if remwel:
        SESSION.delete(remwel)
        SESSION.commit()

