import asyncio
from requests_futures.sessions import FuturesSession
import json
import os

loop = asyncio.get_event_loop()


async def sendImage(message, file, url):
    await message.reply(
        file=file, message="a screenshot of %s" % (url), force_document=True
    )
    os.remove(file)


def hook_factory(*factory_args, **factory_kwargs):
    def first_response(resp, *args, **kwargs):
        try:
            message = factory_kwargs["message"]
            msg = factory_kwargs["msg"]
            session = factory_kwargs["session"]
            url = factory_kwargs["url"]
            if "link" in json.loads(resp.content):

                res = json.loads(resp.content)["link"]
                headers = {
                    "authority": "www.screenshotmachine.com",
                    "pragma": "no-cache",
                    "cache-control": "no-cache",
                    "accept": "*/*",
                    "x-requested-with": "XMLHttpRequest",
                    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.89 Safari/537.36",
                    "content-type": "application/x-www-form-urlencoded; charset=UTF-8",
                    "origin": "https://www.screenshotmachine.com",
                    "sec-fetch-site": "same-origin",
                    "sec-fetch-mode": "cors",
                    "sec-fetch-dest": "empty",
                    "referer": "https://www.screenshotmachine.com/",
                    "accept-language": "en,ar;q=0.9,en-GB;q=0.8",
                }
                response = session.get(
                    "https://www.screenshotmachine.com/%s" % (res),
                    headers=headers,
                    cookies=resp.cookies,
                )
                file = (
                    "tmp/" + (str(message.id) + "-" + str(message.sender_id)) + ".jpg"
                )
                r = response.result()
                if r.status_code == 200:
                    with open(file, "wb") as f:
                        for chunk in r:
                            f.write(chunk)
                loop.create_task(msg.delete())
                loop.create_task(sendImage(message, file, url))
                return None
            else:
                loop.create_task(msg.edit(json.loads(resp.content)["message"]),)
                return None
        except Exception as e:
            print(str(e))
            return None

    return first_response


async def getScreen(message, msg, url, mode):

    try:
        session = FuturesSession()
        headers = {
            "authority": "www.screenshotmachine.com",
            "pragma": "no-cache",
            "cache-control": "no-cache",
            "accept": "*/*",
            "x-requested-with": "XMLHttpRequest",
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.89 Safari/537.36",
            "content-type": "application/x-www-form-urlencoded; charset=UTF-8",
            "origin": "https://www.screenshotmachine.com",
            "sec-fetch-site": "same-origin",
            "sec-fetch-mode": "cors",
            "sec-fetch-dest": "empty",
            "referer": "https://www.screenshotmachine.com/",
            "accept-language": "en,ar;q=0.9,en-GB;q=0.8",
        }

        data = {
            "url": url,
            "device": mode,  # tablet , phone , desktop
            "full": "on",
            "cacheLimit": "1",
        }

        response = session.post(
            "https://www.screenshotmachine.com/capture.php",
            headers=headers,
            data=data,
            hooks={
                "response": hook_factory(
                    message=message, msg=msg, url=url, session=session
                ),
            },
        )
        return "Start processing..."
    except Exception as e:
        print(str(e))
        return None


async def run(message, matches, chat_id, step, crons=None):
    msg = await message.reply("please wait....")
    await getScreen(message, msg, matches[1], matches[0])
    return []


plugin = {
    "name": "screenshot",
    "desc": "Take a screenshot of a website.",
    "usage": ["[!/#]ws <tablet or phone or desktop> <url>"],
    "run": run,
    "sudo": True,
    "patterns": ["^[!/#]ws (tablet|phone|desktop) (.+)$"],
}
