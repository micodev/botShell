import asyncio
from utilities import utilities
from telethon.tl.types import ChannelParticipantsAdmins


async def run(message, matches, chat_id, step, crons=None):
    response = []
    header = "@admin: **Spam Found**"
    chat = message.chat_id
    i = 0
    counter = 0
    arr = []
    async for x in utilities.client.iter_participants(
        chat, filter=ChannelParticipantsAdmins
    ):
        if len(arr) < i + 1:
            arr.append(header)
        arr[i] = arr[i] + "[\u2063](tg://user?id=%s)" % (x.id)
        counter = counter + 1
        if (counter + 1) % 7 == 0:
            i = i + 1

    reply_message = None
    if message.is_reply:
        reply_message = await message.get_reply_message()
        for head in arr:
            nmsg = await reply_message.reply(head)
            if arr[0] != head:
                response.append(nmsg.delete())
    else:
        for head in arr:
            nmsg = await message.reply(head)
            if arr[0] != head:
                response.append(nmsg.delete())
    response.append(message.delete())
    return response


plugin = {
    "name": "tag Admins",
    "desc": "Tag all admins in group.",
    "usage": ["[!/#]tadmin Tag all admins in group."],
    "run": run,
    "sudo": True,
    "patterns": ["^[!/#]tadmin$"],
}

