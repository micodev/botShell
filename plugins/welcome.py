import asyncio
from utilities import utilities
from Db.welcome_sql import getWelcomeSettings, addWelcomeSetting, remWelcomeSetting
from telethon import utils


async def added(event, chat_id, step):
    ws = getWelcomeSettings(chat_id)
    if ws:
        from_user = event.added_by
        target_user = event.user
        if ws.msg_type == "media":
            return [event.reply(file=ws.file_id, message=ws.msg_content)]
        else:
            return [event.reply(ws.msg_content)]


async def run(message, matches, chat_id, step, crons=None):
    if matches[1:] == "sw":
        if message.is_reply:
            msg = await message.get_reply_message()
            if msg.media:
                file = await msg.download_media("tmp")
                addWelcomeSetting(chat_id, "media", msg.text, file)
            else:
                addWelcomeSetting(chat_id, "text", msg.text)
            return [message.reply("welcome message added successfully.")]
        else:
            return [message.reply("please if you may reply on a message.")]
    elif matches[1:] == "cw":
        ws = getWelcomeSettings(chat_id)
        if ws:
            remWelcomeSetting(chat_id)
            return [message.reply("welcome message cleared successfully..")]
        else:
            return [message.reply("no message to be cleared..")]


plugin = {
    "name": "welcome",
    "desc": "Show message when person joined.",
    "usage": [
        "[!/#]sw in reply to message to set welcome message.",
        "[!/#]cw to delete current welcome if exist.",
    ],
    "run": run,
    "added": added,
    "sudo": False,
    "patterns": ["^[!/#]sw$", "^[!/#]cw$"],
}
