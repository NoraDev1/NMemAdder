# import logging
# import os
# from pyrogram import Client,filters
# from pyrogram.types import Message
# import config
# from plugins.eval import remove_if_exists
# LOGS = logging.getLogger(__name__)

# @Client.on_message(filters.private & filters.command("get_logs"))
# async def Nsudos(client,message):
#     a = config.AUTH_USERS
#     if message.from_user.id not in a:
#         return
#     bot_log_path = f'logs.txt'
#     m_list = open(bot_log_path, "r").read()
#     message_s = m_list
#     await message.reply(m_list)