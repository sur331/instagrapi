import time
import random
import telebot
from instagrapi import Client

# ================= ====================================
# 1. إعدادات البوت والحسابات
# ======================================================

# ضع توكن بوت تليجرام الخاص بك هنا (تأخذه من BotFather)
TELEGRAM_BOT_TOKEN = "8968135906:AAHHOKLfvBXg7KQJD67UHGcvbtYkyO8h4Hc"

# قائمة حساباتك على إنستغرام (قم بإضافة حساباتك وكلمات المرور)
INSTAGRAM_ACCOUNTS = [
    {"username": "oiitaop", "password": "suR_1212"},
    {"username": "omanialfi", "password": "suR_1212"},
    {"username": "foofyooe", "password": "suR_1212"},
]

# تهيئة بوت تليجرام
bot = telebot.TeleBot(TELEGRAM_BOT_TOKEN)

# ================= ====================================
# 2. الأوامر ومعالجة الرسائل
# ======================================================

@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    welcome_text = (
        "👋 **أهلاً بك في بوت الإعجابات التلقائية!**\n\n"
        "قم بإرسال رابط منشور إنستغرام للبدء في تنفيذ الإعجابات من حساباتك المجهزة.\n\n"
        "📌 **مثال للرابط:**\n`https://www.instagram.com/p/Cg-92wtKhgD/?igsh=MWFhYjN4emVxb2s0MQ==`"
    )
    bot.reply_to(message, welcome_text, parse_mode="Markdown")

@bot.message_handler(func=lambda message: True)
def process_likes(message):
    post_url = message.text.strip()

    # التحقق من صحة الرابط
    if "instagram.com" not in post_url:
        bot.reply_to(message, "❌ **خطأ:** يرجى إرسال رابط منشور إنستغرام صحيح.")
        return

    # إرسال رسالة جاري العمل
    status_msg = bot.reply_to(message, "⏳ **جاري بدء عملية الإعجابات...**")

    success_count = 0
    fail_count = 0
    total_accounts = len(INSTAGRAM_ACCOUNTS)

    for idx, acc in enumerate(INSTAGRAM_ACCOUNTS, 1):
        username = acc["username"]
        password = acc["password"]

        try:
            # تحديث الحالة للمستخدم في تليجرام
            bot.edit_message_text(
                f"🔄 [{idx}/{total_accounts}] جاري تسجيل الدخول بالحساب: `@{username}`...",
                chat_id=message.chat.id,
                message_id=status_msg.message_id,
                parse_mode="Markdown"
            )

            # الاتصال بإنستغرام
            cl = Client()
            cl.login(username, password)

            # تحويل الرابط إلى المعرّف الخاص بالمنشور (Media ID)
            media_pk = cl.media_pk_from_url(post_url)

            # تنفيذ الإعجاب
            cl.media_like(media_pk)
            success_count += 1

            # الفاصل الزمني العشوائي بين 10 إلى 15 ثانية
            delay = random.randint(10, 15)
            time.sleep(delay)

        except Exception as e:
            fail_count += 1
            print(f"[Error] الحساب {username} فشل بسبب: {e}")

    # إرسال التقرير النهائي
    final_report = (
        f"✅ **اكتملت العملية!**\n\n"
        f"🟢 إعجابات ناجحة: **{success_count}**\n"
        f"🔴 إعجابات فاشلة: **{fail_count}**\n"
        f"📊 إجمالي الحسابات: **{total_accounts}**"
    )
    bot.send_message(message.chat.id, final_report, parse_mode="Markdown")

# ================= ====================================
# 3. تشغيل البوت
# ======================================================
if __name__ == "__main__":
    print("🤖 البوت يعمل الآن ويستقبل الأوامر...")
    bot.infinity_polling()
