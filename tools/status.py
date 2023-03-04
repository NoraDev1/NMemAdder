import datetime

import config
import logging
from plugins.forcesubs import must_join_channel
from plugins.getme import getme
from tools.database import Database 



LOG_CHANNEL = config.LOG_CHANNEL
LOGS = logging.getLogger(__name__)

db = Database(config.DB_URL, config.DB_NAME)



async def handle_user_status(bot, cmd):
    chat_id = cmd.from_user.id
    if not await db.is_user_exist(chat_id):
        await db.add_user(chat_id)
        if LOG_CHANNEL:
            await bot.send_message(
                LOG_CHANNEL,
                f"#NEWUSER \n\nNew User Details : \n\nName : {cmd.from_user.first_name}\nID : {cmd.from_user.id} \nLink : [click here](tg://user?id={cmd.from_user.id})",
            )
        else:
            LOGS.info(f"#NewUser :- Name : {cmd.from_user.first_name} ID : {cmd.from_user.id}")

    ban_status = await db.get_ban_status(chat_id)
    if ban_status["is_banned"]:
        if (
            datetime.date.today() - datetime.date.fromisoformat(ban_status["banned_on"])
        ).days > ban_status["ban_duration"]:
            await db.remove_ban(chat_id)
        else:
            await cmd.reply_text("You are Banned to Use This Bot ", quote=True)
            return
    await must_join_channel(bot,cmd)  
    await cmd.continue_propagation()


