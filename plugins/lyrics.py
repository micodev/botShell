import asyncio
import json
import _thread
from utilities import utilities
import requests
import io
import urllib.parse
from bs4 import BeautifulSoup

loop = asyncio.get_event_loop()


def get_lyrics_result(query, msg, message):
    try:
        from_id = msg.sender_id
        headers = {
            "Connection": "keep-alive",
            "Pragma": "no-cache",
            "Cache-Control": "no-cache",
            "Accept": "application/json, text/javascript, */*; q=0.01",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.105 Safari/537.36",
            "Origin": "https://www.azlyrics.com",
            "Sec-Fetch-Site": "same-site",
            "Sec-Fetch-Mode": "cors",
            "Sec-Fetch-Dest": "empty",
            "Referer": "https://www.azlyrics.com/",
            "Accept-Language": "en,ar;q=0.9,en-GB;q=0.8",
        }

        params = {"q": query}
        response = requests.get(
            "https://search.azlyrics.com/suggest.php", headers=headers, params=params
        )
        js = json.loads(response.content)
        if len(js["songs"]) == 0:
            loop.create_task(message.edit("there is no soung with this name."))
            return None
        utilities.user_steps[from_id] = {
            "name": "lyrics",
            "step": 1,
            "data": js["songs"],
        }
        i = 1
        res = "send a number of the below songs:\n"
        for song in js["songs"]:
            res += f"`{i}` - " + song["autocomplete"] + "\n"
            i = i + 1
        loop.create_task(message.edit(res))
    except Exception as e:
        print(str(e))
        loop.create_task(message.edit("There was an error please use different name."))
    return None


def chunkstring(string, length):
    return (string[0 + i : length + i] for i in range(0, len(string), length))


# async def sendmsg(ch, msg):
#     for c in ch:
#         await msg.reply(c)


def get_lyrics(index, msg):
    from_id = msg.sender_id
    try:
        if int(index) <= 0:
            raise Exception("list index out of range")
        url = utilities.user_steps[from_id]["data"][int(index) - 1]["url"]
        rie = requests.get("https:" + url)

        soup = BeautifulSoup(rie.content.decode(), "html.parser")
        f = soup.find(
            lambda tag: tag.name == "div"
            and "class" in tag.attrs
            and "col-xs-12 col-lg-8 text-center".split() == tag["class"]
        )
        fc = f.find(
            lambda tag: tag.name == "div"
            and " Usage of azlyrics.com content by any third-party lyrics provider is prohibited by our licensing agreement. Sorry about that. "
            in tag.contents
        )
        if len(fc.text) >= 4096:
            # ch = chunkstring(fc.text, 4096)
            f = io.BytesIO(fc.text.encode())
            f.name = "lyrics.txt"
            loop.create_task(
                utilities.client.send_file(msg.chat_id, f, force_document=True)
            )

        else:
            loop.create_task(msg.reply(fc.text))
        del utilities.user_steps[from_id]
    except Exception as e:
        if str(e) == "list index out of range":
            loop.create_task(
                msg.reply(
                    "please, stick with 1-"
                    + str(len(utilities.user_steps[from_id]["data"]))
                )
            )
        else:
            loop.create_task(
                msg.reply(
                    "please, send `/cancel` to cancel conversation of `lyrics plugin`"
                )
            )
    return None


async def run(msg, matches, chat_id, step, crons=None):

    if matches[0] == "lyrics":
        if not (msg.out):
            message = await msg.reply("please wait..")
        else:
            message = msg
        _thread.start_new_thread(get_lyrics_result, (matches[1], msg, message))
    elif step == 1:
        _thread.start_new_thread(get_lyrics, (msg.text, msg))
    return []


plugin = {
    "name": "lyrics",
    "desc": "Show The lyrics of a music.",
    "usage": ["[!/#]lyrics <name of soung>"],
    "run": run,
    "sudo": True,
    "patterns": ["^[!/#](lyrics) (.+)$"],
}
