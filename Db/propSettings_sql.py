from sqlalchemy import (
    BigInteger,
    Integer,
    Boolean,
    Column,
    LargeBinary,
    Numeric,
    String,
    UnicodeText,
)
from Db import SESSION, Base
import os


class PropSetting(Base):
    __tablename__ = "propSettings"
    id = Column(Integer, autoincrement=True, primary_key=True)
    chatId = Column(Numeric)
    propName = Column(String)
    active = Column(Boolean)

    def __init__(self, chatId, propName, active, id=None):
        self.chatId = chatId
        self.propName = propName
        self.active = active
        self.id = id


PropSetting.__table__.create(checkfirst=True)


def getPropSettings(chatId):
    try:
        return SESSION.query(PropSetting).filter(PropSetting.chatId == chatId).get()
    except:
        return None
    finally:
        SESSION.close()


def getPropSetting(chatId, propName):
    try:
        return (
            SESSION.query(PropSetting)
            .filter(PropSetting.chatId == chatId and PropSetting.propName == propName)
            .one()
        )
    except:
        return None
    finally:
        SESSION.close()


def togglePropSettings(chatId, propName, active=True):
    try:
        try:
            addProp = (
                SESSION.query(PropSetting)
                .filter(
                    PropSetting.chatId == chatId and PropSetting.propName == propName
                )
                .one()
            )
        except Exception as e:
            addProp = None
            print(str("error : togglepropsetting : %s" % (e)))

        if addProp:
            addProp.propName = propName
            addProp.active = active
        else:
            addProp = PropSetting(chatId, propName, active)
        SESSION.add(addProp)
        SESSION.commit()
        return True
    except Exception as e:
        print(str("error : togglepropsetting : %s" % (e)))


# def remPropSettingSetting(chat_id):
#     remwel = SESSION.query(PropSetting).get(chat_id)
#     if remwel:
#         SESSION.delete(remwel)
#         SESSION.commit()

