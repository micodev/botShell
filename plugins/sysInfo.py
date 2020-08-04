import asyncio
import re


async def run(message, matches, chat_id, step, crons=None):
    try:
        process = await asyncio.create_subprocess_shell(
            "free && mpstat",
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.STDOUT,
        )
        stdpout, stderr = await process.communicate()
        e = stderr
        if not e:
            e = "No Error"
        res = stdpout.decode("utf-8")

        if e == "No Error":
            regex = r"^Mem:\s+(\d+)\s+(\d+)\s+(\d+)(.*(all)\s+(\d+\.?\d*)\s.*)$"
            matches = re.findall(regex, res, re.MULTILINE | re.DOTALL)
            if len(matches) > 0:
                infos = list(matches[0])
                infos.pop(3)
                res = (
                    "**Total Memory** : %sMB\n**Used Memory** : %sMB\n**Free Memory** : %sMB\nCPU : %s\nMEM : %s"
                    % (
                        int(infos[0]) >> 10,
                        int(infos[1]) >> 10,
                        int(infos[2]) >> 10,
                        infos[4] + "%",
                        ("%.2f" % ((int(infos[1]) >> 10) / (int(infos[0]) >> 10)))
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
