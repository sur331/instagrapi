import os
import time
import random
import logging
import threading
from flask import Flask
import telebot
from instagrapi import Client

# =========================================================
# 1. إعداد السجلات (Logging)
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

threading.Thread(target=run_flask, daemon=True).start()

# =========================================================
# 3. الإعدادات وقائمة 33 كوكيز
# =========================================================
TELEGRAM_BOT_TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN", "ضع_التوكين_هنا")

# ضع الـ 33 Session ID الخاصة بحساباتك هنا
INSTAGRAM_COOKIES = [
    "2683864812%3Ale5ZU7kPci7m4T%3A8%3AAYg102OA1iPGioUGYWskbSxPNo9t-MuHBjusrb0i1w",
    "56820542293%3Auy6j5ZIoALPNtT%3A9%3AAYiNJWB-2kn6Sp8HzXVPhWQ6swpa5ur60GWBKZsuQg",
    "62034526350%3AqnSRaJW6KuysB9%3A13%3AAYjOeOgFaoiPAeFMeEHE0PSjLZL8Rxzbq75Us4m7hw",
    "57478210279%3AqUXTRWAjolYeop%3A19%3AAYiBiM52u1mz5c4zZsuBbXX1eSkC5WVlVNHsnCOc1w",
    "4160978150%3Af8LtuRFUmUwHvH%3A9%3AAYjvZ72eNXvfLn3ba8gWMkiSrNO47Va8DtHJQC_dOA",
    "56987897237%3AN59BT1U0C289IJ%3A24%3AAYjZfqXBozeDe8tU2c9IZDfSsZpSqFhAiVwXO4Mq0Q",
    "63337956754%3ANxsmb1L0SfgGAp%3A28%3AAYhy_9e19U5f-_Mib2ekkccnTP9eqpqw0GR_FtOvww",
    "57646989006%3A5Ydutmsr1SwSbh%3A19%3AAYgkO7VwIVyOF6Y7Gec5MTnOE0f0fg9-uh-8pdXpMA",
    "57139805509%3AvKsxrYJxX9uF64%3A2%3AAYhnx6EAemFPl9V2YZcaEug86A9K4JYV1d2mBWePbg",
    "2062314802%3AS6REsbBrPFZqMI%3A8%3AAYjrM3-7c9zGtGjEMsw-s545UMkVR0l2LB7f87XmaA",
    "62042853691%3AOCqmHbpVGmXrll%3A14%3AAYisRMIRRMnoDPbi5xwE5kHh4f2g_c5bFlnemyIZ9w",
    "57170083165%3AzXMwz7yZBatrp1%3A26%3AAYj9uKDrd1UpfzJJhq76P732GDWoqvz6HswRk-ZUCQ",
    "56085393163%3AO6S7xGe9bFay23%3A6%3AAYjEHOPtHLmvDQOpShC_aXVhp4lo3oCHz-1s_hAksA",
    "59090497779%3AJobRLcwZgISiwA%3A25%3AAYiF2r8OlzmeYNNGYwtVf4Db8vBQvhBosYMpTT9S9g",
    "56257999210%3AKjDTSPHpeB3WEo%3A26%3AAYiK6Z-32klERtYBa3BJd4FHxj7Z0TrBOm_9y1sOyw",
    "56408794683%3A3Ot3s2Z1CYw7GC%3A23%3AAYhuoeNbY7Fx8PCK5DW47QZ759YQVld2S_yhkkz_XQ",
    "56408794683%3A3Ot3s2Z1CYw7GC%3A23%3AAYhuoeNbY7Fx8PCK5DW47QZ759YQVld2S_yhkkz_XQ",
    "57673072874%3AokOgBfnIWwbfKn%3A17%3AAYg40Og3DY-GGuhc0uUVn_pWBOhnSZ3pTHsb_udwt",
    "62001265034%3AO46kzGNGZQqRxl%3A5%3AAYjfLbM5fQvVMaKT41AHO93uA2BlNLa7h2MOZYBczA",
    "56842096284%3AsI2fSe7qlV4SJ2%3A17%3AAYjX7mhLH09kBvmhsROFf77m12uzUa8JQkAWh2fRRQ",
    "63782954883%3AiRHY88Hxy6mxN5%3A15%3AAYjSAiLlqIpfgzgnLeCrDiHugBPpNjJs1g0fxi5B_g",
    "63782954883%3AiRHY88Hxy6mxN5%3A15%3AAYjSAiLlqIpfgzgnLeCrDiHugBPpNjJs1g0fxi5B_g",
    "63782954883%3AiRHY88Hxy6mxN5%3A15%3AAYjSAiLlqIpfgzgnLeCrDiHugBPpNjJs1g0fxi5B_g",
    "57314706707%3AMGvdgmvYvpfFVB%3A24%3AAYjxc1Y2OYPKFc8rjHtn3wreDsEC5_Uggb-3p60UnA",
    "56076138485%3APwmobsfCA7BVxs%3A23%3AAYh5pQKFs2k2DxCTHATwYNvF3hkPrbKoSvgyqHuWvQ",
    "56076138485%3APwmobsfCA7BVxs%3A23%3AAYh5pQKFs2k2DxCTHATwYNvF3hkPrbKoSvgyqHuWvQ",
    "57138853589%3ARiI2BVsPaAyVPq%3A20%3AAYjxnX5T6nRvnfc9uvaKbgvdm3s9wk9cdlA7PrCByw",
    "62272563687%3Ay9oWx178aAFqa5%3A18%3AAYivCvM2ZY8Bdb8WeOWILf2336yRrz8JB_9v4cxHVg",
    "61631894758%3AOCPejtMmjZyrhv%3A11%3AAYgwnJZ1U_8MyRlgKyhKpqj65R1fvEOs8Z7NHk_1Cw",
    "62057773235%3Ai9kRhF3mSpnEDZ%3A14%3AAYg62_HSY7MdtuaB0k_MzOXUnVa8OkSc1BAElYsafg",
    "14335540890%3AldVy9HIcjImzDK%3A29%3AAYgMck_K64zvDIl3H95TrHZ9GFsb2t__qM47YLUw0g",
    "62060842648%3AmiYohBRpIrqgnH%3A25%3AAYiIB3Mjrwr2X9pCz8cxIsF29YQYDocazJ92DEqovg",
    
]

bot = telebot.TeleBot(TELEGRAM_BOT_TOKEN)

# =========================================================
# 4. دوال التعامل مع إنستغرام
# =========================================================
def get_instagram_client(session_id):
    cl = Client()
    try:
        cl.login_by_sessionid(session_id)
        return cl
    except Exception as e:
        logger.error(f"فشل الجلسة {session_id[:8]}... : {e}")
        return None

def extract_media_id(url):
    try:
        cl = Client()
        return cl.media_pk_from_url(url)
    except Exception as e:
        logger.error(f"خطأ استخراج المعرف: {e}")
        return None

def send_likes_job(post_url, chat_id):
    media_id = extract_media_id(post_url)
    if not media_id:
        bot.send_message(chat_id, "❌ متعذر جلب المنشور، تأكد أن الرابط صحيح والحساب عام.")
        return

    total_accounts = len(INSTAGRAM_COOKIES)
    bot.send_message(
        chat_id, 
        f"🚀 **بدء العملية:**\n- عدد الحسابات: {total_accounts}\n- الفاصل الزمني: 15-30 ثانية عشوائي لحماية الحسابات."
    )

    success_count = 0
    fail_count = 0

    for idx, session_id in enumerate(INSTAGRAM_COOKIES, 1):
        cl = get_instagram_client(session_id)
        
        if cl:
            try:
                cl.media_like(media_id)
                success_count += 1
                logger.info(f"[{idx}/{total_accounts}] تم الإعجاب بنجاح.")
            except Exception as e:
                fail_count += 1
                logger.error(f"[{idx}/{total_accounts}] فشل الإعجاب: {e}")
        else:
            fail_count += 1

        # تطبيق المهلة الزمنية بين الحسابات
        if idx < total_accounts:
            delay = random.randint(1, 10)
            logger.info(f"انتظار {delay} ثانية...")
            time.sleep(delay)

    report = (
        f"🏁 **انتهت العملية!**\n\n"
        f"👍 إعجابات ناجحة: {success_count}\n"
        f"❌ إعجابات فاشلة: {fail_count}\n"
        f"📊 الإجمالي: {total_accounts}"
    )
    bot.send_message(chat_id, report, parse_mode="Markdown")

# =========================================================
# 5. أوامر البوت
# =========================================================
@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    bot.reply_to(message, "مرحباً! أرسل رابط المنشور لعمل الإعجابات عبر الـ 32 حساباً.")

@bot.message_handler(func=lambda message: True)
def handle_message(message):
    url = message.text.strip()
    if "instagram.com" in url:
        bot.reply_to(message, "⏳ جاري بدء تنفيذ الإعجابات...")
        threading.Thread(target=send_likes_job, args=(url, message.chat.id)).start()
    else:
        bot.reply_to(message, "⚠️ يرجى إرسال رابط إنستغرام صحيح.")

# =========================================================
# 6. تشغيل البوت
# =========================================================
if __name__ == "__main__":
    logger.info("تم تشغيل البوت...")
    bot.infinity_polling()
