import asyncio
import re


async def run(message, matches, chat_id, step, crons=None):
    try:
        process = await asyncio.create_subprocess_shell(
            "top -n 1",
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.STDOUT,
        )
        stdpout, stderr = await process.communicate()
        e = stderr
        if not e:
            e = "No Error"
        res = stdpout.decode("utf-8").replace("(B", "").replace("=", "")
        ansi_escape = re.compile(r"\x1B(?:[@-Z\\-_]|\[[0-?]*[ -/]*[@-~])")
        sometext = res
        res = ansi_escape.sub("", sometext)
        res = res.replace("\x1b", "")
        print(res)
        if e == "No Error":
            regex = r"^.*up(.+),.*\d+\s*user[s]?.*,.*(\d+\.?\d+?)\s*us,.*Mem\s*:\s*(\d+)\s*total,\s*(\d+)\s*free,\s*(\d+)\s*used,.*$"
            matches = re.findall(regex, res, re.MULTILINE | re.DOTALL)
            if len(matches) > 0:
                infos = list(matches[0])
                res = (
                    "**Uptime** : %s\n**Total Memory** : %sMB\n**Used Memory** : %sMB\n**Free Memory** : %sMB\nCPU : %s\nMEM : %s"
                    % (
                        infos[0],
                        int(infos[2]) >> 10,
                        int(infos[3]) >> 10,
                        int(infos[4]) >> 10,
                        infos[1] + "%",
                        ("%.2f" % ((int(infos[3]) >> 10) / (int(infos[2]) >> 10) * 100))
                        + "%",
                    )
                )

        return [message.reply(res)]
    except Exception as e:
        return [
            message.reply(
                "There was an error when getting the information (check that mpstat is installed and your system is not termux.)"
            )
        ]


plugin = {
    "name": "sys info",
    "desc": "Get current system information.",
    "usage": ["[!/#]sys"],
    "run": run,
    "sudo": True,
    "patterns": ["^[!/#]sys$"],
}
