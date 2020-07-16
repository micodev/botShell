import asyncio
from utilities import utilities
import subprocess


def run_command(command):
    p = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    return iter(p.stdout.readline, b"")


async def run(message, matches, chat_id, step, crons=None):
    response = []
    if not (message.out):
        message = await message.reply("please wait..")
    sting = ""
    command = matches.split()
    for line in run_command(command):
        sting = sting + line.decode("utf-8")
        await message.edit(str(sting))
    return response


plugin = {
    "name": "shell command",
    "desc": "Run your beautiful command using the bot and get output at runtime.",
    "usage": ["[!/#]tr <command>"],
    "run": run,
    "sudo": True,
    "patterns": ["^[!/#]tr (.+)$"],
}
