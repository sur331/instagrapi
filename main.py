import os
import re
import time
import random
import logging
import threading
from urllib.parse import unquote
from flask import Flask
import telebot
from instagrapi import Client

# =========================================================
# 1. إعداد سجلات النظام (Logging)
# =========================================================
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# =========================================================
# 2. إبقاء الخدمة نشطة (Keep-Alive) عبر Flask
# =========================================================
app = Flask(__name__)

@app.route('/')
def home():
    return "Bot is active and running!", 200

def run_flask():
    port = int(os.environ.get("PORT", 8080))
    app.run(host='0.0.0.0', port=port)

# تشغيل Flask في مسار جانبي (Thread)
threading.Thread(target=run_flask, daemon=True).start()

# =========================================================
# 3. الإعدادات وتحديد الكوكيز (3 حسابات)
# =========================================================
TELEGRAM_BOT_TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN", "8968135906:AAHHOKLfvBXg7KQJD67UHGcvbtYkyO8h4Hc")

# قائمة الكوكيز الخاصة بـ 3 حسابات إنستغرام
INSTAGRAM_COOKIES = [
    "62034526350%3AqnSRaJW6KuysB9%3A13%3AAYjOeOgFaoiPAeFMeEHE0PSjLZL8Rxzbq75Us4m7hw",
    "56820542293%3Auy6j5ZIoALPNtT%3A9%3AAYiNJWB-2kn6Sp8HzXVPhWQ6swpa5ur60GWBKZsuQg",
    "62683864812%3Ale5ZU7kPci7m4T%3A8%3AAYg102OA1iPGioUGYWskbSxPNo9t-MuHBjusrb0i1w", 
]

# =========================================================
# 4. تهيئة البوتات والاتصال
# =========================================================
bot = telebot.TeleBot(TELEGRAM_BOT_TOKEN)

def get_instagram_client(sessionid):
    """دالة لإنشاء جلسة إنستغرام باستخدام الكوكيز"""
    cl = Client()
    try:
        # تسجيل الدخول عن طريق sessionid
        cl.login_by_sessionid(sessionid)
        logger.info("تم تسجيل الدخول بنجاح إلى إنستغرام!")
        return cl
    except Exception as e:
        logger.error(f"فشل تسجيل الدخول باستخدام الكوكيز: {e}")
        return None

# =========================================================
# 5. أوامر بوت تليجرام (Handlers)
# =========================================================
@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "أهلاً بك! البوت يعمل بنجاح ومربوط بحسابات إنستغرام.")

if __name__ == '__main__':
    # اختبار تسجيل الدخول لأول حساب كوكيز في القائمة عند التشغيل
    if INSTAGRAM_COOKIES:
        cl = get_instagram_client(INSTAGRAM_COOKIES[0])
    
    logger.info("جاري تشغيل بوت تليجرام...")
    bot.infinity_polling()
