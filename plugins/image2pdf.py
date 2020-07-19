import asyncio
import json
import utilities
from utilities import utilities
import img2pdf
import os


async def Photo_to_pdf(event, imagelist):
    with open("tmp/" + str(event.sender_id) + ".pdf", "wb") as f:
        f.write(img2pdf.convert([i for i in imagelist]))
    return "tmp/" + str(event.sender_id) + ".pdf"


async def run(message, matches, chat_id, step, crons=None):
    from_id = message.sender_id
    if matches[1:] == "photo":
        utilities.user_steps[from_id] = {"name": "img2pdf", "step": 1, "data": []}
        text = "send images as album or separated .."
        return [message.reply(text)]
    if message.text[1:] == "pdf":
        if not (from_id in utilities.user_steps):
            utilities.user_steps[from_id] = {"name": "img2pdf", "step": 1, "data": []}
        if len(utilities.user_steps[from_id]["data"]) == 0:
            return [
                message.reply(
                    "send pictures first or send `/cancel` for canceling operation."
                )
            ]
        await message.reply("please wait..")
        output = await Photo_to_pdf(message, utilities.user_steps[from_id]["data"])
        if output != None:
            for i in utilities.user_steps[from_id]["data"]:
                os.remove(i)
            await message.reply(file=output)
            os.remove(output)
            del utilities.user_steps[from_id]
        return []
    elif step == 1:
        if len(utilities.user_steps[from_id]["data"]) == 20:
            await message.reply(
                "please send /pdf to convert to pdf file you reached the maximum value."
            )
            return []
        file = await utilities.client.download_media(message.photo, "tmp")
        utilities.user_steps[from_id]["data"].append(str(file))


plugin = {
    "name": "img2pdf",
    "desc": "Convert photos to pdf",
    "usage": [
        "[!/#]photo then send photo.",
        "[!/#]pdf it will convert photos to pdf.",
        "[!/#]cancel cancel the operation.",
    ],
    "run": run,
    "sudo": False,
    "patterns": ["^[!/#]photo$", "^__photo__$", "^[!/#]pdf$"],
}
