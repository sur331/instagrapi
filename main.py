import os
import time
import random
import threading
from flask import Flask
import telebot
from instagrapi import Client

# ======================================================
# 1. خادم وهمي لمنع إغلاق الخدمة المجانية في Render
# ======================================================
app = Flask(__name__)

@app.route('/')
def home():
    return "Bot is running!"

def run_flask():
    port = int(os.environ.get("PORT", 8080))
    app.run(host='0.0.0.0', port=port)

threading.Thread(target=run_flask, daemon=True).start()

# ======================================================
# 2. إعدادات البوت والحسابات
# ======================================================
TELEGRAM_BOT_TOKEN = "8968135906:AAHHOKLFvBXg7KQJD67UHGcvbtYkyO8h4Hc"

INSTAGRAM_ACCOUNTS = [
    {"username": "oiitaop", "password": "suR_1212"},
    {"username": "omanianfi", "password": "suR_1212"},
]

bot = telebot.TeleBot(TELEGRAM_BOT_TOKEN)

# ======================================================
# 3. استقبال الرابط وتنفيذ اللايكات
# ======================================================
@bot.message_handler(commands=['start'])
def start_cmd(message):
    bot.reply_to(message, "أرسل لي رابط المنشور الآن لعمل الإعجابات.")

@bot.message_handler(func=lambda message: True)
def process_likes(message):
    post_url = message.text.strip()

    # التحقق من أن النص المنسوخ هو رابط إنستغرام
    if "instagram.com" not in post_url:
        bot.reply_to(message, "الرجاء إرسال رابط منشور إنستغرام فقط.")
        return

    status_msg = bot.reply_to(message, "⏳ جاري البدء في تنفيذ الإعجابات...")

    success_count = 0
    fail_count = 0
    total = len(INSTAGRAM_ACCOUNTS)

    for idx, acc in enumerate(INSTAGRAM_ACCOUNTS, 1):
        username = acc["username"]
        password = acc["password"]

        try:
            bot.edit_message_text(
                f"🔄 [{idx}/{total}] جاري الإعجاب عبر الحساب: @{username}",
                chat_id=message.chat.id,
                message_id=status_msg.message_id
            )

            cl = Client()
            cl.login(username, password)
            media_pk = cl.media_pk_from_url(post_url)
            cl.media_like(media_pk)

            success_count += 1
            time.sleep(random.randint(10, 15))

        except Exception as e:
            fail_count += 1
            print(f"[Error] الحساب {username} فشل: {e}")

    report = f"""✅ اكتملت العملية!

الإعجابات الناجحة: {success_count}
الإعجابات الفاشلة: {fail_count}
إجمالي الحسابات: {total}"""

    bot.send_message(message.chat.id, report)

# ======================================================
# 4. تشغيل البوت
# ======================================================
if __name__ == "__main__":
    bot.infinity_polling()
