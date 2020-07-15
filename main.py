import os
from telethon import TelegramClient, events, Button, extensions, functions, types
from os.path import dirname, realpath, join
import re
import asyncio
import datetime
from utilities import utilities

loop = asyncio.get_event_loop()
utilities.client = None


def sort_key(p):
    return p["name"]


def run_client():
    utilities.config = utilities.get_config()
    config = utilities.config
    utilities.client = TelegramClient(
        "sessions_bot", config["api_id"], config["api_hash"], loop=loop
    )
    utilities.client.start()
    utilities.load_plugins()
    utilities.plugins.sort(key=sort_key)
    utilities.public_plugins.sort(key=sort_key)


run_client()


async def saveBotId():
    me = await utilities.client.get_me()
    utilities.config["bot_id"] = (me).id
    utilities.config["isbot"] = (me).bot
    utilities.save_config()


def check_sudo(chat_id):
    if chat_id in utilities.config["sudo_members"]:
        return True
    return False


def markdown_escape(text):
    text = text.replace("_", "\\_")
    text = text.replace("[", "\\{")
    text = text.replace("*", "\\*")
    text = text.replace("`", "\\`")
    return text


@utilities.client.on(events.ChatAction)
async def my_event_handler(event):

    try:
        if event.user_joined or event.user_added:
            from_user = event.added_by
            target_user = event.user
            plugins = utilities.plugins
            for plugin in plugins:
                if "added" not in plugin:
                    continue
                if "bot" in plugin and utilities.config["isbot"] != plugin["bot"]:
                    if plugin["bot"]:
                        await event.reply("for bot-api only")
                    else:
                        await event.reply("for bot-cli only")
                    return

                if plugin["sudo"]:
                    if check_sudo(event.sender_id):
                        return_values = await plugin["added"](
                            event,
                            event.chat_id,
                            0
                            if (target_user.id in utilities.user_steps)
                            else utilities.user_steps[target_user.id]["step"],
                            crons=utilities.crons,
                        )

                        for return_value in return_values:
                            if return_value:
                                await (return_value)
                    else:
                        await event.reply("for sudores")

                else:
                    return_values = await plugin["added"](
                        event,
                        event.chat_id,
                        0
                        if (target_user.id not in utilities.user_steps)
                        else utilities.user_steps[target_user.id]["step"],
                    )
                    if return_values:
                        for return_value in return_values:
                            await (return_value)
    except Exception as e:
        print("chat_handler : %s" % (e))


@utilities.client.on(events.NewMessage)
async def my_event_handler(event):
    plugins = utilities.plugins
    try:
        message = event.message
        chat_id = event.chat_id
        from_id = event.sender_id
        if from_id in utilities.user_steps:
            for plugin in plugins:
                if plugin["name"] == utilities.user_steps[from_id]["name"]:
                    for pattern in plugin["patterns"]:
                        if re.search(
                            pattern, event.raw_text, re.IGNORECASE | re.MULTILINE
                        ):
                            matches = re.findall(pattern, event.raw_text, re.IGNORECASE)
                            break
                        else:
                            matches = ["xxxxxxxxxx"]
                    if plugin["sudo"]:
                        if check_sudo(from_id):
                            return_values = await plugin["run"](
                                message,
                                matches[0],
                                chat_id,
                                utilities.user_steps[from_id]["step"],
                            )
                            for return_value in return_values:
                                if return_value:
                                    await (return_value)
                        else:
                            await event.reply("for sudores")
                    else:
                        return_values = await plugin["run"](
                            message,
                            matches[0],
                            chat_id,
                            utilities.user_steps[from_id]["step"],
                        )
                        if return_values:
                            for return_value in return_values:
                                await (return_value)
                    break
            return
        if message.text is not None:
            for plugin in plugins:
                for pattern in plugin["patterns"]:
                    if re.search(pattern, event.raw_text, re.IGNORECASE | re.MULTILINE):
                        if (
                            "bot" in plugin
                            and utilities.config["isbot"] != plugin["bot"]
                        ):
                            if plugin["bot"]:
                                await event.reply("for bot-api only")
                            else:
                                await event.reply("for bot-cli only")
                            return
                        matches = re.findall(pattern, event.raw_text, re.IGNORECASE)
                        if plugin["sudo"]:
                            if check_sudo(event.sender_id):
                                return_values = await plugin["run"](
                                    event, matches[0], chat_id, 0, crons=utilities.crons
                                )

                                for return_value in return_values:
                                    if return_value:
                                        await (return_value)
                            else:
                                await event.reply("for sudores")

                        else:
                            return_values = await plugin["run"](
                                event, matches[0], chat_id, 0, crons=utilities.crons
                            )
                            if return_values:
                                for return_value in return_values:
                                    await (return_value)
        if message.photo is not None:
            for plugin in plugins:
                for pattern in plugin["patterns"]:
                    if re.search(pattern, "__photo__", re.IGNORECASE | re.MULTILINE):
                        matches = re.findall(pattern, "__photo__", re.IGNORECASE)
                        if plugin["sudo"]:
                            if check_sudo(event.sender_id):
                                return_values = await plugin["run"](
                                    event, matches[0], chat_id, 0
                                )
                                for return_value in return_values:
                                    if return_value:
                                        await (return_value)
                            else:
                                await event.reply("for sudores")
                        else:
                            return_values = await plugin["run"](
                                event, matches[0], chat_id, 0
                            )
                            if return_values:
                                for return_value in return_values:
                                    await (return_value)

    except Exception as e:
        print(str(e))
        await event.reply("Error : " + str(e))


async def clock():
    while True:
        if len(utilities.crons) != 0:
            for data in utilities.crons:
                if data["time"] < datetime.datetime.now():
                    for plugin in utilities.plugins:
                        if "cron" in plugin:
                            return_values = await plugin["cron"](data)
                            for return_value in return_values:
                                if return_value:
                                    await (return_value)
                    utilities.crons.remove(data)
        await asyncio.sleep(1)


loop.create_task(clock())
loop.create_task(saveBotId())
utilities.client.run_until_disconnected()
