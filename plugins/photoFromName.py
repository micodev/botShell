import asyncio
from utilities import utilities
import urllib
import requests
from lxml import html


async def run(message, matches, chat_id, step, crons=None):
    response = []
    if not (message.out):
        message = await message.reply("please wait ...")
    text = matches[1].replace("\n", " ").replace("\r\n", " ").replace(" ", " ")
    num = matches[0]
    headers = {
        "authority": "coolnames.online",
        "pragma": "no-cache",
        "cache-control": "no-cache",
        "accept": "*/*",
        "x-requested-with": "XMLHttpRequest",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36",
        "content-type": "application/x-www-form-urlencoded; charset=UTF-8",
        "origin": "https://coolnames.online",
        "sec-fetch-site": "same-origin",
        "sec-fetch-mode": "cors",
        "sec-fetch-dest": "empty",
        "referer": "https://coolnames.online/",
        "accept-language": "en,ar;q=0.9,en-GB;q=0.8",
    }

    data = {"name": text, "get": ""}

    page = requests.post(
        "https://coolnames.online/cool.php", headers=headers, data=data
    )
    page_text = page.content.decode("unicode-escape").encode("latin1").decode("utf-8")
    tree = html.fromstring(page_text)
    images = tree.xpath("//img/@src")
    response.append(message.reply(file=images[int(num)].replace(" ", "%20")))
    response.append(message.delete())
    return response


plugin = {
    "name": "photo from name",
    "desc": "generate photo from name from website.",
    "usage": ["[!/#]name <number 0-9><name> generate photo from name from website."],
    "run": run,
    "sudo": True,
    "patterns": ["^[!/#]name (\d) (.+)$"],
}
