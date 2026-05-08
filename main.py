#!/usr/bin/env python3
"""
EL FER3OON BOT - بوت الفرعون للتداول مع Supabase
"""

import os
import asyncio
import threading
import requests
from datetime import datetime
from flask import Flask
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes, MessageHandler, filters

# ===== Flask للـ uptime =====
flask_app = Flask(__name__)

@flask_app.route('/')
def home():
    return "EL FER3OON BOT is running! 👑"

def run_flask():
    port = int(os.environ.get("PORT", 8080))
    flask_app.run(host="0.0.0.0", port=port)

# ===== إعدادات البوت =====
BOT_TOKEN = "8750815249:AAHtWLBgCg1rWXINj-HJCHt-AJeroGgcFWg"
CHANNEL_LINK = "https://t.me/+wm-XT1rWsHhkNjJk"
ADMIN_ID = 6656665257

# ===== Supabase =====
SUPABASE_URL = "https://asckmtsheshyzpqkgcbj.supabase.co"
SUPABASE_KEY = "sb_secret_dNfH3h3BhU-pcXQkU0cRHA_4VF3bsoI"
HEADERS = {
    "apikey": SUPABASE_KEY,
    "Authorization": f"Bearer {SUPABASE_KEY}",
    "Content-Type": "application/json"
}

def db_get_user(chat_id):
    r = requests.get(f"{SUPABASE_URL}/rest/v1/users?chat_id=eq.{chat_id}", headers=HEADERS)
    data = r.json()
    return data[0] if data else None

def db_add_user(chat_id, lang="ar"):
    requests.post(f"{SUPABASE_URL}/rest/v1/users", headers=HEADERS, json={
        "chat_id": chat_id, "lang": lang, "joined": datetime.now().isoformat()
    })

def db_update_lang(chat_id, lang):
    requests.patch(f"{SUPABASE_URL}/rest/v1/users?chat_id=eq.{chat_id}", headers=HEADERS, json={"lang": lang})

def db_get_all_users():
    r = requests.get(f"{SUPABASE_URL}/rest/v1/users?select=chat_id,lang", headers=HEADERS)
    return r.json()

def db_count_users():
    r = requests.get(f"{SUPABASE_URL}/rest/v1/users?select=count", headers={**HEADERS, "Prefer": "count=exact"})
    return r.headers.get("content-range", "0").split("/")[-1]

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
Many people started with us and today earn a decent daily income 🚀

Join the winners now 👑"""

MSG_2_AR = """🚀 تطبيق الفرعون للتداول صار جاهز! 👑
كل اللي تحتاجه بإيدك: إشارات دقيقة، تنبيهات سريعة، وتحليل يساعدك تدخل بأفضل وقت على Quotex 📊⚡
التطبيق معمول ليخلي التداول أبسط وأوضح حتى لو كنت مبتدئ 💡
ابدأ بخطوات صح، تابع الإشارات، وشوف الفرق بنفسك 💰🔥"""

MSG_2_EN = """🚀 EL FER3OON Trading App is ready! 👑
Accurate signals, fast alerts, and analysis to help you enter at the best time on Quotex 📊⚡
Designed to make trading simpler even if you're a beginner 💡
Start right, follow the signals, and see the difference 💰🔥"""

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
Start trading with more capital 👑"""

WELCOME_AR = """هلا {name}! 👋 معك الفرعون 👑
كتير مبسوط إني شايفك هون 🙏

أنا عندي خبرة في التداول، وحابب أشاركك كل شي تعلمته بأسلوب بسيط وواضح ✅

بنهاية المطاف رح تقدر تحقق دخل ثابت إن شاء الله 💰

اشترك بقناتي المجانية عالتلغرام 📢
اضغط على زر "انضم للقناة" تحت ⭐"""

WELCOME_EN = """Hello {name}! 👋 This is EL FER3OON 👑
So glad you're here! 🙏

I have trading experience and I want to share everything in a simple, clear way ✅

You'll be able to generate consistent income, God willing 💰

Subscribe to my FREE Telegram channel 📢
Click "Join Channel" below ⭐"""

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
    await asyncio.sleep(3 * 3600)
    try:
        text = MSG_1_AR if lang == "ar" else MSG_1_EN
        await app.bot.send_video(chat_id=chat_id, video=VIDEO_1_FILE_ID, caption=text, reply_markup=get_keyboard(lang))
    except Exception as e:
        print(f"خطأ رسالة 1: {e}")

    await asyncio.sleep(3 * 3600)
    try:
        text = MSG_2_AR if lang == "ar" else MSG_2_EN
        await app.bot.send_video(chat_id=chat_id, video=VIDEO_2_FILE_ID, caption=text, reply_markup=get_keyboard(lang))
    except Exception as e:
        print(f"خطأ رسالة 2: {e}")

    await asyncio.sleep(3 * 3600)
    try:
        text = MSG_3_AR if lang == "ar" else MSG_3_EN
        await app.bot.send_photo(chat_id=chat_id, photo=PHOTO_3_FILE_ID, caption=text, reply_markup=get_keyboard(lang))
    except Exception as e:
        print(f"خطأ رسالة 3: {e}")

    while True:
        await asyncio.sleep(15 * 3600)
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

# ===== Broadcast =====
async def broadcast_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id != ADMIN_ID:
        await update.message.reply_text("❌ مش مسموح")
        return

    users = db_get_all_users()
    if not users:
        await update.message.reply_text("❌ مفيش مستخدمين")
        return

    msg = update.message
    success = 0
    failed = 0

    await update.message.reply_text(f"📤 جاري الإرسال لـ {len(users)} مستخدم...")

    for user in users:
        uid = user["chat_id"]
        lang = user.get("lang", "ar")
        try:
            if msg.reply_to_message:
                rep = msg.reply_to_message
                if rep.text:
                    await context.bot.send_message(chat_id=uid, text=rep.text)
                elif rep.photo:
                    await context.bot.send_photo(chat_id=uid, photo=rep.photo[-1].file_id, caption=rep.caption or "")
                elif rep.video:
                    await context.bot.send_video(chat_id=uid, video=rep.video.file_id, caption=rep.caption or "")
            elif context.args:
                text = " ".join(context.args)
                await context.bot.send_message(chat_id=uid, text=text)
            success += 1
            await asyncio.sleep(0.05)
        except Exception:
            failed += 1

    await update.message.reply_text(f"✅ تم!\nنجح: {success}\nفشل: {failed}")


async def stats_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id != ADMIN_ID:
        return
    count = db_count_users()
    await update.message.reply_text(f"📊 إحصائيات البوت:\n👥 عدد المستخدمين: {count}")


# ===== أوامر البوت =====
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    first_name = user.first_name or "صديقي"
    chat_id = user.id

    existing = db_get_user(chat_id)
    is_new = existing is None

    if is_new:
        db_add_user(chat_id, "ar")
        lang = "ar"
    else:
        lang = existing.get("lang", "ar")

    msg = WELCOME_AR.format(name=first_name) if lang == "ar" else WELCOME_EN.format(name=first_name)
    await update.message.reply_text(msg, reply_markup=get_keyboard(lang))

    if is_new:
        asyncio.create_task(send_scheduled_messages(context.application, chat_id, lang))


async def get_file_id(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id != ADMIN_ID:
        return
    if update.message.video:
        await update.message.reply_text(f"VIDEO_ID: {update.message.video.file_id}")
    elif update.message.photo:
        await update.message.reply_text(f"PHOTO_ID: {update.message.photo[-1].file_id}")


async def button_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    uid = query.from_user.id
    user_name = query.from_user.first_name or "صديقي"

    try:
        if query.data == "lang_en":
            db_update_lang(uid, "en")
            await query.edit_message_text(WELCOME_EN.format(name=user_name), reply_markup=get_keyboard("en"))
        elif query.data == "lang_ar":
            db_update_lang(uid, "ar")
            await query.edit_message_text(WELCOME_AR.format(name=user_name), reply_markup=get_keyboard("ar"))
    except Exception as e:
        print(f"خطأ callback: {e}")


async def channel_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [[InlineKeyboardButton("👑 انضم للقناة", url=CHANNEL_LINK)]]
    await update.message.reply_text("📢 قناة الفرعون للإشارات 🚀", reply_markup=InlineKeyboardMarkup(keyboard))


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("📋 الأوامر:\n/start - رسالة الترحيب\n/channel - رابط القناة\n/broadcast نص - إرسال للكل\n/stats - إحصائيات\n/help - المساعدة")


# ===== تشغيل البوت =====
def main():
    flask_thread = threading.Thread(target=run_flask, daemon=True)
    flask_thread.start()

    app = Application.builder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help_command))
    app.add_handler(CommandHandler("channel", channel_command))
    app.add_handler(CommandHandler("broadcast", broadcast_command))
    app.add_handler(CommandHandler("stats", stats_command))
    app.add_handler(CallbackQueryHandler(button_callback))
    app.add_handler(MessageHandler(filters.VIDEO | filters.PHOTO, get_file_id))

    print("✅ بوت الفرعون شغال! 👑")
    app.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == "__main__":
    main()
