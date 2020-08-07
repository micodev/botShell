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
from Db import SESSION, Base
import os


class AutoReply(Base):
    __tablename__ = "AutoReply"
    id = Column(Integer, autoincrement=True, primary_key=True)
    text = Column(String)
    file_id = Column(String)
    msg_type = Column(String)
    msg_content = Column(String)

    def __init__(self, text, msg_type, msg_content, file_id, id=None):
        self.id = id
        self.msg_type = msg_type
        self.file_id = file_id
        self.text = text
        self.msg_content = msg_content


AutoReply.__table__.create(checkfirst=True)


def getAutoReply(text):
    try:
        return SESSION.query(AutoReply).filter(AutoReply.text == text).one()
    except:
        return None
    finally:
        SESSION.close()


def getAllAutoReply():
    try:
        return SESSION.query(AutoReply).all()
    except:
        return None
    finally:
        SESSION.close()


def addAutoReply(text, msg_type, msg_content="", file_id=""):
    try:
        addRep = SESSION.query(AutoReply).filter(AutoReply.text == text).one()
    except Exception as e:
        addRep = None
        print(str("error : togglepropsetting : %s" % (e)))

    if addRep:
        addRep.msg_type = msg_type
        addRep.msg_content = msg_content
        try:
            os.remove(addRep.file_id)
        except Exception as e:
            print("addAutoReplySetting : %s" % (e))
        addRep.file_id = file_id
    else:
        addRep = AutoReply(text, msg_type, msg_content, file_id)
    SESSION.add(addRep)
    SESSION.commit()


def remAutoReplySetting(text):
    try:
        remrep = SESSION.query(AutoReply).filter(AutoReply.text == text).one()
        if remrep:
            SESSION.delete(remrep)
            SESSION.commit()
        return True
    except:
        return False

