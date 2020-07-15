import asyncio
from utilities import utilities
from telethon.tl.functions.account import (
    ChangePhoneRequest,
    CheckUsernameRequest,
    SendChangePhoneCodeRequest,
    UpdateProfileRequest,
    UpdateUsernameRequest,
)
from telethon.tl.functions.photos import UploadProfilePhotoRequest
import os
from telethon.tl.types import TypeCodeSettings


async def setUser(message, username):

    valid = await utilities.client(CheckUsernameRequest(username=username))
    if valid:
        print(await utilities.client(UpdateUsernameRequest(username)))
        return message.edit("Username updated successfully.")
    else:
        return message.edit("Someone using @%s." % (username))


async def setBio(message, bio):
    if len(bio) > 70:
        return message.edit("Limit of bio is 70 as maximum.")
    await utilities.client(UpdateProfileRequest(about=bio))
    return message.edit("Bio updated successfully.")


async def setPhoto(message, msg_replied):
    try:
        file = await utilities.client.download_media(msg_replied)
        if file != None:
            await utilities.client(
                UploadProfilePhotoRequest(await utilities.client.upload_file(file))
            )
            os.remove(file)
            return message.edit("Profile photo updated successfully.")

        return message.edit("Try again !")
    except Exception as e:
        if file != None:
            os.remove(file)
        return message.edit("Try again ! %s" % (str(e)))


async def setFname(message, name):
    await utilities.client(UpdateProfileRequest(first_name=name, last_name=""))
    return message.edit("Name updated successfully.")


async def run(msg, matches, chat_id, step, crons=None):
    if not (msg.out):
        message = await msg.reply("please wait...")
    else:
        message = msg
    if matches[0] == "sbio":
        return [await setBio(message, matches[1])]
    if matches[0] == "suser":
        return [await setUser(message, matches[1])]
    if matches[0] == "sname":
        return [await setFname(message, matches[1])]
    if matches == "sphoto" and msg.is_reply:
        msg_replied = await msg.get_reply_message()
        if msg_replied.photo:
            return [await setPhoto(message, msg_replied)]
        else:
            return [message.edit("reply to an Image message please !")]
    elif matches == "sphoto":
        return [message.edit("reply to an Image message please !")]
    else:
        return []


plugin = {
    "name": "profile change",
    "desc": "Change profile info.",
    "usage": [
        "[!/#]sbio <bio>",
        "[!/#]suser <username>",
        "[/#!]sphoto (reply on image)",
        "[/#!]sname <new_name>",
    ],
    "run": run,
    "bot": False,
    "sudo": True,
    "patterns": [
        "^[!/#](sbio) (.+)$",
        "^[!/#](suser) (.+)$",
        "^[/!#](sphoto)$",
        "^[/!#](sname) (.+)$",
    ],
}
