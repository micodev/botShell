import asyncio
import subprocess
from subprocess import CalledProcessError

loop = asyncio.get_event_loop()


async def subproc(message, cmd):
    process = subprocess.Popen(
        cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT
    )
    output = process.communicate()[0]
    exitCode = process.returncode
    try:
        if exitCode == 0:
            await message.edit(output.decode("utf-8"))
            return output
        else:
            raise CalledProcessError(exitCode, cmd, output=output)
    except CalledProcessError as e:
        await message.edit(str(e.cmd) + " returns :\n" + e.stdout.decode("utf-8"))
        return None


async def run(message, matches, chat_id, step, crons=None):
    response = []
    if not (message.out):
        message = await message.reply("please wait..")
    command = matches
    loop.create_task(subproc(message, command))
    return response


plugin = {
    "name": "shell command",
    "desc": "Run your beautiful command using the bot and get output at runtime.",
    "usage": ["[!/#]tr <command>"],
    "run": run,
    "sudo": True,
    "patterns": ["^[!/#]tr (.+)$"],
}
