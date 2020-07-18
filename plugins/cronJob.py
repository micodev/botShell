import asyncio
import os
import re
import datetime
from _datetime import timedelta
from utilities import utilities


async def run(message, matches, chat_id, step, crons=None):
    second = int(matches[0])
    text = matches[1]
    crons.append(
        {
            "chat_id": chat_id,
            "data": text,
            "time": (datetime.datetime.now() + timedelta(seconds=second)),
        }
    )
    return []


async def cron(data):
    return [utilities.client.send_message(data["chat_id"], data["data"])]


plugin = {
    "name": "cronjob",
    "desc": "send cron message",
    "run": run,
    "usage": ["/cron <seconds> <any string> to send cron job after period of time."],
    "cron": cron,
    "sudo": True,
    "patterns": ["^[#!/]cron ([0-9]+) (.+?)$"],
}
