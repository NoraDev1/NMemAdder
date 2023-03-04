from pyrogram import Client, filters
from pyrogram.types import Message, InlineKeyboardButton, InlineKeyboardMarkup
from plugins.getme import getme
from tools.messages import HELP, START, START_BUTTONS, HELP_BUTTONS
from time import time
from datetime import datetime
from config import AUTH_USERS

START_TIME = datetime.utcnow()
START_TIME_ISO = START_TIME.replace(microsecond=0).isoformat()
TIME_DURATION_UNITS = (
    ('week', 60 * 60 * 24 * 7),
    ('day', 60 * 60 * 24),
    ('hour', 60 * 60),
    ('min', 60),
    ('sec', 1)
)
async def _human_time_duration(seconds):
    if seconds == 0:
        return 'inf'
    parts = []
    for unit, div in TIME_DURATION_UNITS:
        amount, seconds = divmod(int(seconds), div)
        if amount > 0:
            parts.append('{} {}{}'
                         .format(amount, unit, "" if amount == 1 else "s"))
    return ', '.join(parts)


@Client.on_message(filters.private & filters.command("start"))
async def start_pm(client: Client, message: Message):
    # if message.from_user.id not in AUTH_USERS:
    #     # await message.delete()
    #     return
    await message.reply_text(
                    text=START.format(message.from_user.mention),
            disable_web_page_preview=True,
            reply_markup=START_BUTTONS)


@Client.on_message(filters.private & filters.command("help"))
async def help_pm(bot: Client, message: Message):
    # if message.from_user.id not in AUTH_USERS:
    #     # await message.delete()
    #     return

    await message.reply_text(
                    text=HELP,
            disable_web_page_preview=True,
            reply_markup=HELP_BUTTONS)

@Client.on_message(filters.command("ping"))
async def ping_pong(client, message):       
    start = time()
    m_reply = await message.reply_text("checking ping...")
    delta_ping = time() - start
    current_time = datetime.utcnow()
    uptime_sec = (current_time - START_TIME).total_seconds()
    uptime = await _human_time_duration(int(uptime_sec))
    await m_reply.edit_text(
        f"🏓 **PING:**  **{delta_ping * 1000:.3f} ms** \n"
        f"⚡️ **Uptime:** **{uptime}**\n\n "
        f"💖 ** @nrbots**"
    )

@Client.on_callback_query(filters.regex("home"))
async def cb_home(client, update):
    user_id = update.from_user.id
    # if update.from_user.id not in AUTH_USERS:
    #     # await message.delete()
    #     return
    await update.message.edit_text(
            text=START.format(update.from_user.mention),
            disable_web_page_preview=True,
            reply_markup=START_BUTTONS)

@Client.on_callback_query(filters.regex("help"))
async def cb_help(client, update):
        # if update.from_user.id not in AUTH_USERS:
        #     # await message.delete()
        #     return
        await update.message.edit_text(
      
            text=HELP,
            disable_web_page_preview=True,
            reply_markup=HELP_BUTTONS)


@Client.on_callback_query(filters.regex("close"))
async def cb_close(client, update):
    # if update.from_user.id not in AUTH_USERS:
    #     # await message.delete()
    #     return
    await update.message.delete()
         
