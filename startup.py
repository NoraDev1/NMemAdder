import logging
from tools.main import bot 

from aiohttp import web
from tools.web import web_server
# from op import app
from pyrogram import idle
from plugins.getme import getme
from config import *
LOGS = logging.getLogger(__name__)

async def main():
 
    try:   
        print("يبدا البوت....")
        LOGS.info("starting bot...")

        await bot.start()
        app = web.AppRunner(await web_server())
        await app.setup()
        bind_address = "0.0.0.0"
        await web.TCPSite(app, bind_address, PORT).start()

        b = await getme()
        
        LOGS.info(f"@{b} started...")

        print(f"@{b} started...")
        # print(LOGS)
        
        
        await idle()
    except Exception as e:
        print(e)
        LOGS.warning(e)

bot.run(main())
