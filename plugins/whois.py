import asyncio
import json
from utilities import utilities
from telethon.tl.functions.users import GetFullUserRequest
from telethon.tl.functions.photos import GetUserPhotosRequest
import re


async def run(message, matches, chat_id, step, crons=None):
    if matches[0] == "wi":
        if re.match(r"@[a-zA-Z][\w\d]{3,30}[a-zA-Z\d]", matches[1]):
            user_id = (await utilities.client.get_entity(matches[1])).id
        else:
            user_id = int(matches[1])
    elif message.is_reply:
        msg = await message.get_reply_message()
        user_id = (
            msg.forward.from_id
            if (msg.forward and msg.forward.sender_id)
            else msg.sender_id
        )
    client = await utilities.client(GetFullUserRequest(user_id))

    user_profile_photos = await utilities.client(
        GetUserPhotosRequest(user_id=user_id, offset=42, max_id=0, limit=80)
    )
    replied_user_profile_photos_count = "NaN"
    try:
        replied_user_profile_photos_count = user_profile_photos.count
    except AttributeError as e:
        pass
    user_id = client.user.id
    first_name = utilities.markdown_escape(client.user.first_name)
    if first_name is not None:
        first_name = first_name.replace("\u2060", "")
    last_name = client.user.last_name
    if last_name is not None:
        last_name = utilities.markdown_escape(last_name)
        last_name = last_name.replace("\u2060", "")
    user_bio = client.about
    if user_bio is not None:
        user_bio = utilities.markdown_escape(client.about)
    common_chats = client.common_chats_count
    caption = """ID: `{}`
First Name: [{}](tg://user?id={})
Last Name: {}
Bio: {}
PhotoCounts: {}
Restricted: {}
Verified: {}
Bot: {}
Groups in Common: {}
""".format(
        user_id,
        first_name,
        user_id,
        last_name,
        user_bio,
        replied_user_profile_photos_count,
        client.user.restricted,
        client.user.verified,
        client.user.bot,
        common_chats,
    )
    return [message.reply(caption, file=client.profile_photo)]


plugin = {
    "name": "whois",
    "desc": "Show information about user.",
    "usage": ["[!/#]wi <reply or use username or id>"],
    "run": run,
    "sudo": True,
    "patterns": ["^[!/#]wi$", "^[!/#](wi) (.+)$",],
}
