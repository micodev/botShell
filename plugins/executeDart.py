from requests_futures.sessions import FuturesSession
import asyncio

loop = asyncio.get_event_loop()


def hook_factory(*factory_args, **factory_kwargs):
    def first_response(resp, *args, **kwargs):
        try:
            message = factory_kwargs["message"]
            cmd = factory_kwargs["cmd"]

            loop.create_task(
                message.edit(
                    "**exec:**\n```%s```\n**result:**\n```%s```"
                    % (
                        cmd,
                        resp.text.replace(
                            "<span style='line-height: 25px;color:#484848;'><b>$dart main.dart</b></span><br>",
                            "",
                        ),
                    )
                )
            )
        except Exception as e:
            print(str(e))

    return first_response


async def run(msg, matches, chat_id, step, crons=None):
    if not (msg.out):
        message = await msg.reply("Please, wait...")
    else:
        message = msg
    if msg.is_reply and matches == "dart":
        msg = await msg.get_reply_message()
        if msg.raw_text:
            cmd = msg.raw_text
        else:
            cmd = "print('Please, reply to text message.')"
    elif matches[0] == "dart":
        cmd = matches[1]
    else:
        return [message.delete()]
    session = FuturesSession()
    headers = {
        "Connection": "keep-alive",
        "Pragma": "no-cache",
        "Cache-Control": "no-cache",
        "Accept": "*/*",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.83 Safari/537.36",
        "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
        "Origin": "https://www.tutorialspoint.com",
        "Sec-Fetch-Site": "same-site",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Dest": "empty",
        "Referer": "https://www.tutorialspoint.com/execute_dart_online.php",
        "Accept-Language": "en,ar;q=0.9,en-GB;q=0.8",
    }
    data = {
        "lang": "dart",
        "code": cmd,
        "ext": "dart",
        "compile": "0",
        "execute": "dart main.dart",
        "mainfile": "main.dart",
        "uid": "7519096",
    }
    session.post(
        "https://tpcg.tutorialspoint.com/tpcg.php",
        headers=headers,
        data=data,
        hooks={"response": hook_factory(cmd=cmd, message=message)},
    )

    return []


plugin = {
    "name": "execute dart",
    "desc": "Test your dart code.",
    "usage": ["[!/#]dart <reply to message or pass it with>"],
    "run": run,
    "sudo": True,
    "patterns": ["^[!/#](dart) (.+)$", "^[!/#](dart)$"],
}

