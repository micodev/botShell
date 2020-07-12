import asyncio
from utilities import utilities


async def run(message, matches, chat_id, step, crons=None):
    if not (message.out):
        message = await message.reply(matches)
    Responses = []
    if matches != None:
        text = matches.replace("\r", " ").replace("\n", " ").replace("\r\n", " ")
        await message.edit("|")
        msg_to_send = ""
        for c in text:
            clip = "ㅤ"
            for i in range(0, 3):
                await message.edit(msg_to_send + clip)
                if clip == "|":
                    clip = "ㅤ"
                else:
                    clip = "|"
                await asyncio.sleep(0.1)
            msg_to_send = msg_to_send + c
            await message.edit(msg_to_send)
            await asyncio.sleep(0.3)
    pass


plugin = {
    "name": "auto Typing",
    "desc": "Edit messages like typing person",
    "usage": ["[!/#]t <text>"],
    "run": run,
    "sudo": True,
    "patterns": ["^[!/#]t (.*)$"],
}
