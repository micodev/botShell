import asyncio
from utilities import utilities
from Db.dev_sql import addDevUser, getDevsUsers, getDevUser, remDevUser
from telethon import utils, errors
import re


async def addDev_user(message, from_id):
    try:
        if getDevUser(from_id):
            return await message.reply("User already added as Dev.")
        addDevUser(from_id)
        utilities.devs.append(from_id)
        return await message.reply("User is Dev now.")
    except Exception as e:
        utilities.prRed(str(type(e)) + " Error : " + str(e))
        return await message.reply(str(e))


async def remDev_user(message, from_id):
    try:
        if not getDevUser(from_id):
            return await message.reply("User already not dev.")
        remDevUser(from_id)
        utilities.devs.remove(from_id)
        return await message.reply("User is not dev now.")
    except Exception as e:
        utilities.prRed(str(type(e)) + " Error : " + str(e))
        return await message.reply(str(e))


async def run(message, matches, chat_id, step, crons=None):

    response = []
    if message.is_private or message.sender_id not in utilities.config["sudo_members"]:
        return []
    if matches == "getDevs":
        muted = getDevsUsers()
        for user in muted:
            print(user.user_id)
    if matches[0] == "dev":
        if re.match(r"@[a-zA-Z][\w\d]{3,30}[a-zA-Z\d]", matches[1]):
            user = await utilities.client.get_entity(matches[1])
            return [addDev_user(message, user.id)]
        elif re.match(r"(\d)", matches[1]):
            return [addDev_user(message, matches[1])]
        else:
            return [message.reply("please, use by reply or use valid username and id")]
    elif matches[0] == "rdev":
        if re.match(r"@[a-zA-Z][\w\d]{3,30}[a-zA-Z\d]", matches[1]):
            user = await utilities.client.get_entity(matches[1])
            name = user.first_name
            return [remDev_user(message, user.id)]
        elif re.match(r"(\d)", matches[1]):
            return [remDev_user(message, matches[1])]
        else:
            return [message.reply("please, use by reply or use valid username and id")]
    elif matches == "dev":
        if message.is_reply:
            msg = await message.get_reply_message()
            fromId = msg.from_id
            chat_id = msg.chat_id
            name = (await msg.get_sender()).first_name
            return [addDev_user(message, fromId)]

    elif matches == "rdev":
        if message.is_reply:
            msg = await message.get_reply_message()
            fromId = msg.from_id
            chat_id = msg.chat_id
            return [remDev_user(message, fromId)]
    return response


plugin = {
    "name": "dev users",
    "desc": "Make someone dev",
    "usage": [
        "[!/#]dev in reply to message to dev a user.",
        "[!/#]rdev in reply to message to undev a user.",
        "[!/#]dev <id or username> to dev a user by id/username.",
        "[!/#]rdev <id or username> to undev a user by id/username.",
    ],
    "run": run,
    "sudo": True,
    "patterns": [
        "^[!/#](getDevs)",
        "^[!/#](dev)$",
        "^[!/#](rdev)$",
        "^[!/#](dev) (.+)$",
        "^[!/#](rdev) (.+)$",
    ],
}
