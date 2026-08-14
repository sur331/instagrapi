import os
import time
import random
import threading
from flask import Flask
import telebot
from instagrapi import Client

# ======================================================
# 0. خادم ويب وهمي لإبقاء Render مجانياً وبدون إغلاق
# ======================================================
app = Flask(__name__)

@app.route('/')
def home():
    return "Bot is running fine!"

def run_flask():
    # Render يمرر المنفذ عبر متغير البيئة PORT تلقائياً
    port = int(os.environ.get("PORT", 8080))
    app.run(host='0.0.0.0', port=port)

# تشغيل خادم الويب في مسار مستقل (Thread)
threading.Thread(target=run_flask, daemon=True).start()

# ======================================================
# 1. الإعدادات والبيانات
# ======================================================
TELEGRAM_BOT_TOKEN = "8968135906:AAHHOKLFvBXg7KQJD67UHGcvbtYkyO8h4Hc"

INSTAGRAM_ACCOUNTS = [
    {"username": "oiitaop", "password": "suR_1212"},
    {"username": "omanianfi", "password": "suR_1212"},
]

bot = telebot.TeleBot(TELEGRAM_BOT_TOKEN)

# ======================================================
# 2. الأوامر والرسائل
# ======================================================
@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    welcome_text = """أهلاً بك في بوت الإعجابات التلقائية!

قم بإرسال رابط منشور إنستغرام للبدء في تنفيذ الإعجابات من حساباتك المجهزة.

مثال للرابط:
https://www.instagram.com/p/CgZa8drK52K/?igsh=bmYxOGdreXV0MGN2"""
    bot.reply_to(message, welcome_text)

@bot.message_handler(func=lambda message: True)
def process_likes(message):
    post_url = message.text.strip()

    if "instagram.com" not in post_url:
        bot.reply_to(message, "خطأ: يرجى إرسال رابط منشور إنستغرام صحيح.")
        return

    status_msg = bot.reply_to(message, "⏳ جاري بدء عملية الإعجابات...")

    success_count = 0
    fail_count = 0
    total_accounts = len(INSTAGRAM_ACCOUNTS)

    for idx, acc in enumerate(INSTAGRAM_ACCOUNTS, 1):
        username = acc["username"]
        password = acc["password"]

        try:
            bot.edit_message_text(
                f"🔄 [{idx}/{total_accounts}] جاري الإعجاب عبر الحساب: @{username}",
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

    report = f"""اكتملت العملية!

إعجابات ناجحة: {success_count}
إعجابات فاشلة: {fail_count}
إجمالي الحسابات: {total_accounts}"""

    bot.send_message(message.chat.id, report)

# ======================================================
# 3. تشغيل البوت
# ======================================================
if __name__ == "__main__":
    print("🤖 البوت يعمل الآن ويستقبل الرسائل...")
    bot.infinity_polling()
