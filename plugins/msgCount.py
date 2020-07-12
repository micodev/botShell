import asyncio
from utilities import utilities


async def run(msg, matches, chat_id, step, crons=None):
    if not msg.is_reply:
        return [msg.reply("this command used in reply to user message..")]
    if not (msg.out):
        message = await msg.reply("please wait...")
    chat = msg.chat_id
    client_from_msg = await utilities.client.get_messages(chat, ids=msg.reply_to_msg_id)
    message_id = 0
    count = 0
    await message.edit("جاري الحساب ... " + str(0))
    i = 1
    j = 1
    messages_get = {}
    while True:
        messages = await utilities.client.get_messages(
            chat, limit=300, offset_id=message_id, from_user=client_from_msg.sender_id,
        )
        for x in messages:
            if j not in messages_get:
                messages_get[j] = []
            messages_get[j].append(x.id)

            if len(messages_get[j]) % 100 == 0:
                j = j + 1
        count = count + len(messages)

        if len(messages) == 0:
            break
        await message.edit("جاري الحساب ... " + str(count * i))
        message1 = messages[len(messages) - 1]
        message_id = message1.id
    await message.edit("عدد الرسائل الكلي : " + str(count))

    return []


plugin = {
    "name": "message count",
    "desc": "Get actual user's message count",
    "usage": ["[!/#]msgs (in reply to message)"],
    "run": run,
    "sudo": True,
    "bot": False,
    "patterns": ["^[!/#]msgs$"],
}
