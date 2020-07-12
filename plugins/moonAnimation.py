import asyncio
from utilities import utilities


async def run(message, matches, chat_id, step, crons=None):
    response = []
    if not (message.out):
        message = await message.reply(matches)
    moon = ["🌑", "🌒", "🌓", "🌔", "🌕", "🌖", "🌗", "🌘"]
    for j in range(0, 60):
        res = ""
        first = moon[0]
        for i in range(1, len(moon)):
            moon[i - 1] = moon[i]
            res = res + moon[i]
        moon[7] = first
        res = res + first
        response.append(message.edit(res))
        response.append(asyncio.sleep(0.25))
    return response


plugin = {
    "name": "moon animation",
    "desc": "Edit message with moon phases.",
    "usage": ["[!/#]moon"],
    "run": run,
    "sudo": True,
    "patterns": ["^[!/#]moon$"],
}
