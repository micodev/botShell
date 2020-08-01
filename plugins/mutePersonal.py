import asyncio
from utilities import utilities
from Db.mute_sql import addMuteUser, getMutedUsers, getMutedUser, remMuteUser
from telethon import utils, errors
import re


def escape(strin):
    alphanumeric = ""
    for character in strin:
        if character.isalnum():
            alphanumeric += character
        else:
            alphanumeric += "-"
    return alphanumeric


async def mute_user(message, from_id, chat_id, name):
    try:
        if getMutedUser(chat_id, from_id):
            return await message.reply("User already muted.")
        await utilities.client.edit_permissions(chat_id, from_id, send_messages=False)
        addMuteUser(chat_id, escape(name), from_id)
        return await message.reply("User muted successfully.")
    except errors.ChatAdminRequiredError as e:
        return await message.reply("Make me admin in group first.")
    except errors.UserAdminInvalidError:
        return await message.reply("Do not use it with admin dude.")
    except Exception as e:
        utilities.prRed(str(type(e)) + " Error : " + str(e))
        return await message.reply(str(e))


async def unmute_user(message, from_id, chat_id):
    try:
        if not getMutedUser(chat_id, from_id):
            return await message.reply("User already unmuted.")
        await utilities.client.edit_permissions(chat_id, from_id, send_messages=True)
        remMuteUser(chat_id, from_id)
        return await message.reply("User unmuted successfully.")
    except errors.ChatAdminRequiredError as e:
        return await message.reply("Make me admin in group first.")
    except errors.UserAdminInvalidError:
        return await message.reply("Do not use it with admin dude.")
    except Exception as e:
        utilities.prRed(str(type(e)) + " Error : " + str(e))
        return await message.reply(str(e))


async def run(message, matches, chat_id, step, crons=None):

    response = []
    if message.is_private:
        return []
    if matches == "getMuted":
        muted = getMutedUsers(chat_id)
        for user in muted:
            print(user.user_id)
    if matches[0] == "mu":
        if re.match(r"@[a-zA-Z][\w\d]{3,30}[a-zA-Z\d]", matches[1]):
            user = await utilities.client.get_entity(matches[1])
            name = user.first_name
            return [mute_user(message, user.id, chat_id, name)]
        elif re.match(r"(\d)", matches[1]):
            return [mute_user(message, matches[1], chat_id, "muteById")]
        else:
            return [message.reply("please, use by reply or use valid username and id")]
    elif matches[0] == "rmu":
        if re.match(r"@[a-zA-Z][\w\d]{3,30}[a-zA-Z\d]", matches[1]):
            user = await utilities.client.get_entity(matches[1])
            name = user.first_name
            return [unmute_user(message, user.id, chat_id)]
        elif re.match(r"(\d)", matches[1]):
            return [unmute_user(message, matches[1], chat_id)]
        else:
            return [message.reply("please, use by reply or use valid username and id")]
    elif matches == "mu":
        if message.is_reply:
            msg = await message.get_reply_message()
            fromId = msg.from_id
            chat_id = msg.chat_id
            name = (await msg.get_sender()).first_name
            return [mute_user(message, fromId, chat_id, name)]

    elif matches == "rmu":
        if message.is_reply:
            msg = await message.get_reply_message()
            fromId = msg.from_id
            chat_id = msg.chat_id
            return [unmute_user(message, fromId, chat_id)]

    return response


plugin = {
    "name": "mute users",
    "desc": "Mute/unmute users in chat.",
    "usage": [
        "[!/#]mu in reply to message to mute user.",
        "[!/#]rmu in reply to message to unmute user.",
        "[!/#]mu <id or username> to mute user by id/username.",
        "[!/#]rmu <id or username> to unmute user by id/username.",
    ],
    "run": run,
    "sudo": True,
    "patterns": [
        "^[!/#](getMuted)",
        "^[!/#](mu)$",
        "^[!/#](rmu)$",
        "^[!/#](mu) (.+)$",
        "^[!/#](rmu) (.+)$",
    ],
}
