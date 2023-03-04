import asyncio
import logging
from pyrogram import Client
from pyrogram.types import Message
from pyrogram.errors import FloodWait as FloodWait1
from pyrogram import Client as Client1, filters
from pyrogram.types import Message, InlineKeyboardButton, InlineKeyboardMarkup
import time
import datetime
import config
from plugins.eval import remove_if_exists
from tools.database import Database
from pyromod.helpers import ikb
from tools.main import bot
LOGS = logging.getLogger(__name__)
db = Database(config.DB_URL, config.DB_NAME)


# api = "14185021"
# hash = "b29b81f8a9f892ff457df8f3372489fc"

import re
def if_url(url):
    regex = re.compile(
            r'^(?:http|ftp)s?://' # http:// or https://
            #r'^t.me|'
            r't.me|'
            r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|' #domain...
            r'localhost|' #localhost...
            r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})' # ...or ip
            r'(?::\d+)?' # optional port
            r'(?:/?|[/?]\S+)$', re.IGNORECASE)
    
    
    string = url
    x = re.match(regex, string) is not None 
    if x:
        if "t.me" in string:
            xu = string.split("t.me/")[1]
            return f"@{xu}"
    elif "@" in string:
        xu = string
        return xu


@Client.on_message(filters.private & filters.command("memadd"))
async def NewChat(client, msg):
    try:
        chat = msg.chat
        nr = await msg.reply_text(".... NR BOTS ....")
        await edit_nrbots(nr)
        userr = msg.from_user.id
        if not await db.get_session(userr):
            return await nr.edit_text("please /login to use this feature.")

        await nr.delete()
        while True:
            src_raw = await bot.ask(chat.id, "أرسل لي الآن رابط مجموعة عامة من حيث تريد كشط ونقل الأعضاء منها.")
            if not src_raw.text:
                continue
            if await is_cancel(msg, src_raw.text):
                return
            src = if_url(src_raw.text)
            
            dest_raw = await bot.ask(chat.id, "أرسل لي الآن رابط مجموعة عامة حيث تريد إضافة أعضاء اليها.")
            if await is_cancel(msg, dest_raw.text):
                return
            dest = if_url(dest_raw.text)
            quant_raw = await bot.ask(chat.id, "أرسل لي الآن الكمية . كم عدد الأعضاء الذي تريد إضافتها الى مجموعتك.\n\nعلى سبيل المثال ارسل: 5\n\nمن أجل أمان حساباتك ضد حظر الاضافه ، يرجى تزويدنا برقم أقل من 20 رقمًا ")
            if await is_cancel(msg, quant_raw.text):
                return
            quant = int(quant_raw.text)
            type_raw = await bot.ask(chat.id, f'اختر الآن أي نوع من الأعضاء تريد كشطه من مجموعه `{src}`\n\nلنقل اعضاء 👤 نشطين👤 أرسل  `a`\n\nلنقل اعضاء 👥 مختلط 👥 أرسل الأعضاء `m`. \n\nارسل: `a` (إذا كنت تريد اعضاء نشطًين)\nارسل: `m` (إذا كنت تريد اعضاء نشطًين)')
            if await is_cancel(msg, type_raw.text):
                return
            type = type_raw.text.lower()

            confirm = await bot.ask(chat.id, f'أنت تريد إضافة `{quant}` {"`👤 أعضاء نشطين 👤`" if type == "a" else "`👥 أعضاء مختلطين 👥`"} من مجموعه `{src}` الى مجموعتك `{dest}`\n\n`هل هذا متاكد من الاضافه؟  (y / n):` \n\nارسل: `y` (إذا كانت الإجابة نعم)\nارسل: `n` (إذا كانت الإجابة لا)')
            if await is_cancel(msg, confirm.text):
                return
            confirm = confirm.text.lower()
            if confirm == "y":
                break
        try:

            await add(msg, src=src, dest=dest, count=quant, type=type)
        except Exception as e:
            return await msg.reply_text(f"**ERROR:** `{str(e)}`",reply_markup=keyboard)
    except Exception as e:
        return await msg.reply_text(f"**ERROR:** `{str(e)}`",reply_markup=keyboard)


async def is_cancel(msg: Message, text: str):
    if text.startswith("/cancel"):
        await msg.reply("Login Cancelled.")
        return True
    elif text.startswith("/login"):
        await msg.reply("Login Cancelled.")
        return True
    elif text.startswith("/start"):
        await msg.reply("Login Cancelled.")
        return True
    elif text.startswith("/restart"):
        await msg.reply("Login Cancelled.")
        return True
    elif text.startswith("/help"):
        await msg.reply("Login Cancelled.")
        return True
    elif text.startswith("/memadd"):
        await msg.reply("Login Cancelled.")
        return True
    elif text.startswith("/status"):
        await msg.reply("Login Cancelled.")
        return True
    elif text.startswith("/"):
        await msg.reply("Login Cancelled.")
        return True
    return False


async def type_(text: str):
    text = text.lower()
    if text == "y":
        return True
    elif text == "n":
        return False
    else:
        return False


async def edit_nrbots(nr):
    await nr.edit_text("**❤️.... NR BOTS ....❤️**")
    await asyncio.sleep(0.3)
    await nr.edit_text("**.❤️... NR BOTS ...❤️.**")
    await asyncio.sleep(0.3)
    await nr.edit_text("**..❤️.. NR BOTS ..❤️..**")
    await asyncio.sleep(0.3)
    await nr.edit_text("**...❤️. NR BOTS .❤️...**")
    await asyncio.sleep(0.3)
    await nr.edit_text("**....❤️ NR BOTS ❤️....**")
    await asyncio.sleep(0.5)


async def edit_starting(nr):
    await nr.edit_text("**❤️.... STARTING CLIENT ....❤️**")
    await asyncio.sleep(0.3)
    await nr.edit_text("**.❤️... STARTING CLIENT ...❤️.**")
    await asyncio.sleep(0.3)
    await nr.edit_text("**..❤️.. STARTING CLIENT ..❤️..**")
    await asyncio.sleep(0.3)
    await nr.edit_text("**...❤️. STARTING CLIENT .❤️...**")
    await asyncio.sleep(0.3)
    await nr.edit_text("**....❤️ STARTING CLIENT ❤️....**")
    await asyncio.sleep(0.5)


async def edit_ini(nr):
    await nr.edit_text("**❤️........❤️**")
    await asyncio.sleep(0.3)
    await nr.edit_text("**.❤️......❤️.**")
    await asyncio.sleep(0.3)
    await nr.edit_text("**..❤️....❤️..**")
    await asyncio.sleep(0.3)
    await nr.edit_text("**...❤️..❤️...**")
    await asyncio.sleep(0.3)
    await nr.edit_text("**....❤️❤️....**")
    await asyncio.sleep(0.3)
    await nr.edit_text("🎊")
    await asyncio.sleep(0.4)

async def edit_active(nr):
    await nr.edit_text("**❤️.... STARTING ACTIVE MEMBER ADDING ....❤️**")
    await asyncio.sleep(0.3)
    await nr.edit_text("**.❤️... STARTING ACTIVE MEMBER ADDING ...❤️.**")
    await asyncio.sleep(0.3)
    await nr.edit_text("**..❤️.. STARTING ACTIVE MEMBER ADDING ..❤️..**")
    await asyncio.sleep(0.3)
    await nr.edit_text("**...❤️. STARTING ACTIVE MEMBER ADDING .❤️...**")
    await asyncio.sleep(0.3)
    await nr.edit_text("**....❤️ STARTING ACTIVE MEMBER ADDING ❤️....**")
    await asyncio.sleep(0.5)

async def edit_mixed(nr):
    await nr.edit_text("**❤️.... STARTING MIXED MEMBER ADDING ....❤️**")
    await asyncio.sleep(0.3)
    await nr.edit_text("**.❤️... STARTING MIXED MEMBER ADDING ...❤️.**")
    await asyncio.sleep(0.3)
    await nr.edit_text("**..❤️.. STARTING MIXED MEMBER ADDING ..❤️..**")
    await asyncio.sleep(0.3)
    await nr.edit_text("**...❤️. STARTING MIXED MEMBER ADDING .❤️...**")
    await asyncio.sleep(0.3)
    await nr.edit_text("**....❤️ STARTING MIXED MEMBER ADDING ❤️....**")
    await asyncio.sleep(0.5)

keyboard = ikb([
        [('✨ Join Updates Channel ✨', 'https://t.me/nrbots',"url")], 

        [('✨ Join Support Group ✨','https://t.me/NrBotsupport',"url")]
                ])

async def add(msg, src, dest, count: int, type):
    userid = msg.from_user.id
    nr = await msg.reply_text("**........**")
    await edit_ini(nr)

    try:

        cc = 0

        session = await db.get_session(userid)
        api = await db.get_api(userid) 
        hash = await db.get_hash(userid) 
        # print(session)
        # session = str(session)

        app = Client(name= userid,session_string=session, api_id=api, api_hash=hash)
        await nr.edit_text("**.... STARTING CLIENT ....**")
        
        await app.start()
        await edit_starting(nr)
        # print('\n\napp started...')
        # await asyncio.sleep(0.5)

        # source chat

        chat = await app.get_chat(src)
        schat_id = chat.id
        await app.join_chat(schat_id)
        # dest chat
        xx = await app.get_chat(dest)
        tt = xx.members_count
        dchat_id = xx.id
        await app.join_chat(dchat_id)
        start_time = time.time()
        await asyncio.sleep(3)
    except Exception as e:
                        e = str(e)
                               # await err(e=e,app=app,nr=nr)
                        if "Client has not been started yet" in e:
                            remove_if_exists(f"{msg.from_user.id}_account.session")
                            return await nr.edit_text("Client has not been started yet",reply_markup=keyboard)
                        elif "403 USER_PRIVACY_RESTRICTED" in e:
                            await nr.edit_text("failed to add because of The user's privacy settings",reply_markup=keyboard)
                            await asyncio.sleep(1)
                        elif "400 CHAT_ADMIN_REQUIRED" in e:
                            await nr.edit_text("failed to add because of This method requires chat admin privileges.\n\nplease make your account admin on the group and try again",reply_markup=keyboard)
                        elif "400 INVITE_REQUEST_SENT" in e:
                            
                            remove_if_exists(f"{msg.from_user.id}_account.session")
                            return await nr.edit_text("hey i cant scrape/add members from a group where i need admin approval to join chat.",reply_markup=keyboard)
                        elif "400 PEER_FLOOD" in e:
                            # 
                            remove_if_exists(f"{msg.from_user.id}_account.session")
                            return await nr.edit_text("Adding stopped due to 400 PEER_FLOOD\n\nyour account is limited please wait sometimes then try again.",reply_markup=keyboard)
                        elif "401 AUTH_KEY_UNREGISTERED" in e:
                            
                            await db.set_session(msg.from_user.id, "")
                            await db.set_login(msg.from_user.id,False)
                            remove_if_exists(f"{msg.from_user.id}_account.session")
                            return await nr.edit_text("please login again to use this feature",reply_markup=keyboard)
                        elif "403 CHAT_WRITE_FORBIDDEN" in e:
                            
                            remove_if_exists(f"{msg.from_user.id}_account.session")
                            return await nr.edit_text("You don't have rights to send messages in this chat\nPlease make user account admin and try again",reply_markup=keyboard)
                        elif "400 CHANNEL_INVALID" in e:
                            
                            remove_if_exists(f"{msg.from_user.id}_account.session")
                            return await nr.edit_text("The source or destination username is invalid",reply_markup=keyboard)
                        elif "400 USERNAME_NOT_OCCUPIED" in e:
                            
                            remove_if_exists(f"{msg.from_user.id}_account.session")
                            return await nr.edit_text("The username is not occupied by anyone please check the username or userid that you have provided",reply_markup=keyboard)
                        elif "401 SESSION_REVOKED" in e:
                            
                            await db.set_session(msg.from_user.id, "")
                            await db.set_login(msg.from_user.id,False)
                            remove_if_exists(f"{msg.from_user.id}_account.session")
                            return await nr.edit_text("you have terminated the login session from the user account \n\nplease login again",reply_markup=keyboard)
        
                        return await nr.edit_text(f"**ERROR:** `{str(e)}`",reply_markup=keyboard)

    if type == "a":
        try:
            await nr.edit_text("**.... STARTING ACTIVE MEMBER ADDING ....**")
            await edit_active(nr)
            await asyncio.sleep(0.5)
            # async for member in app.iter_chat_members(schat_id):
            async for member in app.get_chat_members(schat_id):
                user = member.user

                s = ["RECENTLY","ONLINE"]
                if user.is_bot:
                    pass
                else:
                    b = (str(user.status)).split('.')[1]
                    if b in s:
      
                # s = ["online", "recently"]
                
                # if user.status in s:
                        try:

                            user_id = user.id

                            await nr.edit_text(f'TRYING TO ADD: `{user_id}`')

                            if await app.add_chat_members(dchat_id, user_id):
                                cc = cc+1
                                await nr.edit_text(f'ADDED: `{user_id}`')

                                await asyncio.sleep(5)
                        except FloodWait1 as fl:
                            t = "FLOODWAIT DETECTED IN USER ACCOUNT\n\nSTOPPED ADDING PROCESS"

                            await nr.edit_text(t)
                            x2 = await app.get_chat(dchat_id)
                            t2 = x2.members_count
                            completed_in = datetime.timedelta(
                            seconds=int(time.time() - start_time))
                            ttext = f"""
<u>**✨ Stopped adding process due to Floodwait of {fl.value}s ✨**</u>

    ┏━━━━━━━━━━━━━━━━━┓
    ┣✨ Added to chat Id: `{dchat_id}`
    ┣✨ Previous chat member count : **{tt}**
    ┣✨ Current chat member count : **{t2}**
    ┣✨ Total users added : **{cc}**
    ┣✨ Total time taken : **{completed_in}**s
    ┗━━━━━━━━━━━━━━━━━┛
                                """

                            await app.leave_chat(src)
                            await app.stop()
                            remove_if_exists(f"{msg.from_user.id}_account.session")
                            return await nr.edit_text(ttext,reply_markup=keyboard)
                        except Exception as e:
                            e = str(e)
                                # await err(e=e,app=app,nr=nr)
                            if "Client has not been started yet" in e:
                                remove_if_exists(f"{msg.from_user.id}_account.session")
                                return await nr.edit_text("Client has not been started yet",reply_markup=keyboard)
                            elif "403 USER_PRIVACY_RESTRICTED" in e:
                                await nr.edit_text("failed to add because of The user's privacy settings")
                                await asyncio.sleep(1)
                            elif "400 CHAT_ADMIN_REQUIRED" in e:
                                await nr.edit_text("failed to add because of This method requires chat admin privileges.\n\nplease make your account admin on the group and try again",reply_markup=keyboard)
                            elif "400 INVITE_REQUEST_SENT" in e:
                                await app.stop()
                                remove_if_exists(f"{msg.from_user.id}_account.session")
                                return await nr.edit_text("hey i cant scrape/add members from a group where i need admin approval to join chat.",reply_markup=keyboard)
                            elif "400 PEER_FLOOD" in e:
                                await app.stop()
                                remove_if_exists(f"{msg.from_user.id}_account.session")
                                return await nr.edit_text("Adding stopped due to 400 PEER_FLOOD\n\nyour account is limited please wait sometimes then try again.",reply_markup=keyboard)
                            elif "401 AUTH_KEY_UNREGISTERED" in e:
                                await app.stop()
                                await db.set_session(msg.from_user.id, "")
                                await db.set_login(msg.from_user.id,False)
                                remove_if_exists(f"{msg.from_user.id}_account.session")
                                return await nr.edit_text("please login again to use this feature",reply_markup=keyboard)
                            elif "403 CHAT_WRITE_FORBIDDEN" in e:
                                await app.stop()
                                remove_if_exists(f"{msg.from_user.id}_account.session")
                                return await nr.edit_text("You don't have rights to send messages in this chat\nPlease make user account admin and try again",reply_markup=keyboard)
                            elif "400 CHANNEL_INVALID" in e:
                                await app.stop()
                                remove_if_exists(f"{msg.from_user.id}_account.session")
                                return await nr.edit_text("The source or destination username is invalid",reply_markup=keyboard)
                            elif "400 USERNAME_NOT_OCCUPIED" in e:
                                await app.stop()
                                remove_if_exists(f"{msg.from_user.id}_account.session")
                                return await nr.edit_text("The username is not occupied by anyone please check the username or userid that you have provided",reply_markup=keyboard)
                            elif "401 SESSION_REVOKED" in e:
                                await app.stop()
                                await db.set_session(msg.from_user.id, "")
                                await db.set_login(msg.from_user.id,False)
                                remove_if_exists(f"{msg.from_user.id}_account.session")
                                return await nr.edit_text("you have terminated the login session from the user account \n\nplease login again",reply_markup=keyboard)
          
                            else:
                                await nr.edit_text(f'FAILED TO ADD \n\n**ERROR:** `{str(e)}`')
                                await asyncio.sleep(5)

                        if cc == count:
                            x2 = await app.get_chat(dchat_id)
                            t2 = x2.members_count
                            completed_in = datetime.timedelta(
                            seconds=int(time.time() - start_time))
                            ttext = f"""
<u>**✨ Successfully completed adding process ✨**</u>

    ┏━━━━━━━━━━━━━━━━━┓
    ┣✨ Added to chat Id: `{dchat_id}`
    ┣✨ Previous chat member count : **{tt}**
    ┣✨ Current chat member count : **{t2}**
    ┣✨ Total users added : **{cc}**
    ┣✨ Total time taken : **{completed_in}**s
    ┗━━━━━━━━━━━━━━━━━┛
                                """

                            await app.leave_chat(src)
                            await app.stop()
                            remove_if_exists(f"{msg.from_user.id}_account.session")
                            return await nr.edit_text(ttext,reply_markup=keyboard)

        except Exception as e:
                        e = str(e)
                               # await err(e=e,app=app,nr=nr)
                        if "Client has not been started yet" in e:
                            remove_if_exists(f"{msg.from_user.id}_account.session")
                            return await nr.edit_text("Client has not been started yet",reply_markup=keyboard)
                        elif "403 USER_PRIVACY_RESTRICTED" in e:
                            await nr.edit_text("failed to add because of The user's privacy settings",reply_markup=keyboard)
                            await asyncio.sleep(1)
                        elif "400 CHAT_ADMIN_REQUIRED" in e:
                            await nr.edit_text("failed to add because of This method requires chat admin privileges.\n\nplease make your account admin on the group and try again",reply_markup=keyboard)
                        elif "400 INVITE_REQUEST_SENT" in e:
                            await app.stop()
                            remove_if_exists(f"{msg.from_user.id}_account.session")
                            return await nr.edit_text("hey i cant scrape/add members from a group where i need admin approval to join chat.",reply_markup=keyboard)
                        elif "400 PEER_FLOOD" in e:
                            await app.stop()
                            remove_if_exists(f"{msg.from_user.id}_account.session")
                            return await nr.edit_text("Adding stopped due to 400 PEER_FLOOD\n\nyour account is limited please wait sometimes then try again.",reply_markup=keyboard)
                        elif "401 AUTH_KEY_UNREGISTERED" in e:
                            await app.stop()
                            await db.set_session(msg.from_user.id, "")
                            await db.set_login(msg.from_user.id,False)
                            remove_if_exists(f"{msg.from_user.id}_account.session")
                            return await nr.edit_text("please login again to use this feature",reply_markup=keyboard)
                        elif "403 CHAT_WRITE_FORBIDDEN" in e:
                            await app.stop()
                            remove_if_exists(f"{msg.from_user.id}_account.session")
                            return await nr.edit_text("You don't have rights to send messages in this chat\nPlease make user account admin and try again",reply_markup=keyboard)
                        elif "400 CHANNEL_INVALID" in e:
                            await app.stop()
                            remove_if_exists(f"{msg.from_user.id}_account.session")
                            return await nr.edit_text("The source or destination username is invalid",reply_markup=keyboard)
                        elif "400 USERNAME_NOT_OCCUPIED" in e:
                            await app.stop()
                            remove_if_exists(f"{msg.from_user.id}_account.session")
                            return await nr.edit_text("The username is not occupied by anyone please check the username or userid that you have provided",reply_markup=keyboard)
                        elif "401 SESSION_REVOKED" in e:
                            await app.stop()
                            await db.set_session(msg.from_user.id, "")
                            await db.set_login(msg.from_user.id,False)
                            remove_if_exists(f"{msg.from_user.id}_account.session")
                            return await nr.edit_text("you have terminated the login session from the user account \n\nplease login again",reply_markup=keyboard)
                        await app.stop()
                        remove_if_exists(f"{msg.from_user.id}_account.session")
                        return await nr.edit_text(f"**ERROR:** `{str(e)}`",reply_markup=keyboard)


    if type != "a":
        try:
            await nr.edit_text("**.... STARTING MIXED MEMBER ADDING ....**")
            await edit_mixed(nr)
            async for member in app.get_chat_members(schat_id):
                user = member.user
                  # s = ["online" , "recently"]
                  # if user.status in s:
                try:

                    user_id = user.id

                    await nr.edit_text(f'TRYING TO ADD: `{user_id}`')

                    if await app.add_chat_members(dchat_id, user_id):
                        cc = cc+1
                        await nr.edit_text(f'ADDED: `{user_id}`')

                        await asyncio.sleep(5)
                except FloodWait1 as fl:
                    t = "FLOODWAIT DETECTED IN USER ACCOUNT\n\nSTOPPED ADDING PROCESS"

                    await nr.edit_text(t)
                    x2 = await app.get_chat(dchat_id)
                    t2 = x2.members_count
                    completed_in = datetime.timedelta(
                    seconds=int(time.time() - start_time))
                    ttext = f"""
<u>**✨ Stopped adding process due to Floodwait of {fl.value}s ✨**</u>

    ┏━━━━━━━━━━━━━━━━━┓
    ┣✨ Added to chat Id: `{dchat_id}`
    ┣✨ Previous chat member count : **{tt}**
    ┣✨ Current chat member count : **{t2}**
    ┣✨ Total users added : **{cc}**
    ┣✨ Total time taken : **{completed_in}**s
    ┗━━━━━━━━━━━━━━━━━┛
    
                        """

                    await app.leave_chat(src)
                    await app.stop()
                    remove_if_exists(f"{msg.from_user.id}_account.session")
                    return await nr.edit_text(ttext,reply_markup=keyboard)
                except Exception as e:
                    e = str(e)
                    # await err(e=e,app=app,nr=nr)

                    if "Client has not been started yet" in e:
                        remove_if_exists(f"{msg.from_user.id}_account.session")
                        return await nr.edit_text("Client has not been started yet\n\nplease start the adding process again.",reply_markup=keyboard)
                    elif "403 USER_PRIVACY_RESTRICTED" in e:
                        await nr.edit_text("failed to add because of The user's privacy settings",reply_markup=keyboard)
                        await asyncio.sleep(1)
                    elif "400 CHAT_ADMIN_REQUIRED" in e:
                        await nr.edit_text("failed to add because of This method requires chat admin privileges.\n\nplease make your account admin on the group and try again",reply_markup=keyboard)
                    elif "400 INVITE_REQUEST_SENT" in e:
                        await app.stop()
                        remove_if_exists(f"{msg.from_user.id}_account.session")
                        return await nr.edit_text("hey i cant scrape/add members from a group where i need admin approval to join chat.",reply_markup=keyboard)
                    elif "400 PEER_FLOOD" in e:
                        await app.stop()
                        remove_if_exists(f"{msg.from_user.id}_account.session")
                        return await nr.edit_text("Adding stopped due to 400 PEER_FLOOD\n\nyour account is limited please wait sometimes then try again.",reply_markup=keyboard)
                    elif "401 AUTH_KEY_UNREGISTERED" in e:
                        await app.stop()
                        await db.set_session(msg.from_user.id, "")
                        await db.set_login(msg.from_user.id,False)
                        remove_if_exists(f"{msg.from_user.id}_account.session")
                        return await nr.edit_text("please login again to use this feature",reply_markup=keyboard)
                    elif "403 CHAT_WRITE_FORBIDDEN" in e:
                        await app.stop()
                        remove_if_exists(f"{msg.from_user.id}_account.session")
                        return await nr.edit_text("You don't have rights to add members in this chat\nPlease make user your account admin and try again",reply_markup=keyboard)
                    elif "400 CHANNEL_INVALID" in e:
                        await app.stop()
                        remove_if_exists(f"{msg.from_user.id}_account.session")
                        return await nr.edit_text("The source or destination username is invalid",reply_markup=keyboard)
                    elif "400 USERNAME_NOT_OCCUPIED" in e:
                        await app.stop()
                        remove_if_exists(f"{msg.from_user.id}_account.session")
                        return await nr.edit_text("The username is not occupied by anyone please check the username or userid that you have provided",reply_markup=keyboard)
                    elif "401 SESSION_REVOKED" in e:
                        await app.stop()
                        await db.set_session(msg.from_user.id, "")
                        await db.set_login(msg.from_user.id,False)
                        remove_if_exists(f"{msg.from_user.id}_account.session")
                        return await nr.edit_text("you have terminated the login session from the user account \n\nplease login again",reply_markup=keyboard)
                    else:
                        await nr.edit_text(f'FAILED TO ADD \n\n**ERROR:** `{str(e)}`')
                        await asyncio.sleep(5)

                if cc == count:
                    x2 = await app.get_chat(dchat_id)
                    t2 = x2.members_count
                    completed_in = datetime.timedelta(
                    seconds=int(time.time() - start_time))
                    ttext = f"""
<u>**✨ Successfully completed adding process ✨**</u>

    ┏━━━━━━━━━━━━━━━━━┓
    ┣✨ Added to chat Id: `{dchat_id}`
    ┣✨ Previous chat member count : **{tt}**
    ┣✨ Current chat member count : **{t2}**
    ┣✨ Total users added : **{cc}**
    ┣✨ Total time taken : **{completed_in}**s
    ┗━━━━━━━━━━━━━━━━━┛
                        """

                    await app.leave_chat(src)
                    await app.stop()
                    remove_if_exists(f"{msg.from_user.id}_account.session")
                    return await nr.edit_text(ttext,reply_markup=keyboard)

        except Exception as e:
                        e = str(e)
                               # await err(e=e,app=app,nr=nr)
                        if "Client has not been started yet" in e:
                            remove_if_exists(f"{msg.from_user.id}_account.session")
                            return await nr.edit_text("Client has not been started yet",reply_markup=keyboard)
                        elif "403 USER_PRIVACY_RESTRICTED" in e:
                            await nr.edit_text("failed to add because of The user's privacy settings",reply_markup=keyboard)
                            await asyncio.sleep(1)
                        elif "400 CHAT_ADMIN_REQUIRED" in e:
                            await nr.edit_text("failed to add because of This method requires chat admin privileges.\n\nplease make your account admin on the group and try again",reply_markup=keyboard)
                        elif "400 INVITE_REQUEST_SENT" in e:
                            await app.stop()
                            remove_if_exists(f"{msg.from_user.id}_account.session")
                            return await nr.edit_text("hey i cant scrape/add members from a group where i need admin approval to join chat.",reply_markup=keyboard)
                        elif "400 PEER_FLOOD" in e:
                            await app.stop()
                            remove_if_exists(f"{msg.from_user.id}_account.session")
                            return await nr.edit_text("Adding stopped due to 400 PEER_FLOOD\n\nyour account is limited please wait sometimes then try again.",reply_markup=keyboard)
                        elif "401 AUTH_KEY_UNREGISTERED" in e:
                            await app.stop()
                            await db.set_session(msg.from_user.id, "")
                            await db.set_login(msg.from_user.id,False)
                            remove_if_exists(f"{msg.from_user.id}_account.session")
                            return await nr.edit_text("please login again to use this feature",reply_markup=keyboard)
                        elif "403 CHAT_WRITE_FORBIDDEN" in e:
                            await app.stop()
                            remove_if_exists(f"{msg.from_user.id}_account.session")
                            return await nr.edit_text("You don't have rights to send messages in this chat\nPlease make user account admin and try again",reply_markup=keyboard)
                        elif "400 CHANNEL_INVALID" in e:
                            await app.stop()
                            remove_if_exists(f"{msg.from_user.id}_account.session")
                            return await nr.edit_text("The source or destination username is invalid",reply_markup=keyboard)
                        elif "400 USERNAME_NOT_OCCUPIED" in e:
                            await app.stop()
                            remove_if_exists(f"{msg.from_user.id}_account.session")
                            return await nr.edit_text("The username is not occupied by anyone please check the username or userid that you have provided",reply_markup=keyboard)
                        elif "401 SESSION_REVOKED" in e:
                            await app.stop()
                            await db.set_session(msg.from_user.id, "")
                            await db.set_login(msg.from_user.id,False)
                            remove_if_exists(f"{msg.from_user.id}_account.session")
                            return await nr.edit_text("you have terminated the login session from the user account \n\nplease login again",reply_markup=keyboard)
                        await app.stop()
                        remove_if_exists(f"{msg.from_user.id}_account.session")
                        return await nr.edit_text(f"**ERROR:** `{str(e)}`",reply_markup=keyboard)