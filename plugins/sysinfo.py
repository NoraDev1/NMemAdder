import os
import re
import uuid
import socket
import psutil
import platform

import requests

from config import AUTH_USERS

from tools.main import LOGS

from plugins.eval import remove_if_exists


from pyrogram import Client, filters
from pyrogram.types import Message

def humanbytes(size):
    """Convert Bytes To Bytes So That Human Can Read It"""
    if not size:
        return ""
    power = 2 ** 10
    raised_to_pow = 0
    dict_power_n = {0: "", 1: "Ki", 2: "Mi", 3: "Gi", 4: "Ti"}

    while size > power:
        size /= power
        raised_to_pow += 1
    return str(round(size, 2)) + " " + dict_power_n[raised_to_pow] + "B"


@Client.on_message(filters.command("sysinfo"))

async def fetch_system_information(client, message):
    if message.from_user.id not in AUTH_USERS:
        # await m.delete()
        return
    splatform = platform.system()
    platform_release = platform.release()
    platform_version = platform.version()
    architecture = platform.machine()
    hostname = socket.gethostname()
    ip_address = socket.gethostbyname(socket.gethostname())
    mac_address = ":".join(re.findall("..", "%012x" % uuid.getnode()))
    processor = platform.processor()
    ram = humanbytes(round(psutil.virtual_memory().total))
    cpu_freq = psutil.cpu_freq().current
    if cpu_freq >= 1000:
        cpu_freq = f"{round(cpu_freq / 1000, 2)}GHz"
    else:
        cpu_freq = f"{round(cpu_freq, 2)}MHz"
    du = psutil.disk_usage(client.workdir)
    psutil.disk_io_counters()
    disk = f"{humanbytes(du.used)} / {humanbytes(du.total)} " f"({du.percent}%)"
    cpu_len = len(psutil.Process().cpu_affinity())
    somsg = f"""🖥 **System Information**
    
**PlatForm :** `{splatform}`
**PlatForm - Release :** `{platform_release}`
**PlatForm - Version :** `{platform_version}`
**Architecture :** `{architecture}`
**HostName :** `{hostname}`
**IP :** `{ip_address}`
**Mac :** `{mac_address}`
**Processor :** `{processor}`
**Ram : ** `{ram}`
**CPU :** `{cpu_len}`
**CPU FREQ :** `{cpu_freq}`
**DISK :** `{disk}`
    """
    
    await message.reply(somsg)


@Client.on_message(filters.command("logs"))
async def get_bot_logs(c: Client, m: Message):
    if m.from_user.id not in AUTH_USERS:
        # await m.delete()
        return
    bot_log_path = f'logs.txt'
    if os.path.exists(bot_log_path):
        try:
            pablo = await m.reply_text("please wait....")
            m_list = open(bot_log_path, "r").read()
            message_s = m_list
            key = (
                requests.post("https://nekobin.com/api/documents", json={"content": message_s})
                .json()
                .get("result")
                .get("key")
            )
            url = f"https://nekobin.com/{key}"
            raw = f"https://nekobin.com/raw/{key}"
            reply_text = f"Here is the link of your logs.\n\nNekoBin [Click Here]({url})\n\nRaw [Click Here]({raw})"
            await pablo.edit(reply_text,disable_web_page_preview=True)
            # link = f"https://webshot.deam.io/{url}/?delay=2000"
            # await c.send_photo(m.chat.id, link, caption=f"Screenshort")
            await m.reply_document(
                bot_log_path,
                quote=True,
                caption= f'📁 this is the log of your bot',
            )
        except Exception as e:
            print(f'[ERROR]: {e}')
            LOGS.error(e)
    else:
        if not os.path.exists(bot_log_path):
            await m.reply_text('❌ no logs found !')