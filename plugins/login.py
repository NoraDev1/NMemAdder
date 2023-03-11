import asyncio
import os
import time
from plugins.adder2 import edit_nrbots
from tools.main import bot
from pyromod import listen
from asyncio.exceptions import TimeoutError
from pyromod.helpers import ikb
from pyrogram import Client, filters
from pyrogram import Client as Client1
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, Message

from pyrogram.errors import (
    SessionPasswordNeeded as SessionPasswordNeeded1, FloodWait as FloodWait1,
    PhoneNumberInvalid as PhoneNumberInvalid1 , ApiIdInvalid as ApiIdInvalid1,
    PhoneCodeInvalid as PhoneCodeInvalid1, PhoneCodeExpired as PhoneCodeExpired1
)
from tools.database import Database
import config
db = Database(config.DB_URL, config.DB_NAME)
# api_id = config.API_ID
# api_hash = config.API_HASH


PHONE_NUMBER_TEXT = (
    "أرسل الآن رقم هاتف حساب Telegram الخاص بك بالتنسيق الدولي.  \n"
     "تضمين رمز البلد. مثال: ** + +14154566376 ** \n\n"
     "اضغط /cancel لإلغاء المهمة."
)

API_TEXT = (
    "ارسل الايدي الخاص بك ...\n\n اذا لا تعرف من اين تحصل على الايدي\n 1- اذهب الى موقع تلغرام هذا👇\n http://my.telegram.org \n 2- انسخ الايدي ثما ارسله هنا`"
)

HASH_TEXT = (
    "ارسل api Hash \n\n اذا لا تعرف من اين تحصل على api Hash \n 1- اذهب الى موقع تلغرام هذا👇\n http://my.telegram.org  \n2- انسخ api Hash ثما ارسله هنا`"
)

@bot.on_message(filters.private & filters.command("login"))
async def genStr(_, msg: Message):
    nr = await msg.reply_text("**.... NoRa BOTS ....**")
    await edit_nrbots(nr)
    await asyncio.sleep(0.4)
    await nr.delete()
    await msg.reply("{}! لمزيد من الأمان لحسابك ، يجب أن تزودني بـ api_id و api_hash لتسجيل الدخول إلى حسابك\n\n⚠️ يرجى تسجيل الدخول إلى حسابك الوهمي ، ولا تستخدم حسابك الحقيقي ⚠️\n\n شاهد طريقة الحصول على api id , api Hash \n\n https://youtu.be/NsbhYHz7K_w️".format(msg.from_user.mention))
    await asyncio.sleep(2)
    chat = msg.chat
    api = await bot.ask(
        chat.id, API_TEXT)
    
    if await is_cancel(msg, api.text):
        return
    try:
        check_api = int(api.text)
    except Exception:
        await msg.reply("`APP_ID` غير صالح.\nاضغط على /login لتسجيل مره اخرى.")
        return
    api_id = api.text
    hash = await bot.ask(chat.id, HASH_TEXT)
    if await is_cancel(msg, hash.text):
        return
    if not len(hash.text) >= 30:
        await msg.reply("`api_Hash` غير صالح.\nاضغط على /login لتسجيل مره اخرى")
        return
    api_hash = hash.text
    while True:
        number = await bot.ask(chat.id, PHONE_NUMBER_TEXT)
        if not number.text:
            continue
        if await is_cancel(msg, number.text):
            return
        phone = number.text
        confirm = await bot.ask(chat.id, f'`هذا "{phone}" صحيح؟ (y/n):` \n\nارسل: `y` (اذا كان اارقم صحيح ارسل y )\nارسل: `n` (اذا كان الرقم خطأ ارسل n)')
        if await is_cancel(msg, confirm.text):
            return
        confirm = confirm.text.lower()
        if confirm == "y":
            break
    try:
        client = Client1(f"{chat.id}_account", api_id=api_id, api_hash=api_hash,in_memory=True)
    except Exception as e:
        await bot.send_message(chat.id ,f"**ERROR:** `{str(e)}`\nPress /login to Start again.")
        return
    try:
        await client.connect()
    except ConnectionError:
        await client.disconnect()
        await client.connect()
    try:
        code = await client.send_code(phone)
        await asyncio.sleep(1)
    except FloodWait1 as e:
        await msg.reply(f"You account have Floodwait of {e.value} Seconds. Please try after {e.value} Seconds")
        return
    except ApiIdInvalid1:
        await msg.reply("APP ID and API Hash are Invalid.\n\nPress /login to Start again.")
        return
    except PhoneNumberInvalid1:
        await msg.reply("رقمك هذا غير صحيح.\n\nاضغط /login لتسجيل مره اخرى.")
        return
    try:
        a = """
يتم إرسال كود مكون من خمسه ارقام إلى رقم هاتفك ، 
الرجاء ارسال الكود بتنسيق هذا 1 2 3 4 5. (مسافة بين كل رقم!) \n
إذا لم يرسل Bot OTP ، فحاول  أعد تشغيل وابدأ المهمة مرة أخرى باستخدام الأمر /start إلى Bot.
اضغط /cancel للإلغاء.."""
        otp = await bot.ask(chat.id, a
                    , timeout=300
                    )

    except TimeoutError:
        await msg.reply("بلغ الحد الزمني 5 دقائق.\n اضغط /login الدخول للبدء من جديد")
        return
    if await is_cancel(msg, otp.text):
        return
    otp_code = otp.text
    try:
        await client.sign_in(phone, code.phone_code_hash, phone_code=' '.join(str(otp_code)))
    except PhoneCodeInvalid1:
        await msg.reply("رمز غير صالح. \n\n اضغط /login الدخول للبدء من جديد..")
        return
    except PhoneCodeExpired1:
        await msg.reply("Code is Expired.\n\nPress /login to Start again.")
        return
    except SessionPasswordNeeded1:
        try:
            two_step_code = await bot.ask(
                chat.id, 
                "حسابك يوجد فيه تحقق بخطوتين.\nارسل رمز تحقق بخطوتين او .\n\nاضغط /cancel للإلغاء.",
                timeout=300
            )
        except TimeoutError:
            await msg.reply("`Time limit reached of 5 min.\n\nPress /login to Start again.`")
            return
        if await is_cancel(msg, two_step_code.text):
            return
        new_code = two_step_code.text
        try:
            await client.check_password(new_code)
        except Exception as e:
            await msg.reply(f"**ERROR:** `{str(e)}`")
            return
    except Exception as e:
        await bot.send_message(chat.id ,f"**ERROR:** `{str(e)}`")
        return
    try:
        session_string = await client.export_session_string()
        await bot.send_message(chat.id,"✅ حسابك متصل بنجاح",)
        await db.set_session(chat.id, session_string)
        await db.set_api(chat.id,api_id)
        await db.set_hash(chat.id,api_hash)
        await db.set_login(chat.id,True)
        await client.disconnect()
    except Exception as e:
        await bot.send_message(chat.id ,f"**ERROR:** `{str(e)}`")
        return





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




@Client.on_message(filters.private & filters.command("status"))
async def logoutt(client, message:Message):
    nr = await message.reply_text("checking...")
    user_id = message.from_user.id
    if await db.get_session(user_id):

        try:    
            session = await db.get_session(user_id) 
            api_id = await db.get_api(user_id) 
            api_hash = await db.get_hash(user_id) 
            app = Client(name = user_id,session_string=f"{session}", api_id = api_id, api_hash = api_hash,in_memory=True) 
            await app.start()
            await app.get_me()
            xx = await app.get_me()
            op = xx.first_name
                # ox = xx.username
            id = xx.id
            await app.stop()

            await nr.edit_text(f'USER DETAILS\n\nName: {op}\n\nUser Id: {id}',
                    reply_markup=InlineKeyboardMarkup(
                        [
                            [
                                InlineKeyboardButton(
                                    f"login status {'✅'if ((await db.get_session(user_id)) ) else '❎' }",
                                    callback_data="xyz",
                                )
                            ],
                            [InlineKeyboardButton(
                                f"{'Logout'if ((await db.get_session(user_id)) ) else 'Please Login To Use Adding Feature.' }", callback_data= f"{'Logout'if ((await db.get_session(user_id)) ) else 'Login' }",
                                
                                )
                            ],
                            [InlineKeyboardButton("close", callback_data="close")],
                        ]
                    ),)
        except ApiIdInvalid1:
            try:
                session = await db.get_session(user_id) 
                app = Client(name = user_id,session_string=f"{session}", api_id = config.API_ID, api_hash = config.API_HASH)
                await app.start()
                await app.get_me()
                xx = await app.get_me()
                op = xx.first_name
                # ox = xx.username
                id = xx.id
                await app.stop()
                keyboard = ikb([
        [(f"login status {'✅'if ((await db.get_session(user_id)) ) else '❎' }", f'xyz')], 
        [(f"{'Logout'if ((await db.get_session(user_id)) ) else 'Please Login To Use Adding Feature.' }",f"{'Logout'if ((await db.get_session(user_id)) ) else 'Login' }")],
        [("close","close")]
                    ])
                await nr.edit_text(f'USER DETAILS\n\nName: {op}\n\nUser Id: {id}',
                reply_markup=keyboard)
                    # reply_markup=InlineKeyboardMarkup(
                    #     [
                    #         [
                    #             InlineKeyboardButton(
                    #                 f"login status {'✅'if ((await db.get_session(user_id)) ) else '❎' }",
                    #                 callback_data="xyz",
                    #             )
                    #         ],
                    #         [InlineKeyboardButton(
                    #             f"{'Logout'if ((await db.get_session(user_id)) ) else 'Please Login To Use Adding Feature.' }", callback_data= f"{'Logout'if ((await db.get_session(user_id)) ) else 'Login' }",
                                
                    #             )
                    #         ],
                    #         [InlineKeyboardButton("close", callback_data="close")],
                    #     ]
                    # ),)
            except Exception as e:
                return await nr.edit_text(f'**Error** : {e}')
        except Exception as e:
            return await nr.edit_text(f'**Error** : {e}')
        

    else:        
        keyboard = ikb([
        [(f"login status {'✅'if ((await db.get_session(user_id)) ) else '❎' }", f'xyz')], 
        [(f"{'Logout'if ((await db.get_session(user_id)) ) else 'Please Login To Use Adding Feature.' }",f"{'Logout'if ((await db.get_session(user_id)) ) else 'Login' }")],
        [("close","close")]
                    ])
        await nr.edit_text( 'Please Login to use all the bot features.',
                reply_markup=keyboard)
                # reply_markup=InlineKeyboardMarkup(
                #     [
                #         [
                #             InlineKeyboardButton(
                #                 f"login status {'✅'if ((await db.get_session(user_id)) ) else '❎' }",
                #                 callback_data="xyz",
                #             )
                #         ],
                #         [InlineKeyboardButton(
                #             f"{'Logout'if ((await db.get_session(user_id)) ) else 'Please Login To Use Adding Feature.' }", callback_data= f"{'Logout'if ((await db.get_session(user_id)) ) else 'Login' }",
                            
                #             )
                #         ],
                #         [InlineKeyboardButton("close", callback_data="close")],
                #     ]
                # ),)


@Client.on_callback_query(filters.regex("Logout"))
async def cb_data_logout(client, update):
    user_id = update.from_user.id
    # if update.data == "logout":
    await update.message.edit_text(
            text='هل انت متاكد من تسجيل الخروج',
        reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        f"Yes",
                        callback_data="yes",
                    )
                ],
              
                [InlineKeyboardButton("close", callback_data="close")],
            ]
        ),)


@Client.on_callback_query(filters.regex("yes"))
async def cb_data_yes(client, update):
    user_id = update.from_user.id
    await db.set_session(user_id, "")
    await db.set_login(user_id,False)
    await update.message.edit_text(
            text='Logged Out Successfully ✅\n\nDo terminate the login session manually')
