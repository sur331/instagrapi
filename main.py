import os
import time
import random
import threading
import urllib.parse
from flask import Flask
import telebot
from instagrapi import Client

# ======================================================
# 1. خادم وهمي لإبقاء الخدمة تعمل مجاناً على Render
# ======================================================
app = Flask(__name__)

@app.route('/')
def home():
    return "Bot is running with Updated Sessions!"

def run_flask():
    port = int(os.environ.get("PORT", 8080))
    app.run(host='0.0.0.0', port=port)

threading.Thread(target=run_flask, daemon=True).start()

# ======================================================
# 2. إعدادات التوكن والجلسات (sessions المحدثة)
# ======================================================
TELEGRAM_BOT_TOKEN = "8968135906:AAHHOKLfvBXg7KQJD67UHGcvbtYkyO8h4Hc"

# قائمة كوكيز الحسابات المحدثة
RAW_SESSIONS = [
    "62034526350%3ACuVs63bYudUYMm%3A13%3AAYizI_42s1zqNxdm8B8-vVWK-PbCYWQE9nlzpsK5eA",
    "56820542293%3AazmuOda6rNBAPg%3A28%3AAYhrHFDELCJIUSAafXnuR1GS03mgGltzKwkUIGWNrw", 
    "62057773235%3Ai9kRhF3mSpnEDZ%3A14%3AAYg62_HSY7MdtuaB0k_MzOXUnVa8OkSc1BAElYsafg",
    "61631894758%3AOCPejtMmjZyrhv%3A11%3AAYgwnJZ1U_8MyRlgKyhKpqj65R1fvEOs8Z7NHk_1Cw",
    "62272563687%3Ay9oWx178aAFqa5%3A18%3AAYivCvM2ZY8Bdb8WeOWILf2336yRrz8JB_9v4cxHVg",
    "57138853589%3ARiI2BVsPaAyVPq%3A20%3AAYjxnX5T6nRvnfc9uvaKbgvdm3s9wk9cdlA7PrCByw",
    "56076138485%3APwmobsfCA7BVxs%3A23%3AAYh5pQKFs2k2DxCTHATwYNvF3hkPrbKoSvgyqHuWvQ",
    "56076138485%3APwmobsfCA7BVxs%3A23%3AAYh5pQKFs2k2DxCTHATwYNvF3hkPrbKoSvgyqHuWvQ",
    "57314706707%3AMGvdgmvYvpfFVB%3A24%3AAYjxc1Y2OYPKFc8rjHtn3wreDsEC5_Uggb-3p60UnA",
    "63782954883%3AiRHY88Hxy6mxN5%3A15%3AAYjSAiLlqIpfgzgnLeCrDiHugBPpNjJs1g0fxi5B_g",
    "63782954883%3AiRHY88Hxy6mxN5%3A15%3AAYjSAiLlqIpfgzgnLeCrDiHugBPpNjJs1g0fxi5B_g",
    "56842096284%3AsI2fSe7qlV4SJ2%3A17%3AAYjX7mhLH09kBvmhsROFf77m12uzUa8JQkAWh2fRRQ",
    "62001265034%3AO46kzGNGZQqRxl%3A5%3AAYjfLbM5fQvVMaKT41AHO93uA2BlNLa7h2MOZYBczA",
    "65542576846%3AYNqV7DiUG9BrdO%3A3%3AAYg9oqAW3n0sVtmirDNbHU76Y-unurPwbOMfrx_cBg",
    "57673072874%3AokOgBfnIWwbfKn%3A17%3AAYg40Og3DY-GGuhc0uUVn_pWBOhnSZ3pTHsb_udwt",
    "56408794683%3A3Ot3s2Z1CYw7GC%3A23%3AAYhuoeNbY7Fx8PCK5DW47QZ759YQVld2S_yhkkz_XQ",
    "56257999210%3AKjDTSPHpeB3WEo%3A26%3AAYiK6Z-32klERtYBa3BJd4FHxj7Z0TrBOm_9y1sOyw",
    "59090497779%3AJobRLcwZgISiwA%3A25%3AAYiF2r8OlzmeYNNGYwtVf4Db8vBQvhBosYMpTT9S9g",
    "56085393163%3AO6S7xGe9bFay23%3A6%3AAYjEHOPtHLmvDQOpShC_aXVhp4lo3oCHz-1s_hAksA",
    "57170083165%3AzXMwz7yZBatrp1%3A26%3AAYj9uKDrd1UpfzJJhq76P732GDWoqvz6HswRk-ZUCQ",
    "62042853691%3AOCqmHbpVGmXrll%3A14%3AAYisRMIRRMnoDPbi5xwE5kHh4f2g_c5bFlnemyIZ9w",
    "62062314802%3AS6REsbBrPFZqMI%3A8%3AAYjrM3-7c9zGtGjEMsw-s545UMkVR0l2LB7f87XmaA",
    "57139805509%3AvKsxrYJxX9uF64%3A2%3AAYhnx6EAemFPl9V2YZcaEug86A9K4JYV1d2mBWePbg",
    "57646989006%3A5Ydutmsr1SwSbh%3A19%3AAYgkO7VwIVyOF6Y7Gec5MTnOE0f0fg9-uh-8pdXpMA",
    "56257999210%3ADavNhNxCHAKF3O%3A5%3AAYh5Yb6qE8Mw7e8DTmGlKrTZ7CGU7XDHP4wtzoajNw",
    "63337956754%3ANxsmb1L0SfgGAp%3A28%3AAYhy_9e19U5f-_Mib2ekkccnTP9eqpqw0GR_FtOvww",
    "56987897237%3AN59BT1U0C289IJ%3A24%3AAYjZfqXBozeDe8tU2c9IZDfSsZpSqFhAiVwXO4Mq0Q",
    "64160978150%3Af8LtuRFUmUwHvH%3A9%3AAYjvZ72eNXvfLn3ba8gWMkiSrNO47Va8DtHJQC_dOA",
    "57478210279%3AqUXTRWAjolYeop%3A19%3AAYiBiM52u1mz5c4zZsuBbXX1eSkC5WVlVNHsnCOc1w"
]

bot = telebot.TeleBot(TELEGRAM_BOT_TOKEN)

# ======================================================
# 3. معالجة الطلبات
# ======================================================
@bot.message_handler(commands=['start'])
def start_cmd(message):
    bot.reply_to(message, f"أهلاً بك! البوت متصل ومستعد للتنفيذ عبر {len(RAW_SESSIONS)} حساباً.\nأرسل رابط المنشور للبدء.")

@bot.message_handler(func=lambda message: True)
def process_likes(message):
    post_url = message.text.strip()

    if "instagram.com" not in post_url:
        bot.reply_to(message, "⚠️ يرجى إرسال رابط منشور إنستغرام صحيح.")
        return

    status_msg = bot.reply_to(message, "⏳ جاري بدء التفاعل والتنفيذ عبر الحسابات...")

    success_count = 0
    fail_count = 0
    total = len(RAW_SESSIONS)

    for idx, raw_session in enumerate(RAW_SESSIONS, 1):
        clean_session = urllib.parse.unquote(raw_session).strip()

        try:
            bot.edit_message_text(
                f"🔄 [{idx}/{total}] جاري التفاعل عبر الحساب #{idx}...",
                chat_id=message.chat.id,
                message_id=status_msg.message_id
            )

            cl = Client()
            cl.login_by_sessionid(clean_session)
            
            media_pk = cl.media_pk_from_url(post_url)
            cl.media_like(media_pk)

            success_count += 1
            time.sleep(random.randint(15, 30))

        except Exception as e:
            fail_count += 1
            print(f"[خطأ] الحساب #{idx}: {e}")
            time.sleep(3)

    report = f"""✅ **تم اكتمال العملية!**

❤️ ناجحة: {success_count}
❌ فاشلة: {fail_count}
👥 الإجمالي: {total}"""

    bot.send_message(message.chat.id, report, parse_mode="Markdown")

# ======================================================
# 4. تشغيل البوت
# ======================================================
if __name__ == "__main__":
    bot.infinity_polling()
