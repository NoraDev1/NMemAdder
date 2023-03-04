import logging
import os
from tools.database import db
from pyrogram import Client, filters
import config
LOGS = logging.getLogger(__name__)

@Client.on_message(filters.command("fsub"))       
async def run_l(bt,m):
    if m.from_user.id not in config.AUTH_USERS:
        # await m.delete()
        return
    if len(m.command) == 1:
        await m.reply_text(
            f"Use this command to set into the botn\nUsage:\n\n`/fsub on|off`\n\nEg: `/fsub on`",
           
        )
        return
    fsub = (m.command[1])
    if fsub == "on":
        await db.set_fsub(True)
        await m.reply_text(f"successfully started fsub")
    elif fsub == "off":
        await db.set_fsub(False)
        await m.reply_text(f"successfully stopped fsub")
    else:
        await m.reply_text(
            f"Use this command to set into the botn\nUsage:\n\n`/fsub on|off`\n\nEg: `/fsub on`",
           
        )

@Client.on_message(filters.command("channel"))       
async def set_c(bt,m):
    if m.from_user.id not in config.AUTH_USERS:
        # await m.delete()
        return
    if len(m.command) == 1:
        await m.reply_text(
            f"Use this command to set fsub channel of the bot\n\nUsage:\n\n`/channel channel username or channel id with -100`\n\nEg: `/channel nrbots`",
           
        )
        return
    c = m.command[1]
    await db.set_fsub_channel(c)
    await m.reply_text(f"successfully set fsub channel to @{c}\n\nplease wait few seconds for update")



@Client.on_message(filters.command("b_copy"))       
async def run_l(bt,m):
    if m.from_user.id not in config.AUTH_USERS:
        # await m.delete()
        return
    if len(m.command) == 1:
        await m.reply_text(
            f"Use this command to set broadcast as copy\n\nUsage:\n\n`/b_copy on|off`\n\nEg: `/b_copy on`",
           
        )
        return
    fsub = (m.command[1])
    if fsub == "on":
        await db.set_bcopy(True)
        await m.reply_text(f"successfully set broadcast as copy")
    elif fsub == "off":
        await db.set_bcopy(False)
        await m.reply_text(f"successfully broadcast as forward")
    else:
        await m.reply_text(
            f"Use this command to set broadcast as copy\n\nUsage:\n\n`/b_copy on|off`\n\nEg: `/b_copy on`",
           
        )