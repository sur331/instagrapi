import time
import random
import telebot
from instagrapi import Client

# ======================================================
# 1. الإعدادات والبيانات
# ======================================================

# ضع التوكن الخاص ببوت تليجرام هنا
TELEGRAM_BOT_TOKEN = "YOUR_TELEGRAM_BOT_TOKEN_HERE"

# قائمة الحسابات (قم بتعديل اسم المستخدم وكلمة المرور لكل حساب)
INSTAGRAM_ACCOUNTS = [
    {"username": "oiitaop", "password": "suR_1212"},
    {"username": "omanialfi", "password": "suR_1212"},
    {"username": "foofyooe", "password": "suR_1212"},
]

# تهيئة البوت
bot = telebot.TeleBot(TELEGRAM_BOT_TOKEN)

# ======================================================
# 2. أداء الأوامر والرسائل
# ======================================================

@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    welcome_text = """أهلاً بك في بوت الإعجابات التلقائية!

قم بإرسال رابط منشور إنستغرام للبدء في تنفيذ الإعجابات من حساباتك المجهزة.

مثال للرابط:
https://www.instagram.com/p/CgZa8drK52K/?igsh=bmYxOGdreXV0MGN2""

    bot.reply_to(message, welcome_text)


@bot.message_handler(func=lambda message: True)
def process_likes(message):
    post_url = message.text.strip()

    # التحقق من صحة الرابط
    if "instagram.com" not in post_url:
        bot.reply_to(message, "خطأ: يرجى إرسال رابط منشور إنستغرام صحيح.")
        return

    # إرسال رسالة التعديل التراكمية
    status_msg = bot.reply_to(message, "⏳ جاري بدء عملية الإعجابات...")

    success_count = 0
    fail_count = 0
    total_accounts = len(INSTAGRAM_ACCOUNTS)

    for idx, acc in enumerate(INSTAGRAM_ACCOUNTS, 1):
        username = acc["username"]
        password = acc["password"]

        try:
            # تحديث الحالة في تليجرام
            bot.edit_message_text(
                f"🔄 [{idx}/{total_accounts}] جاري الإعجاب عبر الحساب: @{username}",
                chat_id=message.chat.id,
                message_id=status_msg.message_id
            )

            # تسجيل الدخول وتنفيذ الإعجاب
            cl = Client()
            cl.login(username, password)

            media_pk = cl.media_pk_from_url(post_url)
            cl.media_like(media_pk)

            success_count += 1

            # فاصل زمني عشوائي من 10 إلى 15 ثانية
            delay = random.randint(10, 15)
            time.sleep(delay)

        except Exception as e:
            fail_count += 1
            print(f"[Error] الحساب {username} فشل: {e}")

    # التقرير النهائي
    report = f"""اكتملت العملية!

إعجابات ناجحة: {success_count}
إعجابات فاشلة: {fail_count}
إجمالي الحسابات: {total_accounts}"""

    bot.send_message(message.chat.id, report)

# ======================================================
# 3. تشغيل البوت
# ======================================================
if __name__ == "__main__":
    print("🤖 البوت يعمل الآن ويستقبل الرسائل...")
    bot.infinity_polling()
