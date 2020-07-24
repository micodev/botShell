import asyncio
from utilities import utilities
import urllib.parse
from requests_futures.sessions import FuturesSession
import random
import re

loop = asyncio.get_event_loop()
session = FuturesSession()
filters = {
    "any": "",
    "small": "filterui:imagesize-small",
    "medium": "filterui:imagesize-medium",
    "large": "filterui:imagesize-large",
    "xlarge": "filterui:imagesize-wallpaper",
}


def hook_factory(*factory_args, **factory_kwargs):
    def first_response(resp, *args, **kwargs):
        try:
            message = factory_kwargs["message"]
            response = resp.content
            html = response.decode("utf8")
            links = re.findall("murl&quot;:&quot;(.*?)&quot;", html)
            if len(links) > 0:
                item = random.randint(0, len(links) - 1)
                loop.create_task(message.reply(file=links[item]))
                loop.create_task(message.delete())
            else:
                loop.create_task(message.reply("No image exist."))
        except Exception as e:
            print(str(e))
        return None

    return first_response


async def run(message, matches, chat_id, step, crons=None):
    global filters
    try:
        if not (message.out):
            message = await message.reply(str("please wait...."))
        size = matches[0].lower()
        filter = filters[size]
        query = urllib.parse.quote_plus(matches[1])
        download_count = 0
        headers = {
            "User-Agent": "Mozilla/5.0 (X11; Fedora; Linux x86_64; rv:60.0) Gecko/20100101 Firefox/60.0"
        }
        limit = 30
        page_counter = 0
        adlt = "off"
        url = (
            "https://www.bing.com/images/async?q="
            + urllib.parse.quote_plus(query)
            + "&first="
            + str(page_counter)
            + "&count="
            + str(limit)
            + "&adlt="
            + adlt
            + "&qft="
            + filter
        )
        session.get(
            url, headers=headers, hooks={"response": hook_factory(message=message)}
        )
    except Exception as e:
        print(e)

    return []


plugin = {
    "name": "bing Search",
    "desc": "Get images from bing.com",
    "usage": ["[!/#]bing <any or small or medium or large or xlarge> <photo name>"],
    "run": run,
    "sudo": True,
    "patterns": ["^[!/#]bing (any|small|medium|large|xlarge) (.+)$"],
}
