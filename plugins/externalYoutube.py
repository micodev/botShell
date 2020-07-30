import asyncio
from utilities import utilities
from requests_futures.sessions import FuturesSession
import requests
import re
import json
import time
import youtube_dl
import io

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


def download_big_data(*factory_args, **factory_kwargs):
    def download_fetch(resp, *args, **kwargs):
        try:
            msg = factory_kwargs["msg"]
            f = io.BytesIO(resp.content)
            f.name = "music.mp3"
            loop.create_task(utilities.client.send_file(msg.chat_id, f))
        except:
            loop.create_task(
                msg.reply("Please, download file from [Download](" + m[0] + ")")
            )

    return download_fetch


async def sendFileComplete(msg, m):
    try:
        await utilities.client.send_file(msg.chat_id, m[0])
    except Exception as e:
        if len(m) > 0:
            # await msg.reply("Please, download file from [Download](" + m[0] + ")")
            session.get(
                m[0], hooks={"response": download_big_data(msg=msg)},
            )
        else:
            await msg.reply("error please try again later !.")


def hook_factory(*factory_args, **factory_kwargs):
    tmp_msg = []

    async def callback(msg):
        tmp_msg.append(await msg.reply("take a while."))

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
                        "https://mate03.y2mate.com/mp3Convert",
                        data={
                            "type": " youtube",
                            "_id": m[0],
                            "v_id": v_id,
                            "mp3_type": " 128",
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
                loop.create_task(message.edit("error while fetching id..."))
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
    except Exception as e:
        info = "error while fetching."
    await msg.edit(info)


async def run(msg, matches, chat_id, step, crons=None):
    response = []

    if msg.is_reply:
        if not (msg.out):
            message = await msg.reply("please wait..")
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
                url = "https://mate03.y2mate.com/mp3/ajax"
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
    "name": "external youtube",
    "desc": "Fast way downloading audio from youtube.",
    "usage": ["[!/#]fyt reply on message has youtube url"],
    "run": run,
    "sudo": True,
    "patterns": ["^[!/#]fyt$"],
}

