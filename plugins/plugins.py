import asyncio
import os
import re
from os.path import exists, join
from utilities import utilities


def stringify(plug):
    return (
        "name of plugin is : %s\ndescription : %s\nUsage of plugin :\n%susing by api/cli only ? %s\nIs used by owner of bot ? %s"
        % (
            plug["name"],
            plug["desc"],
            "".join((i + "\n") for i in plug["usage"]),
            ("api" if plug["bot"] else "cli") if "bot" in plug else "both",
            "yes" if plug["sudo"] else "no",
        )
    )


def add_plugin(plugin_name):
    if plugin_name in utilities.config["plugins"]:
        return "This plugin is already active"
    if not exists(join(utilities.WD, "plugins", plugin_name + ".py")):
        return "There is no file that name is " + plugin_name + " in plugins directory"
    utilities.config["plugins"].append(plugin_name)
    utilities.save_config()
    utilities.load_plugins()
    return (
        "Plugin "
        + plugin_name
        + " Enable Successfully\n"
        + stringify(utilities.load_plugin(plugin_name))
    )


def add_inactive_plugin():
    plugin_files = [
        files
        for files in os.listdir(join(utilities.WD, "plugins"))
        if re.search("^(.*)\.py$", files)
    ]
    plugins = []
    for plugin_file in plugin_files:
        plugin_file = plugin_file.replace(".py", "")
        if plugin_file == "__init__":
            continue
        if plugin_file not in utilities.config["plugins"]:
            plugins.append(plugin_file)
    for plugin_name in plugins:
        if plugin_name in utilities.config["plugins"]:
            return "This plugin is already active"
        if not exists(join(utilities.WD, "plugins", plugin_name + ".py")):
            return (
                "There is no file that name is " + plugin_name + " in plugins directory"
            )
        utilities.config["plugins"].append(plugin_name)
    utilities.save_config()
    utilities.load_plugins()
    return "Plugins activated successfully"


def remove_plugin(plugin_name):
    if plugin_name == "plugins":
        return "You Can not disable plugins plugin !! :|"
    if plugin_name not in utilities.config["plugins"]:
        return "This plugin is not active"
    utilities.config["plugins"].remove(plugin_name)
    utilities.save_config()
    utilities.load_plugins()
    return "Plugin " + plugin_name + " Disable Successfully"


def reload_plugin():
    utilities.load_plugins()
    return "Plugins Reloaded !"


def setlang(lang):
    utilities.config["lang"] = lang
    utilities.save_config()
    utilities.load_plugins()
    return "Lang set " + lang


def show_plugin():
    plugin_files = [
        files
        for files in os.listdir(join(utilities.WD, "plugins"))
        if re.search("^(.*)\.py$", files)
    ]
    show_string = "<b>Plugins List</b> \n\n"
    for plugin_file in plugin_files:
        plugin_file = plugin_file.replace(".py", "")
        if plugin_file == "__init__":
            continue
        if plugin_file in utilities.config["plugins"]:
            show_string += "✅ <b>" + plugin_file + "</b>\n"
        else:
            show_string += "❌ <b>" + plugin_file + "</b>\n"
    return show_string


async def run(message, matches, chat_id, step, crons=None):
    response = None
    if matches[1:] == "plugins":
        response = message.reply(show_plugin(), parse_mode="html")
    if matches[0] == "enable":
        response = message.reply(add_plugin(matches[1]))
    if matches[0] == "disable":
        response = message.reply(remove_plugin(matches[1]))
    if matches == "reload":
        response = message.reply(reload_plugin())
    if matches[0] == "setlang":
        response = message.reply(setlang(matches[1]))
    if matches == "enableAll":
        response = message.reply(add_inactive_plugin())
    return [response]


plugin = {
    "name": "Plugins",
    "desc": "Show the plugins",
    "run": run,
    "sudo": True,
    "patterns": [
        "^[!/#]plugins (enableAll)",
        "^[!/#]plugins (enable) (.+?)$",
        "^[!/#]plugins (disable) (.+?)$",
        "^[!/#]plugins (reload)$",
        "^[!/#]plugins$",
        "^[!/#](setlang) (.*)$",
    ],
}
