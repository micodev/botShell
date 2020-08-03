import asyncio
from utilities import utilities
from requests_futures.sessions import FuturesSession
import urllib.parse
from urllib.parse import parse_qs
from bs4 import BeautifulSoup
import re
import json

loop = asyncio.get_event_loop()
session = FuturesSession()


def hook_factory(*factory_args, **factory_kwargs):
    def first_response(res, *args, **kwargs):
        try:
            word = factory_kwargs["word"]
            message = factory_kwargs["message"]
            if res.text:
                resp = json.loads(res.text)
                correction = resp["text"]

                if word == correction:
                    loop.create_task(message.edit("Your sentnece/word is correct."))
                    return None
                res = "Did you mean : \n" + correction + "\n"
                res += "**Corrections :**\n"
                j = 1
                for i in resp["corrections"]:
                    res += str(j) + "- correction type : " + i["type"] + "\n"
                    res += "Description : " + i["longDescription"] + "\n"
                    res += "The word : `%s` will be `%s`\n" % (
                        i["mistakeText"],
                        i["correctionText"],
                    )
                    j = j + 1
                loop.create_task(message.edit(res))
            return None
        except Exception as e:
            print(str(e))
            loop.create_task(message.edit("**ERROR** : \n" + str(e)))
            return None

    return first_response


async def run(msg, matches, chat_id, step, crons=None):
    if not (msg.out):
        message = await msg.reply("Please, wait...")
    else:
        message = msg
    if msg.is_reply:
        msg = await msg.get_reply_message()
        if msg.text:
            headers = {
                "authority": "orthographe.reverso.net",
                "pragma": "no-cache",
                "cache-control": "no-cache",
                "accept": "application/json, text/javascript, */*; q=0.01",
                "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.105 Safari/537.36",
                "content-type": "application/json",
                "origin": "https://www.reverso.net",
                "sec-fetch-site": "same-site",
                "sec-fetch-mode": "cors",
                "sec-fetch-dest": "empty",
                "referer": "https://www.reverso.net/spell-checker/english-spelling-grammar/",
                "accept-language": "en,ar;q=0.9,en-GB;q=0.8",
            }

            data = (
                '{"language":"eng","text": "'
                + msg.text
                + '","autoReplace":true,"interfaceLanguage":"en","locale":"Indifferent","origin":"interactive","generateSynonyms":false,"generateRecommendations":false,"getCorrectionDetails":true}'
            )

            session.post(
                "https://orthographe.reverso.net/api/v1/Spelling",
                headers=headers,
                data=data,
                hooks={"response": hook_factory(message=message, word=msg.text)},
            )
    return []


plugin = {
    "name": "spell check",
    "desc": "Use get more details of did you mean check",
    "usage": ["[!/#]spell2 (reply to message)"],
    "run": run,
    "sudo": True,
    "patterns": ["^[!/#](spell2)$"],
}
