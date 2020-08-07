import asyncio
import _thread
import requests
import urllib.parse
import re
from requests_futures.sessions import FuturesSession
from bs4 import BeautifulSoup
import json

loop = asyncio.get_event_loop()


def getMusic(id, msg, message):
    try:
        session = requests.session()
        getMainPage = session.get("https://savemp3.net")
        pageSoup = BeautifulSoup(getMainPage.content, "lxml")
        bearerToken = pageSoup.find(
            lambda tag: tag.name == "meta"
            and "name" in tag.attrs
            and tag.attrs["name"] == "mp3-token"
        )
        timeStamps = pageSoup.find(
            lambda tag: tag.name == "meta"
            and "name" in tag.attrs
            and tag.attrs["name"] == "timestamp"
        )
        headers = {
            "authority": "mp3.savevids.net",
            "pragma": "no-cache",
            "cache-control": "no-cache",
            "public-key": "2dedd6fc9b129a0d3b6b28b5735edf01",
            "accept": "application/json, text/plain, */*",
            "timestamp": "%s" % (timeStamps["content"]),
            "authorization": "Bearer %s" % (bearerToken["content"]),
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.105 Safari/537.36",
            "content-type": "application/json;charset=UTF-8",
            "origin": "https://savemp3.net",
            "sec-fetch-site": "cross-site",
            "sec-fetch-mode": "cors",
            "sec-fetch-dest": "empty",
            "referer": "https://savemp3.net/",
            "accept-language": "en,ar;q=0.9,en-GB;q=0.8",
        }
        data = '{"service":"youtube","videoId":"' + id + '"}'

        youtubeInformation = session.post(
            "https://mp3.savevids.net/api/web/info", headers=headers, data=data
        )
        info = json.loads(youtubeInformation.content)
        info_message = "title : %s\nauthor : %s" % (
            info["info"]["title"],
            info["info"]["author"],
        )
        url = info["info"]["downloads"][21]["url"]
        loop.create_task(message.reply(info_message, file=info["info"]["thumbnailUrl"]))
        data = {
            "service": "youtube",
            "videoId": info["info"]["id"],
            "title": info["info"]["title"],
            "url": url,
            "length": info["info"]["length"],
            "bitrate": 256,
            "start": 0,
            "end": info["info"]["length"],
        }
        downloadIdResponse = session.post(
            "https://mp3.savevids.net/api/web/download/request",
            headers=headers,
            data=json.dumps(data),
        )
        downloadId = json.loads(downloadIdResponse.content)

        mp3 = "https://mp3.savevids.net/api/web/download/%s" % (
            downloadId["downloadId"]
        )
        loop.create_task(message.reply(file=mp3))

    except Exception as e:
        print(str(e))
        loop.create_task(message.reply("Error: please try another time or use `/sfyt`"))


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
                    getMusic(search_results[0], message, msg)
                else:
                    loop.create_task(message.edit("not found."))
        except Exception as e:
            print(str(e))
        return None

    return first_response


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


async def run(msg, matches, chat_id, step, crons=None):
    response = []
    if matches[0] == "sfyt4":
        if not (msg.out):
            message = await msg.reply("please wait..")
        else:
            message = msg
        query_string = urllib.parse.urlencode({"search_query": str(matches[1])})
        sess = FuturesSession()
        sess.get(
            "http://www.youtube.com/results?" + query_string,
            hooks={"response": get_id(message=message, msg=msg)},
        )
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
                _thread.start_new_thread(getMusic, (id, msg, message))

    return response


plugin = {
    "name": "external youtube",
    "desc": "Fast way downloading audio from youtube.",
    "usage": [
        "[!/#]fyt4 reply on message has youtube url",
        "[!/#](sfyt4) <query> search about song get first result",
    ],
    "run": run,
    "sudo": True,
    "patterns": ["^[!/#]fyt4$", "^[!/#](sfyt4) (.+)$"],
}

