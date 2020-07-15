import asyncio
import utilities
from utilities import utilities
import youtube_dl
import os
import re


def youtube_url_validation(url):
    youtube_regex = (
        r"(https?://)?(www\.)?"
        "(youtube|youtu|youtube-nocookie)\.(com|be)/"
        "(watch\?v=|embed/|v/|.+\?v=)?([^&=%\?]{11})"
    )

    youtube_regex_match = re.match(youtube_regex, url)
    if youtube_regex_match:
        return True

    return False


async def run(message, matches, chat_id, step, crons=None):
    if message.is_reply:
        msg = await message.get_reply_message()
        if msg.text:
            if youtube_url_validation(msg.text):
                ydl_opts = {
                    "outtmpl": "tmp/%(id)s.%(ext)s",
                    "format": "bestaudio/best",
                    "postprocessors": [
                        {
                            "key": "FFmpegExtractAudio",
                            "preferredcodec": "mp3",
                            "preferredquality": "192",
                        }
                    ],
                }
                file = None
                m_sg = await message.reply("please wait...")
                try:
                    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
                        info_dict = ydl.extract_info(msg.text, download=True)
                        file = ydl.prepare_filename(info_dict)
                    if file != None:
                        await message.reply(
                            file=file.replace(".webm", ".mp3").replace("mp4", "mp3").replace(".m4a", ".mp3").
                        )
                        os.remove(file.replace(".webm", ".mp3").replace("mp4", "mp3").replace(".m4a", ".mp3"))
                        await m_sg.delete()
                except Exception as e:
                    await m_sg.edit("Error : " + str(e))

    return []


plugin = {
    "name": "youtube",
    "desc": "Download from youtube (reply to youtube url).",
    "usage": ["[!/#]yt \nReply to youtube url."],
    "run": run,
    "sudo": True,
    "patterns": ["^[!/#]yt$"],
}
