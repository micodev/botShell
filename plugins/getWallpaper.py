import asyncio
from utilities import utilities
import urllib.parse
from requests_futures.sessions import FuturesSession
import json
import random

loop = asyncio.get_event_loop()
session = FuturesSession()


def hook_factory(*factory_args, **factory_kwargs):
    def first_response(resp, *args, **kwargs):
        try:
            message = factory_kwargs["message"]
            result = json.loads(resp.content)
            res = json.loads(resp.content.decode("utf-8"))
            if "photos" in res:
                photos = res["photos"]
                results = photos["results"]
                mode = factory_kwargs["mode"]
                if len(results) > 0:
                    item = random.randint(0, len(results))
                    if mode in results[item]["urls"]:
                        loop.create_task(
                            message.reply(file=results[item]["urls"][mode])
                        )
                        loop.create_task(message.delete())
                    else:
                        loop.create_task(message.edit("mode %s not found." % (mode)))
                else:
                    loop.create_task(message.edit("no images found"))
            else:
                loop.create_task(message.edit("no images found"))
            pass
        except Exception as e:
            print(str(e))
        return None

    return first_response


async def run(message, matches, chat_id, step, crons=None):
    try:
        if not (message.out):
            message = await message.reply(str("please wait...."))
        stri = urllib.parse.quote(matches[1])
        url = "https://unsplash.com/napi/search?query=%s&xp=&per_page=10&page=%s" % (
            stri,
            1,
        )
        session.get(
            url, hooks={"response": hook_factory(message=message, mode=matches[0])}
        )
    except Exception as e:
        print(e)

    return []


plugin = {
    "name": "wallpaper",
    "desc": "Get multi sizes wallpaper",
    "usage": ["[!/#]photo <raw or full or regular or small or thumb> <photo name>"],
    "run": run,
    "sudo": True,
    "patterns": ["^[!/#]photo (raw|full|regular|small|thumb) (.+)$"],
}
