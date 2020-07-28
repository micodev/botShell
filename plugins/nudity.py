import asyncio
import subprocess
from subprocess import CalledProcessError
import os
import random
import _thread
from utilities import utilities
from nudity import Nudity


def longLoading(loop, message, file):
    try:

        nudity = Nudity()
        if nudity.has(file):
            loop.create_task(message.edit("nude detected.."))
        else:
            loop.create_task(message.edit("no nude detected.."))
        if file != None:
            os.remove(file)
    except Exception as e:
        loop.create_task(message.edit(str(e)))
        if file != None:
            os.remove(file)


async def run(message, matches, chat_id, step, crons=None):

    if message.is_reply:
        msg = await message.get_reply_message()
        message = await message.reply("please wait....")
        if msg.photo:
            file = await utilities.client.download_media(msg)
            _thread.start_new_thread(
                longLoading, args=(asyncio.get_event_loop(), message, file)
            )
    return []


plugin = {
    "name": "text to speech",
    "desc": "Voice from text make",
    "usage": ["[!/#]tts (a|e) <text> .", "[!/#]tts (a|e) reply to message."],
    "run": run,
    "sudo": True,
    "patterns": ["^[!/#]nude$"],
}
