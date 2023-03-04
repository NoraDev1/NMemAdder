import os
from pyrogram import Client
import logging
import config
import tracemalloc
from pyromod import listen

from plugins.eval import remove_if_exists

tracemalloc.start()


api = config.API_ID
hash = config.API_HASH
token = config.BOT_TOKEN
# session = config.SESSION

bot = Client(
    "memadder",
    api_id = api,
    api_hash = hash,
    bot_token = token,
    plugins=dict(root="plugins"),
    # in_memory=True,
)


remove_if_exists('logs.txt')
remove_if_exists("unknown_errors.txt")
remove_if_exists("my_account.session")


logging.basicConfig(
  filename=f'logs.txt',
  level=logging.INFO,
  format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logging.getLogger("pyrogram").setLevel(logging.ERROR)
logging.getLogger("pyrogram").setLevel(logging.WARNING)

LOGS = logging.getLogger(__name__)
