import asyncio
from utilities import utilities
import urllib.parse
import requests
import re
from bs4 import BeautifulSoup


async def get_qoute(msg):
    info = utilities.user_steps[msg.sender_id]["data"]
    try:
        url = "https://www.goodreads.com/quotes/tag/%s?page=%s" % (
            urllib.parse.quote_plus(info["query"]),
            str(info["pa_ge"]),
        )
        page = requests.get(url)
        soup = BeautifulSoup(page.content.decode("utf-8"), "html.parser")
        divs = soup.find_all("div", {"class": "quoteText"})
        for div in divs:
            for script in div.findAll(["script", "span", "br"]):
                script.replaceWith("")
            info["qoutes"].append(div.get_text().replace("\n", "  ").replace("―", " "))

        if len(info["qoutes"]) > 1:
            return msg.reply(
                "`"
                + info["qoutes"][info["iter"]]
                + "`"
                + "\nif you wanna skip this conversation press `/cancel`."
            )
        else:
            return msg.reply("no qoutes avail")
        return msg.reply("try again !")
    except Exception as e:
        return msg.reply("try again ! : " + str(e))
    # pagination = tree.xpath(
    #     "//div[@class='leftContainer']/div[@style='float: right;']/div/a"
    # )
    # paginate = []
    # for e in pagination:
    #     if re.match("(\d+)", e.text):
    #         paginate.append(e.text)
    # res = [paginate[0], paginate[-1]]
    # print(res)


async def run(message, matches, chat_id, step, crons=None):
    from_id = message.sender_id
    if matches == "nqoute" and step == 1:
        if from_id in utilities.user_steps:
            if "data" in utilities.user_steps[from_id]:
                info = utilities.user_steps[from_id]["data"]
                print(len(info["qoutes"]))
                if len(info["qoutes"]) == 0:
                    return [message.reply("no qoutes avail")]
                elif len(info["qoutes"]) == (info["iter"] + 1):
                    return [
                        message.reply(
                            "no qoutes in current page press `/qpage "
                            + str(info["pa_ge"] + 1)
                            + "`"
                        )
                    ]
                info["iter"] = info["iter"] + 1
                return [
                    message.reply(
                        "`"
                        + info["qoutes"][info["iter"]]
                        + "`"
                        + "\nif you wanna skip this conversation press `/cancel`."
                    )
                ]
    elif matches[0] == "qoute":
        if step == 0:
            utilities.user_steps[from_id] = {
                "name": "qoute",
                "step": 1,
                "data": {"pa_ge": 1, "qoutes": [], "iter": 0, "query": matches[1]},
            }

        else:
            utilities.user_steps[from_id] = {
                "name": "qoute",
                "step": 1,
                "data": {"pa_ge": 1, "qoutes": [], "iter": 0, "query": matches[1]},
            }
        return [await get_qoute(message)]
    elif matches[0] == "qpage":
        if step > 0:
            utilities.user_steps[from_id]["data"]["pa_ge"] = int(matches[1])
            utilities.user_steps[from_id]["data"]["qoutes"] = []
            utilities.user_steps[from_id]["data"]["iter"] = 1
            return [await get_qoute(message)]
    elif matches == "cancel":
        if from_id in utilities.user_steps:
            del utilities.user_steps[from_id]
            return [message.reply("Canceling successfully !")]
        else:
            return [message.reply("nothing to cancel !")]
    elif from_id in utilities.user_steps:
        return [
            message.reply(
                "there is a conversation available right now if you want to canceling it please press /cancel"
            )
        ]


plugin = {
    "name": "qoute",
    "desc": "get qoutes from internet by tag.",
    "usage": [
        "[!/#]qoute <any tag qoute name> .",
        "[!/#]nqoute for next qoute.",
        "[!/#]qpage <number> to load another list of qoutes if avail.",
        "[!/#]cancel to cancel the operation",
    ],
    "run": run,
    "sudo": True,
    "patterns": [
        "^[!/#](qoute) (.+)$",
        "^[!/#](nqoute)$",
        "^[!/#](qpage) (.+)$",
        "^[/#!](cancel)$",
    ],
}
