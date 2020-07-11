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
                    + "'s usage :\n\n"
                    + "".join(((i + "\n")) for i in plugin["usage"])
                    + "\n"
                )
            else:

                response_text += (
                    "ℹ️ "
                    + plugin["name"]
                    + "'s patterns :\n\n"
                    + "".join((i + "\n") for i in plugin["patterns"])
                    + "\n"
                )
    return response_text if (response_text != "") else "no such a plugin"



async def run(message, matches, chat_id, step, crons=None):
    if matches[1:] == "help":
        return [message.reply(getallUsage(), parse_mode=None)]
    else:
        return [message.reply(getallUsage(matches), parse_mode=None)]


plugin = {
    "name": "Help",
    "desc": "Show Help of plugins",
    "usage": ["`[!/#]help`", "`[!/#]help <plugin_file_name>`"],
    "run": run,
    "sudo": False,
    "patterns": ["^[!/#]help (.*)$", "^[!/#]help$",],
}
