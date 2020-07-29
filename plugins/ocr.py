import asyncio
import json
from utilities import utilities
import os
import requests


async def ocr_get(msg, lang):

    try:
        file = await utilities.client.download_media(msg, lang)
        if file != None:
            file_data = None
            with open(file, "rb") as image_file:
                file_data = image_file.read()
            url = "https://api.ocr.space/parse/image"
            data = {
                "apikey": "5a64d478-9c89-43d8-88e3-c65de9999580",
                "language": lang,
            }
            if lang == "eng":
                data["OCREngine"] = 2
            os.remove(file)
            page = requests.post(url, data=data, files={file: file_data}, timeout=5,)

            return json.loads(page.content)["ParsedResults"][0]["ParsedText"]

        return "try again !"
    except Exception as e:
        return "try again !"


async def run(message, matches, chat_id, step, crons=None):
    if message.is_reply:
        msg = await message.get_reply_message()
        lang = "eng" if matches == "e" else "ara"
        if msg.photo:
            strin = await ocr_get(msg, lang)
            return [message.reply(strin)]
        else:
            return [message.reply("reply to an Image message please !")]
    else:
        return [message.reply("reply to an Image message please !")]
    pass


plugin = {
    "name": "ocr",
    "desc": "Convert Image into Text",
    "usage": ["[!/#]ocr(a|e) (reply to photo message) a for arabic,e for english"],
    "run": run,
    "sudo": False,
    "patterns": ["^[!/#]ocr(a|e)$"],
}
