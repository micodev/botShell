import asyncio
from utilities import utilities


async def run(message, matches, chat_id, step, crons=None):
    response = []
    if not (message.out):
        message = await message.reply(matches)
    clocks = ["🕐", "🕑", "🕒", "🕓", "🕔", "🕕", "🕖", "🕗", "🕘", "🕙", "🕚", "🕛"]
    for j in range(0, 60):
        res = ""
        first = clocks[0]
        for i in range(1, 12):
            clocks[i - 1] = clocks[i]
            res = res + clocks[i]
        clocks[11] = first
        res = res + first
        response.append(message.edit(res))
        response.append(asyncio.sleep(0.25))
    return response


plugin = {
    "name": "clock animation",
    "desc": "Edit message with clock emoji phases.",
    "usage": ["[!/#]clock"],
    "run": run,
    "sudo": True,
    "patterns": ["^[!/#]clock$"],
}
