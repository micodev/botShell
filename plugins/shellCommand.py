import asyncio
import io

loop = asyncio.get_event_loop()


async def subproc(message, cmd):

    try:
        process = await asyncio.subprocess.create_subprocess_shell(
            cmd, stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.STDOUT
        )
        res = ""
        data = await process.stdout.readline()
        while (data) != b"":
            line = data.decode("ascii").rstrip()
            data = await process.stdout.readline()
            res += line + "\n"
        _, stderr = await process.communicate()
        e = stderr
        if not e:
            e = "No Error"
        output = f"**QUERY:**\n__Command:__\n`{cmd}` \n__PID:__\n`{process.pid}`\n\n**stderr:** \n`{e}`\n**Output:**\n{res}"

        if len(output) > 4000:
            with io.BytesIO(str.encode(output)) as out_file:
                out_file.name = "exec.text"
                await message.reply(file=out_file)
            await message.delete()
        else:
            await message.edit(output)
        return output

    except Exception as e:
        print("Error : " + str(e))
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
