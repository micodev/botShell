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
    if message.sender_id not in utilities.config["sudo_members"]:
        return []
    if matches == "getDevs":
        devlist = getDevsUsers()
        res = ""
        i = 1
        for user in devlist:
            userId = int("%.0f" % user.user_id)
            try:
                _user = await utilities.client.get_entity(userId)
                strin = (
                    str(i)
                    + " - [%s](tg://user?id=%s)"
                    % (_user.first_name, int("%.0f" % userId))
                    + "\n"
                )
            except Exception as e:
                strin = (
                    str(i)
                    + " - [%s](tg://user?id=%s)"
                    % (("dev" + str(i)), int("%.0f" % userId))
                    + "\n"
                )
            i += 1
            res = res + strin
        return [message.reply(res if (len(res) != 0) else "no devs")]
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
    elif matches == "rdevall":
        devlist = getDevsUsers()
        for user in devlist:
            remDevUser(user.user_id)
            utilities.devs.remove(user.user_id)
        return [message.reply("done.")]
    return response


plugin = {
    "name": "dev users",
    "desc": "Make someone dev",
    "usage": [
        "[!/#]rdevall delete all devs that has been promoted.",
        "[!/#]getDevs get all devs users in bot.",
        "[!/#]dev in reply to message to dev a user.",
        "[!/#]rdev in reply to message to undev a user.",
        "[!/#]dev <id or username> to dev a user by id/username.",
        "[!/#]rdev <id or username> to undev a user by id/username.",
    ],
    "run": run,
    "sudo": True,
    "patterns": [
        "^[!/#](rdevall)$",
        "^[!/#](getDevs)",
        "^[!/#](dev)$",
        "^[!/#](rdev)$",
        "^[!/#](dev) (.+)$",
        "^[!/#](rdev) (.+)$",
    ],
}
