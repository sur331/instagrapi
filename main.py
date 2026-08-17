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
    "62034526350%3AqnSRaJW6KuysB9%3A13%3AAYjOeOgFaoiPAeFMeEHE0PSjLZL8Rxzbq75Us4m7hw",
    "62060842648%3AmiYohBRpIrqgnH%3A25%3AAYiIB3Mjrwr2X9pCz8cxIsF29YQYDocazJ92DEqovg",
    "62683864812%3Ale5ZU7kPci7m4T%3A8%3AAYg102OA1iPGioUGYWskbSxPNo9t-MuHBjusrb0i1w",
    "2057773235%3Ai9kRhF3mSpnEDZ%3A14%3AAYg62_HSY7MdtuaB0k_MzOXUnVa8OkSc1BAElYsafg",
    "61631894758%3AOCPejtMmjZyrhv%3A11%3AAYgwnJZ1U_8MyRlgKyhKpqj65R1fvEOs8Z7NHk_1Cw",
    "2272563687%3Ay9oWx178aAFqa5%3A18%3AAYivCvM2ZY8Bdb8WeOWILf2336yRrz8JB_9v4cxHVg",
    "57138853589%3ARiI2BVsPaAyVPq%3A20%3AAYjxnX5T6nRvnfc9uvaKbgvdm3s9wk9cdlA7PrCByw",
    "56076138485%3APwmobsfCA7BVxs%3A23%3AAYh5pQKFs2k2DxCTHATwYNvF3hkPrbKoSvgyqHuWvQ",
    "57314706707%3AMGvdgmvYvpfFVB%3A24%3AAYjxc1Y2OYPKFc8rjHtn3wreDsEC5_Uggb-3p60UnA",
    "63782954883%3AiRHY88Hxy6mxN5%3A15%3AAYjSAiLlqIpfgzgnLeCrDiHugBPpNjJs1g0fxi5B_g",
    "14335540890%3AldVy9HIcjImzDK%3A29%3AAYgMck_K64zvDIl3H95TrHZ9GFsb2t__qM47YLUw0g",
    "63782954883%3AiRHY88Hxy6mxN5%3A15%3AAYjSAiLlqIpfgzgnLeCrDiHugBPpNjJs1g0fxi5B_g",
    "56842096284%3AsI2fSe7qlV4SJ2%3A17%3AAYjX7mhLH09kBvmhsROFf77m12uzUa8JQkAWh2fRRQ",
    "62001265034%3AO46kzGNGZQqRxl%3A5%3AAYjfLbM5fQvVMaKT41AHO93uA2BlNLa7h2MOZYBczA",
    "57673072874%3AokOgBfnIWwbfKn%3A17%3AAYg40Og3DY-GGuhc0uUVn_pWBOhnSZ3pTHsb_udwt",
    "56408794683%3A3Ot3s2Z1CYw7GC%3A23%3AAYhuoeNbY7Fx8PCK5DW47QZ759YQVld2S_yhkkz_XQ",
    "56408794683%3A3Ot3s2Z1CYw7GC%3A23%3AAYhuoeNbY7Fx8PCK5DW47QZ759YQVld2S_yhkkz_XQ",
    "56257999210%3AKjDTSPHpeB3WEo%3A26%3AAYiK6Z-32klERtYBa3BJd4FHxj7Z0TrBOm_9y1sOyw",
    "59090497779%3AJobRLcwZgISiwA%3A25%3AAYiF2r8OlzmeYNNGYwtVf4Db8vBQvhBosYMpTT9S9g",
    "56085393163%3AO6S7xGe9bFay23%3A6%3AAYjEHOPtHLmvDQOpShC_aXVhp4lo3oCHz-1s_hAksA",
    "57170083165%3AzXMwz7yZBatrp1%3A26%3AAYj9uKDrd1UpfzJJhq76P732GDWoqvz6HswRk-ZUCQ",
    "2042853691%3AOCqmHbpVGmXrll%3A14%3AAYisRMIRRMnoDPbi5xwE5kHh4f2g_c5bFlnemyIZ9w",
    "2062314802%3AS6REsbBrPFZqMI%3A8%3AAYjrM3-7c9zGtGjEMsw-s545UMkVR0l2LB7f87XmaA",
    "57139805509%3AvKsxrYJxX9uF64%3A2%3AAYhnx6EAemFPl9V2YZcaEug86A9K4JYV1d2mBWePbg",
    "57646989006%3A5Ydutmsr1SwSbh%3A19%3AAYgkO7VwIVyOF6Y7Gec5MTnOE0f0fg9-uh-8pdXpMA",
    "63337956754%3ANxsmb1L0SfgGAp%3A28%3AAYhy_9e19U5f-_Mib2ekkccnTP9eqpqw0GR_FtOvww",
    "6987897237%3AN59BT1U0C289IJ%3A24%3AAYjZfqXBozeDe8tU2c9IZDfSsZpSqFhAiVwXO4Mq0Q",
    "64160978150%3Af8LtuRFUmUwHvH%3A9%3AAYjvZ72eNXvfLn3ba8gWMkiSrNO47Va8DtHJQC_dOA",
    "7478210279%3AqUXTRWAjolYeop%3A19%3AAYiBiM52u1mz5c4zZsuBbXX1eSkC5WVlVNHsnCOc1w",
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
