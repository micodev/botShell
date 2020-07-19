import asyncio
import json
from utilities import utilities
import os
import requests
from lxml import html
import re


def dump_string(x):

    text = """
    Title :{}
    \n""".format(
        x["title"]
    )
    links = x["links"]
    _link = ""
    f = 0
    for link in links:
        f = f + 1
        _link = _link + str(f) + " - " + link + "\n"
    return text + _link


async def book_get(msg):
    info = utilities.user_steps[msg.sender_id]["data"]
    try:

        url = (
            "http://gen.lib.rus.ec/search.php?&req="
            + info["query"]
            + "&phrase=1&view=simple&column=title&sort=year&sortmode=DESC&page="
            + str(info["pa_ge"])
        )
        page = requests.get(url)
        tree = html.fromstring(page.text)
        table = tree.xpath("//table")
        i = 0
        info["books"] = {}
        for ch in table[2]:
            obj = {}
            for c in ch:
                if not (len(c) < 1):
                    for a in c:
                        if not (a.text == None):
                            if a.text == "[edit]":
                                continue
                            if re.search("^\[[0-9]\]$", a.text):
                                if "links" not in obj:
                                    obj["links"] = []
                                obj["links"].append(a.get("href"))
                            else:
                                if "title" not in obj:
                                    obj["title"] = ""
                                obj["title"] = obj["title"] + " ," + a.text
            info["books"][i] = obj
            i = i + 1
        if len(info["books"]) > 1:
            sti = dump_string(info["books"][info["iter"]])
            return msg.reply(sti)
        else:
            return msg.reply("no books avail")
        return msg.reply("try again !")
    except Exception as e:
        return msg.reply("try again ! : " + str(e))


async def run(message, matches, chat_id, step, crons=None):
    from_id = message.sender_id
    print(matches)
    if matches == "nbook" and step == 1:
        if from_id in utilities.user_steps:
            if "data" in utilities.user_steps[from_id]:
                info = utilities.user_steps[from_id]["data"]
                print(len(info["books"]))
                if len(info["books"]) == 0:
                    return [message.reply("no books avail")]
                elif len(info["books"]) == (info["iter"] + 1):
                    return [
                        message.reply(
                            "no books in current page press `/page "
                            + str(info["pa_ge"] + 1)
                            + "`"
                        )
                    ]
                info["iter"] = info["iter"] + 1
                return [message.reply(dump_string(info["books"][info["iter"]]))]
    elif matches[0] == "book":
        if step == 0:
            utilities.user_steps[from_id] = {
                "name": "getbook",
                "step": 1,
                "data": {"pa_ge": 1, "books": {}, "iter": 1, "query": matches[1]},
            }

        else:
            utilities.user_steps[from_id] = {
                "name": "getbook",
                "step": 1,
                "data": {"pa_ge": 1, "books": {}, "iter": 1, "query": matches[1]},
            }
        return [await book_get(message)]
    elif matches[0] == "page":
        if step > 0:
            utilities.user_steps[from_id]["data"]["pa_ge"] = int(matches[1])
            utilities.user_steps[from_id]["data"]["books"] = {}
            utilities.user_steps[from_id]["data"]["iter"] = 1
            return [await book_get(message)]
    elif from_id in utilities.user_steps:
        return [
            message.reply(
                "there is a conversation available right now if you want to canceling it please press /cancel"
            )
        ]


plugin = {
    "name": "getbook",
    "desc": "get scientific books.",
    "usage": [
        "[!/#]book <any subject or book name (english only)> .",
        "[!/#]nbook for next book.",
        "[!/#]page <number> to load another list of book if avail.",
        "[!/#]cancel to cancel the operation",
    ],
    "run": run,
    "sudo": False,
    "patterns": ["^[!/#](book) (.+)$", "^[!/#](nbook)$", "^[!/#](page) (.+)$",],
}
