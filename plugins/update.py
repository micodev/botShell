import asyncio
import subprocess
import os
import sys
from utilities import utilities


def runGitPull():
    p = subprocess.Popen(
        "git pull", stdout=subprocess.PIPE, stderr=subprocess.STDOUT, shell=True
    )
    return iter(p.stdout.readline, b"")


def restartBot():
    p = subprocess.call("bash run.sh", shell=True)


async def run(message, matches, chat_id, step, crons=None):
    upd = ""
    utilities.config = utilities.get_config()
    utilities.config["updateChat"] = message.chat_id
    utilities.save_config()
    for line in runGitPull():
        upd = upd + line.decode("utf-8")
    if "Already" in upd:
        return [message.reply("The source is up to date.")]
    else:
        await message.reply(
            "The source has been updated,the bot will restart please wait."
        )
        restartBot()
    return []


plugin = {
    "name": "update",
    "desc": "Update the bot from source",
    "usage": ["[!/#]update update bot from internal."],
    "run": run,
    "sudo": True,
    "patterns": ["^[!/#]update$"],
}
