import asyncio
import json
from utilities import utilities


async def run(message, matches, chat_id, step, crons=None):
    if not (message.out):
        message = await message.reply(matches)
    Responses = []
    if matches != None:
        text = matches.replace("\r", ".").replace("\n", ".").replace("\r\n", ".")
        sting = text.replace(" ", "．") + "．"
        for j in range(0, 4):
            for i in range(0, len(sting)):
                await message.edit(sting)
                await asyncio.sleep(0.2)
                sting = sting[len(sting) - 1] + sting[:-1]

        for j in range(0, 4):
            for i in range(0, len(sting)):
                await asyncio.sleep(0.2)
                await message.edit(sting)
                sting = sting[1:] + sting[0]
            j = j + 1
        await message.edit(sting)
    return []


plugin = {
    "name": "Marquee",
    "desc": "Edit messages repeatidly",
    "usage": ["[!/#]r <text>"],
    "run": run,
    "sudo": True,
    "patterns": ["^[!/#]r (.*)$"],
}
