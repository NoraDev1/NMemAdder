from tools.main import bot

async def getme():
    
    data = await bot.get_me()
    BOT_USERNAME = data.username
    return str(BOT_USERNAME)

async def botid():
    
    data = await bot.get_me()
    BOT_ID = data.id
    return (BOT_ID)