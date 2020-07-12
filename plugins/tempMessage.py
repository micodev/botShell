import asyncio
from utilities import utilities


async def run(message, matches, chat_id, step, crons=None):
    response = []
    if not (message.out):
        message = await message.reply(matches)
    duration = "💔❤️❤️❤️💛💛💛💚💚💚"

    while duration != "":
        response.append(message.edit(matches + "\n———————————————\n" + duration))
        response.append(asyncio.sleep(1))
        duration = duration[:-1]
    response.append(message.delete())
    return response


plugin = {
    "name": "Temp Messages",
    "desc": "send msgs for a period of time.",
    "usage": ["[!/#]tm <text> to send message for a period of time."],
    "run": run,
    "sudo": True,
    "patterns": ["^[!/#]tm (.+)$"],
}

