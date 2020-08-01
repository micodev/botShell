import asyncio
from utilities import utilities
from requests_futures.sessions import FuturesSession
from telethon.tl.types import DocumentAttributeAudio
import requests
import urllib.parse
import re
import json
import time
import youtube_dl
import io
import _thread

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


def get_url(id, msg, message, token, json_res):
    headers = {
        "authority": "mp3-youtube.download",
        "pragma": "no-cache",
        "cache-control": "no-cache",
        "accept": "application/json, text/plain, */*",
        "x-locale": "en",
        "x-token": token,
        "x-requested-with": "XMLHttpRequest",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.105 Safari/537.36",
        "sec-fetch-site": "same-origin",
        "sec-fetch-mode": "cors",
        "sec-fetch-dest": "empty",
        "referer": "https://mp3-youtube.download/en/online-audio-converter",
        "accept-language": "en,ar;q=0.9,en-GB;q=0.8",
    }
    while json_res["data"]["fileUrl"] == None and json_res["data"]["error"] == None:
        response = requests.get(
            "https://mp3-youtube.download/download/" + json_res["data"]["uuid"],
            headers=headers,
        )
        json_res = json.loads(response.text)
    if json_res["data"]["error"] != None:
        loop.create_task(message.edit(json_res["data"]["error"]))
        return
    loop.create_task(message.delete())
    loop.create_task(message.reply(file=json_res["data"]["fileUrl"]))


def fetch_token(*factory_args, **factory_kwargs):
    def first_response(resp, *args, **kwargs):
        try:
            id = factory_kwargs["id"]
            msg = factory_kwargs["msg"]
            message = factory_kwargs["message"]
            res = re.findall("var token = '(.+)'<\/script>", resp.text)
            token = res[0]
            headers = {
                "authority": "mp3-youtube.download",
                "pragma": "no-cache",
                "cache-control": "no-cache",
                "accept": "application/json, text/plain, */*",
                "x-locale": "en",
                "x-token": token,
                "x-requested-with": "XMLHttpRequest",
                "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.105 Safari/537.36",
                "content-type": "application/json;charset=UTF-8",
                "origin": "https://mp3-youtube.download",
                "sec-fetch-site": "same-origin",
                "sec-fetch-mode": "cors",
                "sec-fetch-dest": "empty",
                "referer": "https://mp3-youtube.download/en/online-audio-converter",
                "accept-language": "en,ar;q=0.9,en-GB;q=0.8",
            }
            data = (
                '{"url":"https://www.youtube.com/watch?v=%s"' % (id)
            ) + ',"extension":"mp3"}'
            session.post(
                "https://mp3-youtube.download/download/start",
                headers=headers,
                data=data,
                hooks={
                    "response": start_task(id=id, message=message, msg=msg, token=token)
                },
            )
        except Exception as e:
            print(str(e))
        return None

    return first_response


def start_task(*factory_args, **factory_kwargs):
    def first_response(resp, *args, **kwargs):
        id = factory_kwargs["id"]
        msg = factory_kwargs["msg"]
        message = factory_kwargs["message"]
        token = factory_kwargs["token"]
        json_res = json.loads(resp.text)
        _thread.start_new_thread(get_url, (id, msg, message, token, json_res))

    return first_response


def downloadProcess(id, message, msg):

    headers = {
        "authority": "mp3-youtube.download",
        "pragma": "no-cache",
        "cache-control": "no-cache",
        "upgrade-insecure-requests": "1",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.105 Safari/537.36",
        "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
        "sec-fetch-site": "none",
        "sec-fetch-mode": "navigate",
        "sec-fetch-user": "?1",
        "sec-fetch-dest": "document",
        "accept-language": "en,ar;q=0.9,en-GB;q=0.8",
    }

    session.get(
        "https://mp3-youtube.download/en/online-audio-converter",
        headers=headers,
        hooks={"response": fetch_token(id=id, message=message, msg=msg)},
    )


def get_id(*factory_args, **factory_kwargs):
    def first_response(html_content, *args, **kwargs):
        try:
            msg = factory_kwargs["msg"]
            message = factory_kwargs["message"]

            if html_content.text != "":
                loop.create_task(message.edit("searching for mp3 file..."))
                search_results = re.findall(
                    r"/watch\?v=(.{11})", html_content.content.decode()
                )
                if len(search_results) > 0:
                    loop.create_task(message.edit("start converting..."))
                    downloadProcess(search_results[0], message, msg)
                else:
                    loop.create_task(message.edit("not found."))
        except Exception as e:
            print(str(e))
        return None

    return first_response


async def run(msg, matches, chat_id, step, crons=None):
    response = []
    if matches[0] == "sfyt2":
        if not (msg.out):
            message = await msg.reply("please wait..")
        else:
            message = msg
        query_string = urllib.parse.urlencode({"search_query": str(matches[1])})
        session.get(
            "http://www.youtube.com/results?" + query_string,
            hooks={"response": get_id(message=message, msg=msg)},
        )
    elif msg.is_reply:
        if not (msg.out):
            message = await msg.reply("please wait..")
        else:
            message = msg
        msg = await msg.get_reply_message()
        if msg.text:
            valid = youtube_url_validation(msg.text)
            if valid is not None:
                id = valid.groups()[-1]
                downloadProcess(id, message, msg)
    return response


plugin = {
    "name": "external youtube",
    "desc": "Fast way downloading audio from youtube.",
    "usage": [
        "[!/#]fyt reply on message has youtube url",
        "[!/#](sfyt) <query> search about song get first result",
    ],
    "run": run,
    "sudo": True,
    "patterns": ["^[!/#]fyt2$", "^[!/#](sfyt2) (.+)$"],
}

