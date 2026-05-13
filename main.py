#!/usr/bin/env python3
"""
EL FER3OON BOT - مرحلة أولى: جمع file_id للميديا
ابعت الفيديوهات والصور للبوت وهيرد بالـ file_id
"""

import os
import threading
from flask import Flask
from telegram import Update
from telegram.ext import Application, MessageHandler, ContextTypes, filters

# ===== Flask للـ uptime =====
flask_app = Flask(__name__)

@flask_app.route('/')
def home():
    return "EL FER3OON BOT - جاهز لاستقبال الملفات 👑"

def run_flask():
    port = int(os.environ.get("PORT", 8080))
    flask_app.run(host="0.0.0.0", port=port)

# ===== إعدادات =====
BOT_TOKEN = "8843707521:AAFG9Nf1-1SosYI85uHtKlKv62WUJgpOFyM"
ADMIN_ID = 6656665257

# ===== handler للميديا =====
async def get_file_id(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id != ADMIN_ID:
        return

    msg = update.message

    if msg.video:
        file_id = msg.video.file_id
        await msg.reply_text(f"✅ VIDEO_FILE_ID:\n`{file_id}`", parse_mode="Markdown")

    elif msg.photo:
        file_id = msg.photo[-1].file_id
        await msg.reply_text(f"✅ PHOTO_FILE_ID:\n`{file_id}`", parse_mode="Markdown")

    elif msg.document:
        file_id = msg.document.file_id
        await msg.reply_text(f"✅ DOCUMENT_FILE_ID:\n`{file_id}`", parse_mode="Markdown")

    else:
        await msg.reply_text("❌ ابعت فيديو أو صورة فقط")

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "👑 أهلاً يا أدمن!\nابعتلي الفيديوهات والصور وأنا هرد بالـ file_id بتاع كل واحد."
    )

# ===== تشغيل البوت =====
def main():
    flask_thread = threading.Thread(target=run_flask, daemon=True)
    flask_thread.start()

    from telegram.ext import CommandHandler
    app = Application.builder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.VIDEO | filters.PHOTO | filters.Document.ALL, get_file_id))

    print("✅ بوت جمع الملفات شغال! ابعت الميديا دلوقتي 👑")
    app.run_polling()

if __name__ == "__main__":
    main()
