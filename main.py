#!/usr/bin/env python3
"""
EL FER3OON BOT - بوت الفرعون للتداول مع جدول رسائل
"""

import json
import os
import asyncio
from datetime import datetime
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes, MessageHandler, filters

# ===== إعدادات البوت =====
BOT_TOKEN = "8750815249:AAHtWLBgCg1rWXINj-HJCHt-AJeroGgcFWg"
CHANNEL_LINK = "https://t.me/+wm-XT1rWsHhkNjJk"
USERS_FILE = "users.json"

# ===== file_id للميديا =====
VIDEO_1_FILE_ID = "BAACAgQAAxkBAAM2afzeTK0QaLQGYdnUt0W9_US1KYYAAuIgAAL0I-hTZ1qfFnAM1PA7BA"
VIDEO_2_FILE_ID = "BAACAgQAAxkBAANDafzhEvESXfDc4MXEyqYtKUlBym4AAukgAAL0I-hTbD9qLCbHqxE7BA"
PHOTO_3_FILE_ID = "AgACAgQAAxkBAAM_afzgw-1UxXKQca1RI2oZgQjX6DMAArQQaxv0I-hT1W_dgvVMW_UBAAMCAAN5AAM7BA"

# ===== نصوص الرسائل =====

MSG_1_AR = """🔥 مع تطبيقنا للتداول، الموضوع صار أسهل بكتير!
إشارات قوية ودقيقة على منصة Quotex 📈⚡

تابع الصفقات، حقق نتائج ممتازة، واسحب أرباحك بكل سهولة 💸
ناس كتير بلشت معنا بخطوات بسيطة واليوم عم تحقق دخل يومي محترم 🚀

إذا بدك تبدأ صح وتدخل السوق بثقة، جرّب التطبيق وهلّق دورك تكون من الرابحين 👑"""

MSG_1_EN = """🔥 With our trading app, it's never been easier!
Powerful and accurate signals on Quotex 📈⚡

Track trades, achieve great results, and withdraw your profits easily 💸
Many people started with us with simple steps and today earn a decent daily income 🚀

If you want to start right and enter the market with confidence, try the app and join the winners now 👑"""

MSG_2_AR = """🚀 تطبيق الفرعون للتداول صار جاهز! 👑
كل اللي تحتاجه بإيدك: إشارات دقيقة، تنبيهات سريعة، وتحليل يساعدك تدخل بأفضل وقت على Quotex 📊⚡
التطبيق معمول ليخلي التداول أبسط وأوضح حتى لو كنت مبتدئ 💡
ابدأ بخطوات صح، تابع الإشارات، وشوف الفرق بنفسك 💰🔥"""

MSG_2_EN = """🚀 EL FER3OON Trading App is ready! 👑
Everything you need in your hands: accurate signals, fast alerts, and analysis to help you enter at the best time on Quotex 📊⚡
The app is designed to make trading simpler and clearer even if you're a beginner 💡
Start with the right steps, follow the signals, and see the difference yourself 💰🔥"""

MSG_3_AR = """🎁 سجل من خلالنا واحصل على بونص ترحيبي 100% من قيمة أول إيداع على Quotex 💸🔥
يعني لو أودعت 100$ رح يصير رصيدك 200$ مباشرة 🚀
سجّل من الرابط 👇
https://broker-qx.pro/sign-up/?lid=643973
واستخدم كود البونص 🎯
SPECIAL100
فرصة قوية تبدأ تداولك برأس مال أكبر وتحقيق نتائج أفضل 👑"""

MSG_3_EN = """🎁 Register through us and get a 100% welcome bonus on your first deposit on Quotex 💸🔥
Deposit $100 and your balance becomes $200 instantly 🚀
Register here 👇
https://broker-qx.pro/sign-up/?lid=643973
Use bonus code 🎯
SPECIAL100
A great opportunity to start trading with more capital 👑"""

WELCOME_AR = """هلا {name}! 👋 معك الفرعون 👑
كتير مبسوط إني شايفك هون 🙏

أنا عندي خبرة في التداول، وحابب أشاركك كل شي تعلمته بأسلوب بسيط وواضح، لحتى تفهم بسهولة وتوصل للنتيجة الصح ✅

بنهاية المطاف رح تقدر تحقق دخل ثابت إن شاء الله 💰

كل اللي لازم تعمله إنك تشترك بقناتي المجانية عالتلغرام 📢
اضغط على زر "انضم للقناة" تحت، وأنا بانتظارك هنيك ⭐"""

WELCOME_EN = """Hello {name}! 👋 This is EL FER3OON 👑
So glad you're here! 🙏

I have trading experience and I want to share everything I've learned in a simple, clear way so you can easily understand and achieve real results ✅

By the end, you'll be able to generate consistent income, God willing 💰

All you need to do is subscribe to my FREE Telegram channel 📢
Click "Join Channel" below, and I'll be waiting for you there ⭐"""

# ===== إدارة المستخدمين =====
def load_users():
    if os.path.exists(USERS_FILE):
        with open(USERS_FILE, "r") as f:
            return json.load(f)
    return {}

def save_users(users):
    with open(USERS_FILE, "w") as f:
        json.dump(users, f)

# ===== كيبورد =====
def get_keyboard(lang="ar"):
    if lang == "ar":
        return InlineKeyboardMarkup([
            [InlineKeyboardButton("🔔 اشترك في القناة", url=CHANNEL_LINK)],
            [InlineKeyboardButton("📢 اذهب إلى القناة", url=CHANNEL_LINK)],
            [InlineKeyboardButton("🌐 English", callback_data="lang_en")],
        ])
    else:
        return InlineKeyboardMarkup([
            [InlineKeyboardButton("🔔 Subscribe", url=CHANNEL_LINK)],
            [InlineKeyboardButton("📢 Go to Channel", url=CHANNEL_LINK)],
            [InlineKeyboardButton("🇸🇦 العربية", callback_data="lang_ar")],
        ])

# ===== إرسال الرسائل المجدولة =====
async def send_scheduled_messages(app, chat_id, lang):
    # رسالة 1 - بعد 3 ساعات
    await asyncio.sleep(3 * 3600)
    try:
        text = MSG_1_AR if lang == "ar" else MSG_1_EN
        await app.bot.send_video(chat_id=chat_id, video=VIDEO_1_FILE_ID, caption=text, reply_markup=get_keyboard(lang))
    except Exception as e:
        print(f"خطأ رسالة 1: {e}")

    # رسالة 2 - بعد 3 ساعات تانية
    await asyncio.sleep(3 * 3600)
    try:
        text = MSG_2_AR if lang == "ar" else MSG_2_EN
        await app.bot.send_video(chat_id=chat_id, video=VIDEO_2_FILE_ID, caption=text, reply_markup=get_keyboard(lang))
    except Exception as e:
        print(f"خطأ رسالة 2: {e}")

    # رسالة 3 - بعد 3 ساعات تالتة
    await asyncio.sleep(3 * 3600)
    try:
        text = MSG_3_AR if lang == "ar" else MSG_3_EN
        await app.bot.send_photo(chat_id=chat_id, photo=PHOTO_3_FILE_ID, caption=text, reply_markup=get_keyboard(lang))
    except Exception as e:
        print(f"خطأ رسالة 3: {e}")

    # تكرار كل يوم للأبد
    while True:
        await asyncio.sleep(15 * 3600)  # الباقي من اليوم
        try:
            text = MSG_1_AR if lang == "ar" else MSG_1_EN
            await app.bot.send_video(chat_id=chat_id, video=VIDEO_1_FILE_ID, caption=text, reply_markup=get_keyboard(lang))
        except Exception as e:
            print(f"خطأ تكرار 1: {e}")

        await asyncio.sleep(3 * 3600)
        try:
            text = MSG_2_AR if lang == "ar" else MSG_2_EN
            await app.bot.send_video(chat_id=chat_id, video=VIDEO_2_FILE_ID, caption=text, reply_markup=get_keyboard(lang))
        except Exception as e:
            print(f"خطأ تكرار 2: {e}")

        await asyncio.sleep(3 * 3600)
        try:
            text = MSG_3_AR if lang == "ar" else MSG_3_EN
            await app.bot.send_photo(chat_id=chat_id, photo=PHOTO_3_FILE_ID, caption=text, reply_markup=get_keyboard(lang))
        except Exception as e:
            print(f"خطأ تكرار 3: {e}")

# ===== أوامر البوت =====
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    first_name = user.first_name or "صديقي"
    chat_id = user.id

    users = load_users()
    is_new = str(chat_id) not in users

    if is_new:
        users[str(chat_id)] = {"lang": "ar", "joined": str(datetime.now())}
        save_users(users)

    lang = users[str(chat_id)].get("lang", "ar")
    msg = WELCOME_AR.format(name=first_name) if lang == "ar" else WELCOME_EN.format(name=first_name)
    await update.message.reply_text(msg, reply_markup=get_keyboard(lang))

    if is_new:
        asyncio.create_task(send_scheduled_messages(context.application, chat_id, lang))


async def get_file_id(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message.video:
        fid = update.message.video.file_id
        print(f"VIDEO FILE_ID: {fid}")
        await update.message.reply_text(f"VIDEO_ID: {fid}")
    elif update.message.photo:
        fid = update.message.photo[-1].file_id
        print(f"PHOTO FILE_ID: {fid}")
        await update.message.reply_text(f"PHOTO_ID: {fid}")


async def button_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    users = load_users()
    uid = str(query.from_user.id)

    try:
        if query.data == "lang_en":
            users.setdefault(uid, {})["lang"] = "en"
            save_users(users)
            await query.edit_message_reply_markup(reply_markup=get_keyboard("en"))
        elif query.data == "lang_ar":
            users.setdefault(uid, {})["lang"] = "ar"
            save_users(users)
            await query.edit_message_reply_markup(reply_markup=get_keyboard("ar"))
    except Exception:
        pass


async def channel_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [[InlineKeyboardButton("👑 انضم للقناة", url=CHANNEL_LINK)]]
    await update.message.reply_text("📢 قناة الفرعون للإشارات 🚀", reply_markup=InlineKeyboardMarkup(keyboard))


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("📋 الأوامر:\n/start - رسالة الترحيب\n/channel - رابط القناة\n/help - المساعدة")


# ===== تشغيل البوت =====
def main():
    app = Application.builder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help_command))
    app.add_handler(CommandHandler("channel", channel_command))
    app.add_handler(CallbackQueryHandler(button_callback))
    app.add_handler(MessageHandler(filters.VIDEO | filters.PHOTO, get_file_id))

    print("✅ بوت الفرعون شغال! 👑")
    app.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == "__main__":
    main()
