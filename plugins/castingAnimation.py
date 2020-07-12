import asyncio
from utilities import utilities
from collections import deque


async def run(message, matches, chat_id, step, crons=None):
    response = []
    if not (message.out):
        message = await message.reply(matches)
    response.append(message.edit(matches + "."))
    msg_total = deque([matches, "⠀⠀⁦⠀⁦", "⠀⠀⁦⠀⁦", "⠀⠀⁦⠀⁦", "⠀⠀⁦⠀⁦"])
    k = 0
    while k < 4:
        for i in range(0, len(msg_total)):
            msg_total.rotate(1)
            msg = "".join(str(x) + "\r\n" for x in msg_total)
            response.append(asyncio.sleep(0.3))
            response.append(message.edit(msg))
        k = k + 1
    response.append(message.edit(matches))
    return response


plugin = {
    "name": "message as casting",
    "desc": "send then cast content for a period of time.",
    "usage": ["[!/#]cast <text> to send then cast content for a period of time."],
    "run": run,
    "sudo": True,
    "patterns": ["^[!/#]cast (.+)$"],
}

