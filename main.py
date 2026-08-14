import os
import time
import random
import threading
from flask import Flask
import telebot
from instagrapi import Client

# ======================================================
# 1. خادم وهمي لإبقاء الخدمة تعمل مجاناً على Render
# ======================================================
app = Flask(__name__)

@app.route('/')
def home():
    return "Bot is active!"

def run_flask():
    port = int(os.environ.get("PORT", 8080))
    app.run(host='0.0.0.0', port=port)

threading.Thread(target=run_flask, daemon=True).start()

# ======================================================
# 2. إعدادات التوكن والجلسات (Sessions) للحسابات الـ 4
# ======================================================
TELEGRAM_BOT_TOKEN = "8968135906:AAHHOKLfvBXg7KQJD67UHGcvbtYkyO8h4Hc"

INSTAGRAM_SESSIONS = [
    {
        "id": "1",
        "sessionid": "63782954883%3ACxM77v17v2Ltg9%3A7%3AAYhbbTv34-_cXNca4JHmcBmAKfSplSWZr08qbdf9Uw"
    },
    {
        "id": "2",
        "sessionid": "62341132903%3ATAjb5e174j35cp%3A3%3AAYgMnhJfs6sO2w96F_ZA_I5_Nv3CuGlmfcIccJ2lPg"
    },
    {
        "id": "3",
        "sessionid": "57482313741%3A8HPZQ9DkH7X7Ba%3A14%3AAYjACFwcEQ4msSl8ugibRiPhjkYhndO_hu0rl_xnBw"
    },
    {
        "id": "4",
        "sessionid": "64103212632%3An2rRLg51vfY1Kz%3A11%3AAYi7VWV8fDd7T2jN9CjqjSs6893vXMuag4L1b0Sq-g"
    }
]

bot = telebot.TeleBot(TELEGRAM_BOT_TOKEN)

# ======================================================
# 3. استقبال روابط تليجرام وتنفيذ الإعجابات
# ======================================================
@bot.message_handler(commands=['start'])
def start_cmd(message):
    bot.reply_to(message, "أهلاً بك! أرسل لي رابط منشور إنستغرام لعمل الإعجابات تلقائياً.")

@bot.message_handler(func=lambda message: True)
def process_likes(message):
    post_url = message.text.strip()

    if "instagram.com" not in post_url:
        bot.reply_to(message, "⚠️ يرجى إرسال رابط منشور إنستغرام صحيح فقط.")
        return

    status_msg = bot.reply_to(message, "⏳ جاري بدء تنفيذ الإعجابات...")

    success_count = 0
    fail_count = 0
    total = len(INSTAGRAM_SESSIONS)

    for idx, acc in enumerate(INSTAGRAM_SESSIONS, 1):
        session_id = acc["sessionid"]
        acc_id = acc["id"]

        try:
            bot.edit_message_text(
                f"🔄 [{idx}/{total}] جاري الإعجاب عبر الحساب رقم #{acc_id}...",
                chat_id=message.chat.id,
                message_id=status_msg.message_id
            )

            cl = Client()
            # تسجيل الدخول عبر الجلسة بدون كلمة سر أو كود تحقق
            cl.login_by_sessionid(session_id)
            
            media_pk = cl.media_pk_from_url(post_url)
            cl.media_like(media_pk)

            success_count += 1
            # فاصل زمني لتفادي الحظر بين كل حساب والآخر
            time.sleep(random.randint(5, 10))

        except Exception as e:
            fail_count += 1
            print(f"[Error] الحساب #{acc_id} فشل: {e}")

    report = f"""✅ **اكتملت العملية!**

إعجابات ناجحة: {success_count}
إعجابات فاشلة: {fail_count}
إجمالي الحسابات: {total}"""

    bot.send_message(message.chat.id, report, parse_mode="Markdown")

# ======================================================
# 4. تشغيل البوت
# ======================================================
if __name__ == "__main__":
    bot.infinity_polling()
