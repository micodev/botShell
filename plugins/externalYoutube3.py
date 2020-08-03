import asyncio
import _thread
import requests
import urllib.parse
import re
from requests_futures.sessions import FuturesSession

loop = asyncio.get_event_loop()


def getMusic(id, msg, message):
    session = requests.Session()
    url = "https://mp3cyborg.com/"
    response = session.get(url)
    cookie = list(response.cookies)[0].value
    body = re.findall(
        '<input type="hidden" name="csrf_token" value="(.+)">', response.text
    )[0]
    headers = {
        "authority": "mp3cyborg.com",
        "pragma": "no-cache",
        "cache-control": "no-cache",
        "accept": "text/html-partial, */*; q=0.9",
        "x-requested-with": "XMLHttpRequest",
        "x-ic-request": "true",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.105 Safari/537.36",
        "x-http-method-override": "POST",
        "content-type": "application/x-www-form-urlencoded; charset=UTF-8",
        "origin": "https://mp3cyborg.com",
        "sec-fetch-site": "same-origin",
        "sec-fetch-mode": "cors",
        "sec-fetch-dest": "empty",
        "referer": "https://mp3cyborg.com/",
        "accept-language": "en,ar;q=0.9,en-GB;q=0.8",
        "cookie": "csrf_token=" + cookie,
    }

    data = {
        "ic-request": "true",
        "csrf_token": body,
        "url": "https://www.youtube.com/watch?v=" + id,
        "ic-id": "1",
        "ic-target-id": "url",
        "ic-current-url": "/",
        "_method": "POST",
    }

    response = session.post(
        "https://mp3cyborg.com/download-url", headers=headers, data=data
    )
    task = re.findall('<div ic-src="(.+)" ic-poll', response.text)
    url = (
        "https://mp3cyborg.com"
        + task[0]
        + "?ic-request=true&&ic-id=1&ic-target-id=url&ic-current-url=%2F&_method=GET"
    )
    task = []
    i = 0
    while len(task) <= 0 and i < 1000:
        i += 1
        response = session.get(url)
        res = response.text
        task = re.findall('<a class="btn download" href="(.+)" >', res)
    if len(task) == 0:
        loop.create_task(
            msg.reply("It takes long to convert please download another link.")
        )
    else:
        loop.create_task(msg.reply(file="https://mp3cyborg.com/" + task[0]))


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
    if matches[0] == "sfyt3":
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
        "[!/#]fyt3 reply on message has youtube url",
        "[!/#](sfyt3) <query> search about song get first result",
    ],
    "run": run,
    "sudo": True,
    "patterns": ["^[!/#]fyt3$", "^[!/#](sfyt3) (.+)$"],
}

