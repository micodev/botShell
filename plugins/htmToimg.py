import imgkit
import os
from PIL import Image

options = {"format": "png", "xvfb": ""}


async def run(message, matches, chat_id, step, crons=None):
    if message.is_reply:
        msg = await message.get_reply_message()
        if msg.text:
            file = "tmp/imgkit_" + str(message.sender_id) + ".png"
            html = "<meta charset='utf-8'>\n" + msg.text
            img = imgkit.from_string(html, file, options=options)
            image = Image.open(file)
            image.save(file, quality=40, optimize=True)
            await message.reply(file=file, force_document=True)
            os.remove(file)
            return []
        else:
            return [message.reply("reply to an text message please !")]
    else:
        return [message.reply("reply to an text message please !")]
    pass


plugin = {
    "name": "htmToimg",
    "desc": "Convert html to img",
    "usage": ["[/!#]html reply to a message to convert it to html as image"],
    "run": run,
    "sudo": False,
    "patterns": ["^[!/#]html$"],
}
