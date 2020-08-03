import asyncio
import _thread
import requests
import urllib.parse
import re
from utilities import utilities

loop = asyncio.get_event_loop()


def getWord(word, msg, message):

    headers = {
        "Connection": "keep-alive",
        "Pragma": "no-cache",
        "Cache-Control": "no-cache",
        "Upgrade-Insecure-Requests": "1",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.105 Safari/537.36",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
        "Sec-Fetch-Site": "none",
        "Sec-Fetch-Mode": "navigate",
        "Sec-Fetch-User": "?1",
        "Sec-Fetch-Dest": "document",
        "Accept-Language": "en,ar;q=0.9,en-GB;q=0.8",
    }

    res = requests.get(
        "https://dictionary.cambridge.org/dictionary/english-arabic/"
        + urllib.parse.quote(word),
        headers=headers,
    )
    try:
        from bs4 import BeautifulSoup

        soup = BeautifulSoup(res.content, "html.parser")
        audios = soup.findAll(
            lambda tag: tag.name == "source"
            and "type" in tag.attrs
            and "ogg" in tag["type"]
        )
        prouniciation = soup.findAll(
            lambda tag: tag.name == "span"
            and "class" in tag.attrs
            and "ipa" in tag["class"]
        )
        for audio in audios:
            loop.create_task(
                utilities.client.send_file(
                    msg.chat_id, "https://dictionary.cambridge.org/%s" % (audio["src"]),
                )
            )
        result = "\nPronunciation:\nUK : %s\nUS : %s\nMain Meaning is : %s\nTranslated : %s\nExample : %s"
        main = soup.find(
            lambda tag: "class" in tag.attrs
            and "def-block ddef_block".split(" ") == tag["class"]
        )
        main_title = main.find(
            lambda tag: "class" in tag.attrs
            and "def ddef_d db".split(" ") == tag["class"]
        )
        main_tr = main.find(
            lambda tag: "class" in tag.attrs
            and "trans dtrans dtrans-se".split(" ") == tag["class"]
        )
        main_ex = main.find(
            lambda tag: "class" in tag.attrs
            and "examp dexamp".split(" ") == tag["class"]
        )
        result = result % (
            prouniciation[0].text if (len(prouniciation) > 0) else "Nan",
            prouniciation[1].text if (len(prouniciation) > 0) else "Nan",
            main_title.text if (main_title) else "Nan",
            main_tr.text.replace("  ", "").replace("\n", "") if (main_tr) else "Nan",
            main_ex.text if (main_ex) else "Nan",
        )

        # -----------------------------------------------#
        result += result + "\nAlternative Meaning :"
        conts = soup.findAll(
            lambda tag: "class" in tag.attrs
            and "phrase-block dphrase-block".split(" ") == tag["class"]
        )
        i = 1
        for p in conts:
            result += "\n%s - %s\nTranslated : %s\nExample : \n%s."
            phrase_body = p.find(
                lambda tag: "class" in tag.attrs
                and "def ddef_d db".split(" ") == tag["class"]
            )

            phrase_tr = p.find(
                lambda tag: "class" in tag.attrs
                and "trans dtrans dtrans-se".split(" ") == tag["class"]
            )
            phrase_ex = p.find(
                lambda tag: "class" in tag.attrs
                and "examp dexamp".split(" ") == tag["class"]
            )
            result = result % (
                i,
                phrase_body.text if (phrase_body) else "Nan",
                phrase_tr.text.replace("  ", "").replace("\n", "")
                if (phrase_tr)
                else "Nan",
                phrase_ex.text if (phrase_ex) else "Nan",
            )
            i += 1
        loop.create_task(message.edit(result))
    except Exception as e:
        print(str(e))
        loop.create_task(message.reply("try with another word please."))


async def run(msg, matches, chat_id, step, crons=None):
    response = []
    if matches[0] == "dict":
        if not (msg.out):
            message = await msg.reply("please wait..")
        else:
            message = msg
        _thread.start_new_thread(getWord, (matches[1], msg, message))

    return response


plugin = {
    "name": "word dictionary",
    "desc": "Get meaning of word with is spell and pronunciation.",
    "usage": ["[[!/#](dict)] <word> meaning of word with is spell and pronunciation.",],
    "run": run,
    "sudo": True,
    "patterns": ["^[!/#](dict) (.+)$"],
}

