import asyncio
import requests
import json


async def getScreen(url, mode):

    try:
        session = requests.session()
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
            # 'full': 'on',
            "cacheLimit": "1",
        }

        response = session.post(
            "https://www.screenshotmachine.com/capture.php", headers=headers, data=data
        )
        res = json.loads(response.content)["link"]
        response = session.get("https://www.screenshotmachine.com/%s" % (res))
        return response.content
    except Exception as e:
        print(str(e))
        return None


async def run(message, matches, chat_id, step, crons=None):
    msg = await message.reply("please wait....")
    img = await getScreen(matches[1], matches[0])
    if img is None:
        return [
            msg.edit("please check the terminal error happened!"),
        ]
    else:

        return [
            msg.delete(),
            message.reply(file=img, message="a screenshot of %s" % (matches[1])),
        ]


plugin = {
    "name": "screenshot",
    "desc": "Take a screenshot of a website.",
    "usage": ["[!/#]ws <tablet or phone or desktop> <url>"],
    "run": run,
    "sudo": True,
    "patterns": ["^[!/#]ws (tablet|phone|desktop) (.+)$"],
}
