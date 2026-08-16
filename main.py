import os
import random
import time
import requests
import telebot
from instagrapi import Client

# 1. جلب البيانات السرية من البيئة (Render Environment Variables)
BOT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')
FILE_URL = os.getenv('ACCOUNTS_URL')

# التأكد من وجود البيانات السرية
if not BOT_TOKEN or not FILE_URL:
    raise ValueError("❌ خطأ: لم يتم العثور على TELEGRAM_BOT_TOKEN أو ACCOUNTS_URL في إعدادات البيئة!")

bot = telebot.TeleBot(BOT_TOKEN)

@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    bot.reply_to(
        message, 
        "مرحباً بك! 👋\nأرسل لي رابط منشور أنستقرام لبدء تنفيذ اللايكات من الحسابات الـ 35."
    )

@bot.message_handler(func=lambda message: "instagram.com" in message.text)
def process_likes(message):
    media_url = message.text.strip()
    bot.reply_to(message, "⏳ جاري جلب الحسابات وبدء تنفيذ اللايكات...")

    # 2. قراءة ملف الحسابات من الرابط المخفي
    try:
        response = requests.get(FILE_URL)
        accounts = response.json()
    except Exception as e:
        bot.send_message(message.chat.id, f"❌ خطأ في قراءة ملف الحسابات: {e}")
        return

    success_count = 0
    fail_count = 0
    total_accounts = len(accounts)

    # 3. المرور على الحسابات وتنفيذ العمليات
    for index, acc in enumerate(accounts, 1):
        cl = Client()
        try:
            # تسجيل الدخول المباشر
            cl.login(acc['username'], acc['password'])
            
            # جلب معرف المنشور وعمل لايك
            media_id = cl.media_id(cl.media_pk_from_url(media_url))
            cl.media_like(media_id)
            
            success_count += 1
            print(f"[{index}/{total_accounts}] تم بنجاح: {acc['username']}")
            
        except Exception as e:
            fail_count += 1
            print(f"[{index}/{total_accounts}] فشل الحساب {acc['username']}: {e}")

        # فاصل زمني عشوائي لحماية الحسابات (من 45 إلى 90 ثانية)
        time.sleep(random.randint(45, 90))
        
        # استراحة كل 5 حسابات لتفادي الحظر
        if index % 5 == 0 and index != total_accounts:
            print("استراحة لمدة 5 دقائق لحماية الحسابات...")
            time.sleep(300)

    # 4. إرسال التقرير النهائي على تليجرام
    report = (
        f"✅ **اكتملت العملية!**\n\n"
        f"👍 نجاح: {success_count}\n"
        f"❌ فشل: {fail_count}\n"
        f"📊 الإجمالي: {total_accounts}"
    )
    bot.send_message(message.chat.id, report)

# تشغيل البوت باستمرار
if __name__ == "__main__":
    print("🤖 البوت يعمل الان بانتظار الأوامر...")
    bot.polling(non_stop=True)
