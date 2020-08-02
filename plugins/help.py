import asyncio
from os.path import join
import os
import re
from utilities import utilities


def getallUsage(name=None):
    response_text = ""

    plugin_files = [name]
    if name == None:
        plugin_files = [
            files
            for files in os.listdir(join(utilities.WD, "plugins"))
            if re.search("^(.*)\.py$", files)
        ]
    msgs = []
    for plugin_file in plugin_files:
        plugin_file = plugin_file.replace(".py", "")
        if plugin_file == "__init__":
            continue
        if plugin_file in utilities.config["plugins"]:
            plugin = utilities.load_plugin(plugin_file)
            if "usage" in plugin:
                response_text += (
                    "ℹ️ "
                    + plugin["name"]
                    + "'s usage :\n"
                    + "".join(((i + "\n")) for i in plugin["usage"])
                    + "\n"
                    + ("" if name == None else "Description : " + plugin["desc"])
                )
            else:
                response_text += (
                    "ℹ️ "
                    + plugin["name"]
                    + "'s patterns :\n"
                    + "".join((i + "\n") for i in plugin["patterns"])
                    + "\n"
                )
            if len(response_text) > 3500:
                msgs.append(response_text)
                response_text = ""
    if len(response_text) > 0:
        msgs.append(response_text)
    return msgs if (len(msgs) > 0) else "no such a plugin"


async def run(message, matches, chat_id, step, crons=None):
    response = []
    if matches[1:] == "help":
        for i in getallUsage():
            response.append(message.reply(i, parse_mode=None))
        return response
    else:
        for i in getallUsage(matches):
            response.append(message.reply(i, parse_mode=None))
        return response


plugin = {
    "name": "Help",
    "desc": "Show Help of plugins",
    "usage": ["`[!/#]help`", "`[!/#]help <plugin_file_name>`"],
    "run": run,
    "sudo": False,
    "patterns": ["^[!/#]help (.*)$", "^[!/#]help$",],
}
