import asyncio
from os.path import isfile, getsize
import os


async def run(message, matches, chat_id, step, crons=None):
    if message.out:
        message = await message.edit("Please wait...")
    else:
        message = await message.reply("Please wait...")
    response = []
    if isfile(matches):
        if os.stat(matches).st_size > 40000000:
            response.append(message.edit("File reach maximum size."))
        else:
            response.append(message.reply(file=matches))
            response.append(message.delete())
    else:
        response.append(message.edit("No file found with current name."))
    return response


plugin = {
    "name": "getFileServer",
    "desc": "Download file from server to Telegram.",
    "usage": ["[!/#]down <path or filename>"],
    "run": run,
    "sudo": True,
    "patterns": ["^[!/#]down (.+)$"],
}
