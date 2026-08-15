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

# ======================================================
# 1. إعداد سجلات النظام (Logging)
# ======================================================
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# ======================================================
# 2. خادم Flask لإبقاء الخدمة نشطة (Keep-Alive)
# ======================================================
app = Flask(__name__)

@app.route('/')
def home():
    return "Bot is active and running!", 200

def run_flask():
    port = int(os.environ.get("PORT", 8080))
    app.run(host='0.0.0.0', port=port)

threading.Thread(target=run_flask, daemon=True).start()

# ======================================================
# 3. الإعدادات وقائمة الـ 30 كوكيز / الجلسات
# ======================================================
# ضع توكن بوت التلغرام الخاص بك هنا (أو استدعائه من متغيرات البيئة)
TELEGRAM_BOT_TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN", "ضغ_توكن_البوت_هنا")

# ضع الـ 30 كوكيز أو الـ sessionid هنا بين التنصيص
# يمكنك وضع الكوكيز كاملة أو الـ sessionid فقط وسيتكفل الكود باستخراجه
INSTAGRAM_COOKIES = [
    "57756971432%3As4EdL0v3oTqDsO%3A17%3AAYgyPeGkK-qK4WzUbfHFsOrZbaSbmgxGE0BPULD6Sg",
    "63782954883%3AlHVJedZoAgXEeT%3A24%3AAYiwxCJMBTW45wGVGVZORcULCVpXs3y3Sugq4WGJIQ;dpr=2.8125",
    "57314706707%3A3IwGZb6eGucmRm%3A12%3AAYib8Zc3DqNCb3o4hdobxPzj6jKRyub5T_Bq7vrA-w;dpr=2.8125",
    "62063778773%3AmFlQ7u0OTrBF0N%3A29%3AAYj4vPqX0HHWg3L-6MlfRtCLjaApgJxJRcQ-lnFIHw",
    "70143665267%3AHebl4wPWOE3STp%3A3%3AAYjFGCXincj16kSwgOZdrVT4C-Ghpr80idXDqDH1qw",
    "62264580737%3AI8UIprxwzbeaqm%3A18%3AAYhA_wnEM10aGUPxpJD8ZxJbB5LNL09Q1XzvuLJevQ",
    "ضع_الكوكيز_السابعة_هنا",
    "ضع_الكوكيز_الثامنة_هنا",
    "ضع_الكوكيز_التاسعة_هنا",
    "ضع_الكوكيز_العاشرة_هنا",
    "ضع_الكوكيز_11_هنا",
    "ضع_الكوكيز_12_هنا",
    "ضع_الكوكيز_13_هنا",
    "ضع_الكوكيز_14_هنا",
    "ضع_الكوكيز_15_هنا",
    "ضع_الكوكيز_16_هنا",
    "ضع_الكوكيز_17_هنا",
    "ضع_الكوكيز_18_هنا",
    "ضع_الكوكيز_19_هنا",
    "ضع_الكوكيز_20_هنا",
    "ضع_الكوكيز_21_هنا",
    "ضع_الكوكيز_22_هنا",
    "ضع_الكوكيز_23_هنا",
    "ضع_الكوكيز_24_هنا",
    "ضع_الكوكيز_25_هنا",
    "ضع_الكوكيز_26_هنا",
    "ضع_الكوكيز_27_هنا",
    "ضع_الكوكيز_28_هنا",
    "ضع_الكوكيز_29_هنا",
    "ضع_الكوكيز_30_هنا",
]

bot = telebot.TeleBot(TELEGRAM_BOT_TOKEN)

# ======================================================
# 4. دالة استخراج الـ sessionid تلقائياً
# ======================================================
def parse_session_id(cookie_input: str) -> str:
    """تستخرج قيمة sessionid سواء أدخلت الكوكيز كاملة أو الـ sessionid فقط"""
    cookie_input = cookie_input.strip()
    
    # إذا كانت النص يحتوي على sessionid=
    match = re.search(r'sessionid=([^;]+)', cookie_input)
    if match:
        return unquote(match.group(1)).strip()
    
    # إذا أدخل المستخدم الـ sessionid مباشرة
    return unquote(cookie_input).strip()

# ======================================================
# 5. أوامر البوت واستقبال الطلبات
# ======================================================
@bot.message_handler(commands=['start'])
def start_cmd(message):
    total_active = len([c for c in INSTAGRAM_COOKIES if "ضع_الكوكيز" not in c])
    bot.reply_to(
        message, 
        f"<b>أهلاً بك! 👋</b>\n\n"
        f"البوت جاهز للتنفيذ عبر <b>{total_active}</b> حساب/جلسة مجهزة.\n"
        f"أرسل رابط منشور إنستغرام للبدء في زيادة الإعجابات.",
        parse_mode="HTML"
    )

@bot.message_handler(func=lambda message: True)
def process_likes(message):
    post_url = message.text.strip()

    # التأكد من أن النص رابط إنستغرام
    if "instagram.com" not in post_url:
        bot.reply_to(message, "⚠️ يرجى إرسال رابط منشور إنستغرام صحيح.")
        return

    # تنظيف وتجهيز الجلسات الفعالة فقط
    active_sessions = [
        parse_session_id(c) for c in INSTAGRAM_COOKIES 
        if c and "ضع_الكوكيز" not in c
    ]

    if not active_sessions:
        bot.reply_to(message, "❌ لم يتم إضافة أي كوكيز أو جلسات في قائمة `INSTAGRAM_COOKIES` بعد!")
        return

    status_msg = bot.reply_to(message, "⏳ جاري بدء العملية والتفاعل مع المنشور...")

    success_count = 0
    fail_count = 0
    total = len(active_sessions)

    for idx, session_id in enumerate(active_sessions, start=1):
        try:
            # تحديث حالة البوت في التلغرام
            bot.edit_message_text(
                f"🔄 <b>[{idx}/{total}]</b> جاري إضافة إعجاب عبر الحساب رقم #{idx}...",
                chat_id=message.chat.id,
                message_id=status_msg.message_id,
                parse_mode="HTML"
            )

            # تسجيل الدخول عبر الـ Session ID والقيام بالإعجاب
            cl = Client()
            cl.login_by_sessionid(session_id)
            
            media_pk = cl.media_pk_from_url(post_url)
            cl.media_like(media_pk)

            success_count += 1
            logger.info(f"✅ نجح الإعجاب من الحساب #{idx}")

            # فاصل زمني عشوائي لحماية الحسابات من الحظر (بين 12 و 25 ثانية)
            time.sleep(random.randint(12, 25))

        except Exception as e:
            fail_count += 1
            logger.error(f"❌ فشل الحساب #{idx}: {e}")
            time.sleep(3)

    # تقرير النهاية
    report = (
        f"<b>✅ تم اكتمال العملية!</b>\n\n"
        f"❤️ <b>الإعجابات الناجحة:</b> {success_count}\n"
        f"❌ <b>الحسابات الفاشلة/المنتهية:</b> {fail_count}\n"
        f"👥 <b>إجمالي المحاولات:</b> {total}"
    )

    bot.send_message(message.chat.id, report, parse_mode="HTML")

# ======================================================
# 6. تشغيل البوت
# ======================================================
if __name__ == "__main__":
    logger.info("🤖 جاري تشغيل البوت...")
    bot.infinity_polling(timeout=10, long_polling_timeout=5)
