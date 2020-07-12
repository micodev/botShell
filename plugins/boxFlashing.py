import asyncio
from utilities import utilities


async def run(message, matches, chat_id, step, crons=None):
    if not (message.out):
        message = await message.reply(matches)
    block = "◼️"
    length = int(matches[0])
    if length % 2 != 0:
        length = length + 1
    arr = [["◻️" for i in range(length)] for j in range(length)]
    for z in range(0, int(matches[1])):
        length = int(matches[0])
        if length % 2 != 0:
            length = length + 1
        total = length
        parts = int((length) / 2)  # 4 ,0 \ 2 , 0
        k = -1
        v = -1
        for part in range(1, parts + 1):
            k = k + 1
            v = v + 1
            kk = k
            vv = v
            step = 1
            moves = length * 4 - 4
            for i in range(1, moves + 1):
                arr[k][v] = block
                if step == 1:
                    v = v + 1
                elif step == 2:
                    k = k + 1
                elif step == 3:
                    v = v - 1
                elif step == 4:
                    k = k - 1
                if (
                    (i + 1 == length)
                    or (i + 1 == (2 * (length)) - 1)
                    or (i + 1 == (3 * (length)) - 2)
                ):
                    step = step + 1
            str = ""
            for hor in range(0, total):
                for ver in range(0, total):
                    str = str + arr[hor][ver]
                str = str + "\n"
            await message.edit(str)
            await asyncio.sleep(0.4)
            length = int(length - 2)
        block = "◼️" if block == "◻️" else "◻️"
    return []


plugin = {
    "name": "box flashing",
    "desc": "make flashing box by editing message.",
    "usage": ["[!/#]bf <length> <repeat count>"],
    "run": run,
    "sudo": True,
    "patterns": ["^[!/#]bf (\d) (\d+)$"],
}
