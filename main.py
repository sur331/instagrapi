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
    "63782954883%3A3MZx6ldRJyyqDJ%3A27%3AAYjJq1m74E5DNGRmMPDiZYtow49U_PAgWrQ2cNu9Cw",
    "62063778773%3AUfaJJcAQZoM6Gp%3A20%3AAYh6Df22TmsmJC94QFfOE28vhcYKnuFNAd_SVllmrg;dpr=2.8125",
    "57314706707%3AGR6bXrCfhOhuzB%3A12%3AAYhpGSCAkXh1k_rtE9J3jPli61XiHv5PKZZUG1lTnA",
    "70143665267%3AX72riH8cmE3yN8%3A11%3AAYhnKLdiuDP29O-_yqE9XRcouxEJIUHEZMFKOoYusQ",
    "57314706707%3AuwxOabNjhM0jTq%3A12%3AAYhGbGwrPRPGNea_c03pNckMPuusw1yNt2UmsQNY9w",
    "62299992885%3AuUqGqPOdPm4Zqa%3A16%3AAYg_kDe3jqBhiZZ-V-H5v2rXrR0quy7YZTnL21oe9g",
    "62299992885%3Ayz2cxvs3myY19K%3A16%3AAYjhK_2hDG0xFem92DPkmANq-7Aa8N9TTwRrm5DfVQ",
    "52290524344%3Afv9FBKR1aGqStr%3A19%3AAYiAceRHe2zxj7k4-1jk9c0KC0ahSPuDvWZrtA1W_g",
    "62503042404%3AVa1lc39LUErVkf%3A21%3AAYhiffI5bs94kDY3xRODa8bQHVW_NJgyDiMcFJdbjA",
    "52290524344%3Aifl0DyzCgmuIvN%3A19%3AAYguyyD9zgRXpKKbW-OL7Wy-9iBVoQxWIbSLHor5kw",
    "62034526350%3AOWmtZYmh1FrXb7%3A13%3AAYgNbYVchA22osR0WqIjCvPA-KYD6GjnsbQ6QlZwdw",
    "56959999287%3ADkudqo5JNNWeeU%3A17%3AAYjSIsXBUd2BRgrMiS2-kAKj_6lF0xycgCyamm1g8Q",
    "62001265034%3AxwUxzBde3lDOTT%3A20%3AAYjZmDhOD46vRs1CPO9rgZFa8XiGaH7KOW1duKithg",
    "56959999287%3AN1jlF67HztCHPu%3A17%3AAYj0R06JPmp2nq8m53x34d8vYUoOY_FNNuXdzhvuTA",
    "56204743006%3AvdOnjiEyTDVHOs%3A24%3AAYgV6HHZAFESXeZkWa6DQBjXLxTNNbXA5Ss6BJltgA",
    "62244918577%3AxuU57bCfnGJ7uU%3A0%3AAYiTF9QTtscwACPUnEMneqvyznIn_yRfP5whrVA36w",
    "57991418362%3AD8kUbLAPbKjcqn%3A25%3AAYhDqSJ7_nreAdDoPNQvhza1qtTho9AI0OaA8IjJEA",
    "62244918577%3Ar1D6zFIAEErh9Z%3A0%3AAYj_4gwAf04vPBREO9wumgP9Riwajy2MqRqqR0O26Q",
    "57139805509%3A3JP6h6dGaaebHb%3A2%3AAYiEQ3PaEymKNx0xTbINT81Y24wGwk-y5D9JSldWCw",
    "57756971432%3An40xVOCVnMsljt%3A17%3AAYi6FXrY41MhDnbX-PjMw8v69qYBQHIAc6_lZlQgIA",
    "57756971432%3As4EdL0v3oTqDsO%3A17%3AAYgyPeGkK-qK4WzUbfHFsOrZbaSbmgxGE0BPULD6Sg",
    "56085393163%3AfrdhRAHHoPBo2a%3A20%3AAYj2aTviNM-Gh8QZ48Kic3WwufIueY_QOw-C4Uve5w",
    "62042853691%3An5q5ygmtPUiYR9%3A14%3AAYguO9shcfIA1XFVfxS08go7C6bPuxSsMmsh-8NkZg",
    "59090497779%3AK3mlvwXb3WqYLZ%3A14%3AAYgTRTytniPVD1lheN8HrHbqZ026Q3sIoA3dZSUbJw",
    "56257999210%3ADavNhNxCHAKF3O%3A5%3AAYh5Yb6qE8Mw7e8DTmGlKrTZ7CGU7XDHP4wtzoajNw",
    "55519343963%3AZ7Uy1zS4caPQKD%3A6%3AAYjt2k67VW-z471WrI6TTKckn75MMflykF2II_6qtw",
    "56408794683%3AoYmP4uvkUdo1s2%3A4%3AAYgBAhC_gd1qe6NTO74b6TkMvbiP8nkeDxe1c6sqGg",
    "57673072874%3A4yF9s3dnw1eGq7%3A25%3AAYj36ZsMWXCib77B2xlsu3bvcUFe2aAVnmNsrKVLCg",
    "57314706707%3A4bxwaCF6CKwpWi%3A17%3AAYiUWwNfbgmJmEs07wFG6ETLLNc7LmJLqJx87dyQbA"
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
