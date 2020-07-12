import asyncio
import json
from utilities import utilities

number = [
    "◼️◼️◼️◼️◼️◼️◼️◼️\n◼️◼️◼️◼️◼️◼️◼️◼️\n◼️◻️◻️◻️◻️◻️◻️◼️\n◼️◻️◻️◼️◼️◻️◻️◼️\n◼️◻️◻️◼️◼️◻️◻️◼️\n◼️◻️◻️◼️◼️◻️◻️◼️\n◼️◻️◻️◻️◻️◻️◻️◼️\n◼️◼️◼️◼️◼️◼️◼️◼️",
    "◼️◼️◼️◼️◼️◼️◼️◼️\n◼️◼️◼️◼️◼️◼️◼️◼️\n◼️◼️◻️◻️◻️◼️◼️◼️\n◼️◼️◼️◻️◻️◼️◼️◼️\n◼️◼️◼️◻️◻️◼️◼️◼️\n◼️◼️◼️◻️◻️◼️◼️◼️\n◼️◼️◼️◻️◻️◼️◼️◼️\n◼️◼️◼️◼️◼️◼️◼️◼️",
    "◼️◼️◼️◼️◼️◼️◼️◼️\n◼️◼️◼️◼️◼️◼️◼️◼️\n◼️◻️◻️◻️◻️◻️◻️◼️\n◼️◼️◼️◼️◼️◻️◻️◼️\n◼️◻️◻️◻️◻️◻️◻️◼️\n◼️◻️◻️◼️◼️◼️◼️◼️\n◼️◻️◻️◻️◻️◻️◻️◼️\n◼️◼️◼️◼️◼️◼️◼️◼️",
    "◼️◼️◼️◼️◼️◼️◼️◼️\n◼️◼️◼️◼️◼️◼️◼️◼️\n◼️◻️◻️◻️◻️◻️◻️◼️\n◼️◼️◼️◼️◼️◻️◻️◼️\n◼️◻️◻️◻️◻️◻️◻️◼️\n◼️◼️◼️◼️◼️◻️◻️◼️\n◼️◻️◻️◻️◻️◻️◻️◼️\n◼️◼️◼️◼️◼️◼️◼️◼️",
]


async def run(message, matches, chat_id, step, crons=None):
    if not (message.out):
        message = await message.reply(matches)
    if matches != None:
        length = int(matches)
        if length % 2 != 0:
            length = length + 1
        total = length
        arr = [["◻️" for i in range(length)] for j in range(length)]
        parts = int((length) / 2)  # 4 ,0 \ 2 , 0
        k = -1
        v = -1
        if total == 8:
            for num in reversed(number):
                await message.edit(num)
                await asyncio.sleep(1)
        for part in range(1, parts + 1):
            k = k + 1
            v = v + 1
            kk = k
            vv = v
            step = 1
            moves = length * 4 - 4
            for i in range(1, moves + 1):
                arr[k][v] = "◼️"
                strr = ""
                for hor in range(0, total):
                    for ver in range(0, total):
                        strr = strr + arr[hor][ver]
                    strr = strr + "\n"
                # print(str)
                await message.edit(strr)
                await asyncio.sleep(1)
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

            length = int(length - 2)

    pass


plugin = {
    "name": "Square snake",
    "desc": "Snake square moving.",
    "usage": ["[!/#]snake <number>"],
    "run": run,
    "sudo": True,
    "patterns": ["^[!/#]snake (.*)$"],
}
