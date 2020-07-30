import asyncio
from utilities import utilities
from requests_futures.sessions import FuturesSession
import requests
import re
import json
import time
import youtube_dl

loop = asyncio.get_event_loop()
session = FuturesSession()


def youtube_url_validation(url):
    youtube_regex = (
        r"(https?://)?(www\.)?"
        "(youtube|youtu|youtube-nocookie)\.(com|be)/"
        "(watch\?v=|embed/|v/|.+\?v=)?([^&=%\?]{11})"
    )

    youtube_regex_match = re.match(youtube_regex, url)
    if youtube_regex_match:
        return youtube_regex_match
    return None


def downloaded_file(*factory_args, **factory_kwargs):
    def last_response(resp, *args, **kwargs):
        try:

            async def sendMessage(msg, file):
                await msg.reply(file=file)
                await msg.delete()
                return

            msg = factory_kwargs["tp"]
            loop.create_task(sendMessage(msg, resp.content))

        except Exception as e:
            print(str(e))
        pass

    return last_response


async def sendFileComplete(msg, m):
    try:
        await utilities.client.send_file(msg.chat_id, m[0])
    except Exception as e:
        print(str(e))
        await msg.reply("Error Occured Try again .")


def hook_factory(*factory_args, **factory_kwargs):
    tmp_msg = []

    async def callback(msg):
        tmp_msg.append(await msg.reply("Take A While."))

    def first_response(resp, *args, **kwargs):
        try:
            msg = factory_kwargs["msg"]
            message = factory_kwargs["message"]
            v_id = factory_kwargs["id"]
            url = factory_kwargs["url"]
            result = json.loads(resp.content)
            res = result["result"].replace("\r\n", "").replace("\\", " ")
            m = re.findall("_id: '(.*)',.+?v_id", res, re.IGNORECASE)

            if len(m) > 0:
                file_url = True
                cookies_temp = None
                while file_url:
                    req = requests.post(
                        "https://mate01.y2mate.com/en23/convert",
                        data={
                            "type": " youtube",
                            "_id": m[0],
                            "v_id": v_id,
                            "fquality":"720p",
                            "ftype":"mp4",
                        },
                        cookies=cookies_temp,
                    )
                    cookies_temp = req.cookies
                    if req.text != None and req.text != "":
                        req_res = json.loads(req.content)
                        if "result" in req_res:
                            if (
                                "running"
                                not in req_res["result"]
                                .replace("\r\n", "")
                                .replace("\\", "")
                                .lower()
                            ):
                                file_url = False
                                m = re.findall(
                                    '<a href="(.*)" rel=',
                                    req_res["result"],
                                    re.IGNORECASE,
                                )
                                loop.create_task(sendFileComplete(msg, m))

                                if len(tmp_msg) > 0:
                                    loop.create_task(tmp_msg[0].delete())
                                return
                    if len(tmp_msg) == 0:
                        loop.create_task(callback(msg))
                        time.sleep(3)
                    elif len(tmp_msg) > 1:
                        for i in range(0, len(tm_msg) - 2):
                            print(i)
                            loop.create_task(tmp_msg[i].delete())

            else:
                loop.create_task(message.edit("Invalid YouTube url ."))
                return
            pass
        except Exception as e:
            print(str(e))
        return None

    return first_response


async def extract_info(url, msg):
    info = ""
    try:
        with youtube_dl.YoutubeDL() as ydl:
            info_dict = ydl.extract_info(url, download=False)
            info += "Title : " + info_dict["title"] + "\n"
            info += "Uploader : " + info_dict["uploader"] + "\n"
            info += "Channel url : " + info_dict["uploader_url"] + "\n"
    except Exception as e:
        info = "Error Fetching Video Information ."
    await msg.edit(info)


async def run(msg, matches, chat_id, step, crons=None):
    response = []

    if msg.is_reply:
        if not (msg.out):
            message = await msg.reply("Searching on YouTube.com...")
        else:
            message = msg
        msg = await msg.get_reply_message()
        if msg.text:
            valid = youtube_url_validation(msg.text)
            if valid is not None:
                id = valid.groups()[-1]
                loop.create_task(
                    extract_info("https://www.youtube.com/watch?v=" + id, message)
                )
                url = "https://mate01.y2mate.com/en23/analyze/ajax"
                data = {
                    "url": "https://www.youtube.com/watch?v=" + id,
                    "q_auto": 0,
                    "ajax": 1,
                }
                session.post(
                    url,
                    data=data,
                    hooks={
                        "response": hook_factory(
                            message=message, msg=msg, url=url, id=id
                        )
                    },
                )

    return response


plugin = {
    "name": "Youtube Video Downloader ",
    "desc": "Best Way To Download Youtube Video .",
    "usage": ["[!/#]video Reply To Massage That Contains Vaild Youtube Video url ."],
    "run": run,
    "sudo": True,
    "patterns": ["^[!/#]video$"],
}

