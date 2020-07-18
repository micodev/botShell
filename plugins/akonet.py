import asyncio
from utilities import utilities
from requests_futures.sessions import FuturesSession
import json

loop = asyncio.get_event_loop()


def hook_factory(*factory_args, **factory_kwargs):
    def first_response(resp, *args, **kwargs):
        try:
            message = factory_kwargs["message"]
            from_id = factory_kwargs["from_id"]
            utilities.user_steps[from_id] = {"name": "akonet", "step": 1, "data": []}
            utilities.user_steps[from_id]["data"] = json.loads(resp.content)
            res = ""
            j = 0
            for i in utilities.user_steps[from_id]["data"]:
                res = res + "/akonet_%s for %s" % (j, i["name"]) + "\n"
                j = j + 1
            loop.create_task(message.edit(res))
        except Exception as e:
            print(str(e))

    return first_response


async def run(message, matches, chat_id, step, crons=None):
    from_id = message.sender_id
    if not (message.out) and step == 0:
        message = await message.reply("Please wait..")
    if matches == "cancel":
        if from_id in utilities.user_steps:
            del utilities.user_steps[from_id]
            return [message.reply("Canceling successfully !")]
        else:
            return [message.reply("nothing to cancel !")]
    elif matches == "akonet":
        if step == 0:
            session = FuturesSession()
            response = session.get(
                "http://www.akonet.info/index.php/index",
                hooks={"response": hook_factory(message=message, from_id=from_id)},
            )
        else:
            return []
    elif step == 1:
        info = utilities.user_steps[from_id]["data"][int(matches[0])]
        img = "http://www.akonet.info/images/isp/" + info["logo"]
        messge = "name : %s\nstatus : %s\nping : %s\nloss : %s" % (
            info["name"],
            "up" if info["status"] else "down",
            info["ping"],
            info["loss"] + "%",
        )
        return [message.reply(file=img, message=messge)]
    else:
        return [message.edit("please send `/akonet`")]
    return []


plugin = {
    "name": "akonet",
    "desc": "Get net status from isp in Iraq.",
    "usage": [
        "[!/#]akonet to get whole list of isp.",
        "[!/#]akonet_<id of isp> to get info about specific isp.",
        "[/!#]cancel to cancel operation.",
    ],
    "run": run,
    "sudo": True,
    "patterns": ["^[!/#](akonet)$", "^[/!#]akonet_(\d+)(@.+)?$", "^[/!#](cancel)"],
}
