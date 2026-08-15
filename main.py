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
    return "Bot is active with 28 accounts!"

def run_flask():
    port = int(os.environ.get("PORT", 8080))
    app.run(host='0.0.0.0', port=port)

threading.Thread(target=run_flask, daemon=True).start()

# ======================================================
# 2. إعدادات التوكن والجلسات (Sessions) لـ 28 حساباً
# ======================================================
TELEGRAM_BOT_TOKEN = "8968135906:AAHHOKLfvBXg7KQJD67UHGcvbtYkyO8h4Hc"

INSTAGRAM_SESSIONS = [
    {"id": "1", "sessionid": "57482313741%3AioArFfp3FeYzoP%3A14%3AAYgraTZ2GkjUsLMgq2_g0OgZcnHF7yRTWTveQd8D-w"},
    {"id": "2", "sessionid": "62341132903%3AlVOGBkVNyqiywE%3A17%3AAYgprFF6ZHPagb38PI5Y0ts_OseBeXt_Nsm42arbXg"},
    {"id": "3", "sessionid": "62213803419%3AwZUWNmpOGRPFkN%3A21%3AAYiUuLhNerUpi1hyqR4w6F_iOQQXhagUcOyrAeU3JA"},
    {"id": "4", "sessionid": "64103212632%3AtdO6UD2mHGOeai%3A11%3AAYhMLrTgqEPIRinZxWLehKB2DI6yJeWr-yl565pBkg"},
    {"id": "5", "sessionid": "62415293906%3AIwiEtdhab4ASPv%3A7%3AAYgBaV9-FktYJ0M_XKsNopRdA0fgULPsvo-kO2VT6A"},
    {"id": "6", "sessionid": "56204743006%3A0ikYbM37u22xyP%3A19%3AAYhoh5iRPhD5A1nSPi51JkTqyLmwI6Tja2r5qT8DAQ"},
    {"id": "7", "sessionid": "57437960504%3AZc5qZ3SJ0UABUt%3A3%3AAYgBK0ODg7wDA5Ge62SaLJK4i_4t83bzTLVPxXVz2g"},
    {"id": "8", "sessionid": "62244918577%3AHYe02rci0JIi0r%3A0%3AAYjJPFhe-6yJx_5PziVspKXl5C56knmOz9rKHcBQ0Q"},
    {"id": "9", "sessionid": "64191058006%3AMyLuu4ofXslNKb%3A12%3AAYjwXONPw3G1yDK4jz8l2DdV_7lW2xj1hFRilL9Tzw"},
    {"id": "10", "sessionid": "55736844695%3AUfokpqwDkr02dU%3A22%3AAYirtHN4lT1WOGH0O9vNcjSUwifVviILiNtCI8hezQ"},
    {"id": "11", "sessionid": "55401748889%3AGTOsviiH4K4y0c%3A2%3AAYinaT7N8NshcRiV1sPA4K-BnicG2FxBF9jwhi2TKw"},
    {"id": "12", "sessionid": "64053657843%3AkiP1JfMzLcxmB0%3A28%3AAYgM_yiFrF5UripDXgQ-vbQrp2Gi8UhE-tmkwZmWUg"},
    {"id": "13", "sessionid": "62063778773%3AGDHZr3XfudRV6q%3A20%3AAYjgzW4mT_5VpjxY3LsTDeMnoPto-3qwIQy3gSGKzw"},
    {"id": "14", "sessionid": "65542576846%3AYNqV7DiUG9BrdO%3A3%3AAYg9oqAW3n0sVtmirDNbHU76Y-unurPwbOMfrx_cBg"},
    {"id": "15", "sessionid": "56959999287%3A8Kh8bOmHxdBOp7%3A17%3AAYhpkBItDLxP9ty0N6URppXxH66gtnSHI3keV3DLaw"},
    {"id": "16", "sessionid": "62264580737%3AzV2JtVWjYtUq70%3A19%3AAYhokyNYMDzh2lSkEs2xi0rDawGdgMOke33XsvevjQ"},
    {"id": "17", "sessionid": "55395580346%3AaSmoHcSlQL3ZrW%3A7%3AAYjPiYLHlVWkKsJrR6h2NIv-TMRGkWd2RUqhpi8SOA"},
    {"id": "18", "sessionid": "56779868751%3AFrf7YAjuDqZINs%3A4%3AAYheCbV0zlHz5RQtxhdA2VQfGb5GWu4kMv0aa9cejg"},
    {"id": "19", "sessionid": "59173074423%3Ayg8e3gnoqFXCKt%3A11%3AAYi-IoqRvGVt02B56LOxC5k0rphtWkxgUoTk1Tzg3g"},
    {"id": "20", "sessionid": "57170083165%3AuwhIMfVm1UjzpV%3A6%3AAYjq9KkgQxFRZZZInMthv2LWC2EB-1WQQlCjmyYBWA"},
    {"id": "21", "sessionid": "52445894947%3A7yQljXl3o9RLBl%3A28%3AAYhPsyspvtuzuCJBAmWNG0qRMsPhDzN97jZAv3sXSA"},
    {"id": "22", "sessionid": "56085393163%3AfrdhRAHHoPBo2a%3A20%3AAYj2aTviNM-Gh8QZ48Kic3WwufIueY_QOw-C4Uve5w"},
    {"id": "23", "sessionid": "62042853691%3An5q5ygmtPUiYR9%3A14%3AAYguO9shcfIA1XFVfxS08go7C6bPuxSsMmsh-8NkZg"},
    {"id": "24", "sessionid": "59090497779%3AK3mlvwXb3WqYLZ%3A14%3AAYgTRTytniPVD1lheN8HrHbqZ026Q3sIoA3dZSUbJw"},
    {"id": "25", "sessionid": "56257999210%3ADavNhNxCHAKF3O%3A5%3AAYh5Yb6qE8Mw7e8DTmGlKrTZ7CGU7XDHP4wtzoajNw"},
    {"id": "26", "sessionid": "55519343963%3AZ7Uy1zS4caPQKD%3A6%3AAYjt2k67VW-z471WrI6TTKckn75MMflykF2II_6qtw"},
    {"id": "27", "sessionid": "56408794683%3AoYmP4uvkUdo1s2%3A4%3AAYgBAhC_gd1qe6NTO74b6TkMvbiP8nkeDxe1c6sqGg"},
    {"id": "28", "sessionid": "57673072874%3A4yF9s3dnw1eGq7%3A25%3AAYj36ZsMWXCib77B2xlsu3bvcUFe2aAVnmNsrKVLCg"}
]

bot = telebot.TeleBot(TELEGRAM_BOT_TOKEN)

# ======================================================
# 3. استقبال روابط تليجرام وتنفيذ الإعجابات
# ======================================================
@bot.message_handler(commands=['start'])
def start_cmd(message):
    bot.reply_to(message, f"أهلاً بك! البوت جاهز لخدمتك بواسطة {len(INSTAGRAM_SESSIONS)} حساباً.\nأرسل لي رابط منشور إنستغرام لعمل الإعجابات تلقائياً.")

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
            cl.login_by_sessionid(session_id)
            
            media_pk = cl.media_pk_from_url(post_url)
            cl.media_like(media_pk)

            success_count += 1
            # فاصل زمني عشوائي لحماية الحسابات من الحظر (بين 3 و 7 ثوانٍ)
            time.sleep(random.randint(3, 7))

        except Exception as e:
            fail_count += 1
            print(f"[Error] الحساب #{acc_id} فشل: {e}")

    report = f"""✅ **اكتملت العملية بنجاح!**

❤️ إعجابات ناجحة: {success_count}
❌ إعجابات فاشلة: {fail_count}
👥 إجمالي الحسابات: {total}"""

    bot.send_message(message.chat.id, report, parse_mode="Markdown")

# ======================================================
# 4. تشغيل البوت
# ======================================================
if __name__ == "__main__":
    bot.infinity_polling()
