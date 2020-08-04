import asyncio
import subprocess
from subprocess import CalledProcessError
import os
import random

loop = asyncio.get_event_loop()


def shellquote(s):
    return "'" + s.replace("'", "'\\''") + "'"


async def getVoice(message, matches):
    tmp = await message.reply("Please wait...")
    export_file = (
        "tmp/"
        + str(message.sender_id)
        + str(random.randint(0, message.sender_id))
        + "voice.mp3"
    )
    text = matches[1].replace("\r\n", "").replace("\n", "")
    text = text.replace('"', '\\"').replace("'", "\\'")
    lang = "ar" if "a" in matches[0] else "en"
    cmd = (
        'gtts-cli "'
        + text
        + '" --lang='
        + lang
        + " --output "
        + export_file
        + " && ffmpeg  -y -i "
        + export_file
        + " -map 0:a -acodec:a libopus -b:a 100k -vbr on "
        + export_file.replace("mp3", "ogg")
    )
    process = await asyncio.create_subprocess_shell(
        cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT
    )

    stdout, stderr = await process.communicate()

    exitCode = process.returncode
    try:
        await tmp.delete()
        if exitCode == 0:
            await message.reply(file=export_file.replace("mp3", "ogg"))
        else:
            raise CalledProcessError(exitCode, cmd, output="k")
        os.remove(export_file)
        os.remove(export_file.replace("mp3", "ogg"))

        return None
    except CalledProcessError as e:
        os.remove(export_file)
        os.remove(export_file.replace("mp3", "ogg"))
        await tmp.reply(str(e.cmd) + " returns :\n" + e.stdout.decode("utf-8"))
        return None


async def run(msg, matches, chat_id, step, crons=None):

    if msg.is_reply and matches[0] == "tts":
        msg = await msg.get_reply_message()
        matche = []
        matche.append(matches[1])
        if msg.text:
            matche.append(msg.text)
        else:
            matche[0] = "e"
            matche.append("Please reply on text")
        matches = matche

    return [getVoice(msg, matches)]


plugin = {
    "name": "text to speech",
    "desc": "Voice from text maker.",
    "usage": ["[!/#]tts (a|e) <text> .", "[!/#]tts (a|e) reply to message."],
    "run": run,
    "sudo": True,
    "patterns": ["^[!/#]tts (a|e) (.+)$", "^[!/#](tts) (a|e)$"],
}
