from pyrogram.types import CallbackQuery, InlineKeyboardButton, InlineKeyboardMarkup


#messages
# START = """
# **Hello🎈{}!** \n 

# **I'll Kick All New Users As Soon As he Join Your Chat**

# **Just Add Me To Your Channel Or In Your Group ➕**\n

# **For More Details Open Help Menu**

# **A Bot Project By @nrbots**
# """
START = """
**مرحبا🎈{}!**

**أنا روبوت بسيط اقوم بنقل الأعضاء النشطين من مجموعة أخرى إلى مجموعتك.**

**لست بحاجة إلى إضافتي إلى قناتك أو في مجموعتك**\n

**اضغط على تعليمات 👇 لمعرفة طريقة الاستخدام**

في حالة وجود أي مشكلة أو خطأ ، يرجى إبلاغنا في مجموعة الدعم الخاصة بنا @NrBotsupport

**قناة البوت @nrbots ❤️**
"""
HELP = """
- تعليمات استخدام البوت 🤖⚡..

• قم بأضافه حساب او اكثر كي تتمكن من استخدام البوت يفضل اضافه رقم وهمي 

- بعد اضافه رقم الى البوت تستطيع نقل الاعضاء من اي مجموعه الى مجموعتك او قناتك🤖✔.

**اوامر استخدام البوت 🤖💖**

- /start **اضغط للتاكد من ان البوت يعمل🤖**

- /login **اضغط لتسجيل الدخول إلى حسابك في البوت و للإضافة حساب آخر 👤**

- /status **للتحقق من حالة تسجيل الدخول الخاصة بك✔**

- /memadd **اضغط للبدا بنقل الأعضاء الى قناتك او مجموعتك👥** 

- /help **اضغط لمعرفه تعليمات📋**


في حالة وجود أي مشكلة أو خطأ ، يرجى إبلاغنا في مجموعة الدعم الخاصة بنا @NrBotsupport

**قناة البوت @nrbots ❤️**
"""
# /ping **use this to check the server ping and uptime of this bot**
# - /stop for stop the adding process.
START_BUTTONS = InlineKeyboardMarkup(
        [[
        InlineKeyboardButton('تعليمات', callback_data='help'),
        InlineKeyboardButton('إغلاق', callback_data='close')
        ],[
        InlineKeyboardButton('Join Updates Channel',url = 'https://t.me/nrbots')],[
        InlineKeyboardButton('Join Support Group',url = 'https://t.me/NrBotsupport'),
        ]
        ]
       
    )
HELP_BUTTONS = InlineKeyboardMarkup(
        [[
        InlineKeyboardButton('Home', callback_data='home'),
        InlineKeyboardButton('Close', callback_data='close')
        ],[
        InlineKeyboardButton('قناة تحديثات البوت',url = 'https://t.me/nrbots')],[
        InlineKeyboardButton('مجموعة فريق دعم البوت',url = 'https://t.me/NrBotsupport'),
        ]
        ]
       
    )