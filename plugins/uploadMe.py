import asyncio
import subprocess
import os
from utilities import utilities


async def downloadFile(msg):
    file_msg = msg.file
    print(file_msg.ext)
    if file_msg.ext == ".py":
        if os.path.isfile("plugins/%s" % ((file_msg.name))):
            return "There is already file with this name please rename it."
        file = await msg.download_media("tmp")
        try:
            values = {}
            with open(file, encoding="utf-8") as f:
                code = compile(f.read(), file, "exec")
                exec(code, values)
                f.close()
            os.replace(file, file.replace("tmp", "plugins"))
            return "Done added to Plugins send `/plugins enable %s` to enable it" % (
                file_msg.name.replace(".py", "")
            )
        except Exception as e:
            os.remove(file)
            return str(e)
    else:
        return "reply on python file dude."


async def run(message, matches, chat_id, step, crons=None):
    response = []
    print(matches)
    if matches == "up":
        if message.is_reply:
            msg = await message.get_reply_message()
            if msg.file:
                strin = await downloadFile(msg)
                return [message.reply(strin)]
            else:
                return [message.reply("reply to an File please !")]
        else:
            return [message.reply("reply to an File please !")]
        pass
        return response
    elif matches[0] == "del":
        plugin = matches[1]
        if os.path.isfile("plugins/%s" % ((plugin + ".py"))):
            print(plugin)
            if plugin in utilities.config["plugins"]:
                utilities.config["plugins"].remove(plugin)
                utilities.save_config()
                utilities.load_plugins()
            os.remove("plugins/%s" % ((plugin + ".py")))
            return [message.reply("plugin has been deleted.")]
        else:
            return [message.reply("no plugin found with this name.")]


plugin = {
    "name": "uploadMe",
    "desc": "Upload your plugins from anywhere in bot by reply to msg.",
    "usage": [
        "[!/#]up (reply to python plugin file).",
        "[!/#]]del <plugin name> to delete plugin that in plugins folder.",
    ],
    "run": run,
    "sudo": True,
    "patterns": ["^[!/#](up)$", "^[!/#](del) (.+)$"],
}
