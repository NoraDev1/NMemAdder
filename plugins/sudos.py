import logging
import os
from pyrogram import Client,filters
from pyrogram.types import Message
import config
from plugins.eval import remove_if_exists
LOGS = logging.getLogger(__name__)

@Client.on_message(filters.private & filters.command("sudos"))
async def Nsudos(client,message):
    a = config.AUTH_USERS
    if message.from_user.id not in a:
        return
    
    i = 0
    msg = ""
    for us in a:
        try:
            i = i+1
            u = await client.get_users(us)
            user = (
                    u.first_name if not u.mention else u.mention
                )
            msg += f"{i} 👤 {user} ( `{us}` )\n\n"
        except Exception:
            msg += f"{i} 👤 ~~Invalid User~~ ( `{us}` )\n\n"
            continue

    await message.reply(msg)


@Client.on_message(filters.private & filters.command("clear"))
async def clean(client,message):
    a = config.AUTH_USERS
    if message.from_user.id not in a:
        return
    bot_log_path = f'logs.txt'
    try:
        # remove_if_exists(bot_log_path)
        remove_if_exists("downloads")
        await message.reply_text('successfully cleared cached files !')
    except Exception as e:
        await message.reply_text('❌ no cache found !')
        LOGS.error(e)
    
        # if not os.path.exists(bot_log_path):
        #     await message.reply_text('❌ no cache found !')