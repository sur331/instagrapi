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
    return "Bot is running Diagnostic Mode!"

def run_flask():
    port = int(os.environ.get("PORT", 8080))
    app.run(host='0.0.0.0', port=port)

threading.Thread(target=run_flask, daemon=True).start()

# ======================================================
# 2. إعدادات التوكن والجلسات
# ======================================================
TELEGRAM_BOT_TOKEN = "8968135906:AAHHOKLfvBXg7KQJD67UHGcvbtYkyO8h4Hc"

RAW_SESSIONS = [
    "57482313741%3AioArFfp3FeYzoP%3A14%3AAYgraTZ2GkjUsLMgq2_g0OgZcnHF7yRTWTveQd8D-w",
    "62341132903%3AlVOGBkVNyqiywE%3A17%3AAYgprFF6ZHPagb38PI5Y0ts_OseBeXt_Nsm42arbXg",
    "62213803419%3AwZUWNmpOGRPFkN%3A21%3AAYiUuLhNerUpi1hyqR4w6F_iOQQXhagUcOyrAeU3JA",
    "64103212632%3AtdO6UD2mHGOeai%3A11%3AAYhMLrTgqEPIRinZxWLehKB2DI6yJeWr-yl565pBkg",
    "62415293906%3AIwiEtdhab4ASPv%3A7%3AAYgBaV9-FktYJ0M_XKsNopRdA0fgULPsvo-kO2VT6A",
    "56204743006%3A0ikYbM37u22xyP%3A19%3AAYhoh5iRPhD5A1nSPi51JkTqyLmwI6Tja2r5qT8DAQ",
    "57437960504%3AZc5qZ3SJ0UABUt%3A3%3AAYgBK0ODg7wDA5Ge62SaLJK4i_4t83bzTLVPxXVz2g",
    "62244918577%3AHYe02rci0JIi0r%3A0%3AAYjJPFhe-6yJx_5PziVspKXl5C56knmOz9rKHcBQ0Q",
    "64191058006%3AMyLuu4ofXslNKb%3A12%3AAYjwXONPw3G1yDK4jz8l2DdV_7lW2xj1hFRilL9Tzw",
    "55736844695%3AUfokpqwDkr02dU%3A22%3AAYirtHN4lT1WOGH0O9vNcjSUwifVviILiNtCI8hezQ",
    "55401748889%3AGTOsviiH4K4y0c%3A2%3AAYinaT7N8NshcRiV1sPA4K-BnicG2FxBF9jwhi2TKw",
    "64053657843%3AkiP1JfMzLcxmB0%3A28%3AAYgM_yiFrF5UripDXgQ-vbQrp2Gi8UhE-tmkwZmWUg",
    "62063778773%3AGDHZr3XfudRV6q%3A20%3AAYjgzW4mT_5VpjxY3LsTDeMnoPto-3qwIQy3gSGKzw",
    "65542576846%3AYNqV7DiUG9BrdO%3A3%3AAYg9oqAW3n0sVtmirDNbHU76Y-unurPwbOMfrx_cBg",
    "56959999287%3A8Kh8bOmHxdBOp7%3A17%3AAYhpkBItDLxP9ty0N6URppXxH66gtnSHI3keV3DLaw",
    "62264580737%3AzV2JtVWjYtUq70%3A19%3AAYhokyNYMDzh2lSkEs2xi0rDawGdgMOke33XsvevjQ",
    "55395580346%3AaSmoHcSlQL3ZrW%3A7%3AAYjPiYLHlVWkKsJrR6h2NIv-TMRGkWd2RUqhpi8SOA",
    "56779868751%3AFrf7YAjuDqZINs%3A4%3AAYheCbV0zlHz5RQtxhdA2VQfGb5GWu4kMv0aa9cejg",
    "59173074423%3Ayg8e3gnoqFXCKt%3A11%3AAYi-IoqRvGVt02B56LOxC5k0rphtWkxgUoTk1Tzg3g",
    "57170083165%3AuwhIMfVm1UjzpV%3A6%3AAYjq9KkgQxFRZZZInMthv2LWC2EB-1WQQlCjmyYBWA",
    "52445894947%3A7yQljXl3o9RLBl%3A28%3AAYhPsyspvtuzuCJBAmWNG0qRMsPhDzN97jZAv3sXSA",
    "56085393163%3AfrdhRAHHoPBo2a%3A20%3AAYj2aTviNM-Gh8QZ48Kic3WwufIueY_QOw-C4Uve5w",
    "62042853691%3An5q5ygmtPUiYR9%3A14%3AAYguO9shcfIA1XFVfxS08go7C6bPuxSsMmsh-8NkZg",
    "59090497779%3AK3mlvwXb3WqYLZ%3A14%3AAYgTRTytniPVD1lheN8HrHbqZ026Q3sIoA3dZSUbJw",
    "56257999210%3ADavNhNxCHAKF3O%3A5%3AAYh5Yb6qE8Mw7e8DTmGlKrTZ7CGU7XDHP4wtzoajNw",
    "55519343963%3AZ7Uy1zS4caPQKD%3A6%3AAYjt2k67VW-z471WrI6TTKckn75MMflykF2II_6qtw",
    "56408794683%3AoYmP4uvkUdo1s2%3A4%3AAYgBAhC_gd1qe6NTO74b6TkMvbiP8nkeDxe1c6sqGg",
    "57673072874%3A4yF9s3dnw1eGq7%3A25%3AAYj36ZsMWXCib77B2xlsu3bvcUFe2aAVnmNsrKVLCg"
]

bot = telebot.TeleBot(TELEGRAM_BOT_TOKEN)

# ======================================================
# 3. معالجة الإعجابات مع كشف الأخطاء Detailed Errors
# ======================================================
@bot.message_handler(commands=['start'])
def start_cmd(message):
    bot.reply_to(message, f"أهلاً بك! جاهز لخدمتك عبر {len(RAW_SESSIONS)} حساباً.\nأرسل رابط منشور إنستغرام لبدء الإعجابات.")

@bot.message_handler(func=lambda message: True)
def process_likes(message):
    post_url = message.text.strip()

    if "instagram.com" not in post_url:
        bot.reply_to(message, "⚠️ يرجى إرسال رابط منشور إنستغرام صحيح فقط.")
        return

    status_msg = bot.reply_to(message, "⏳ جاري تنفيذ الإعجابات وتشخيص الجلسات...")

    success_count = 0
    fail_count = 0
    total = len(RAW_SESSIONS)
    failed_logs = []

    for idx, raw_session in enumerate(RAW_SESSIONS, 1):
        clean_session = urllib.parse.unquote(raw_session).strip()

        try:
            bot.edit_message_text(
                f"🔄 [{idx}/{total}] جاري التجربة على الحساب رقم #{idx}...",
                chat_id=message.chat.id,
                message_id=status_msg.message_id
            )

            cl = Client()
            # تقليل البصمة الرقمية للحد من الكشف
            cl.set_user_agent("Instagram 269.0.0.18.75 Android (26/8.0.0; 480dpi; 1080x1920; Xiaomi; Redmi Note 5; whyred; qcom; en_US; 314665258)")
            cl.login_by_sessionid(clean_session)
            
            media_pk = cl.media_pk_from_url(post_url)
            cl.media_like(media_pk)

            success_count += 1
            time.sleep(random.randint(5, 10))

        except Exception as e:
            fail_count += 1
            err_msg = str(e).splitlines()[0] if str(e) else "Unknown Error"
            failed_logs.append(f"حساب #{idx}: {err_msg[:30]}")
            time.sleep(2)

    # التقرير النهائي
    report = f"✅ **نتيجة المحاولة:**\n\n"
    report += f"❤️ ناجح: {success_count}\n"
    report += f"❌ فاشل: {fail_count}\n"
    report += f"👥 الإجمالي: {total}\n\n"

    if failed_logs:
        report += "⚠️ **عينة من أسباب الفشل:**\n"
        for log in failed_logs[:5]:  # عرض أول 5 أخطاء فقط لمعرفة السبب
            report += f"• {log}\n"

    bot.send_message(message.chat.id, report, parse_mode="Markdown")

# ======================================================
# 4. تشغيل البوت
# ======================================================
if __name__ == "__main__":
    bot.infinity_polling()
