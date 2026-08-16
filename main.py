import os
import random
import time
import requests
import telebot
from instagrapi import Client

# جلب البيانات تلقائياً من إعدادات البيئة (Render Environment Variables)
BOT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')
FILE_URL = os.getenv('ACCOUNTS_URL')

# التحقق من وجود المفاتيح في Render
if not BOT_TOKEN or not FILE_URL:
    raise ValueError("❌ خطأ: يرجى التأكد من إضافة TELEGRAM_BOT_TOKEN و ACCOUNTS_URL في إعدادات Render!")

bot = telebot.TeleBot(BOT_TOKEN)

@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    bot.reply_to(message, "مرحباً بك! 👋\nأرسل لي رابط منشور أنستقرام لبدء تنفيذ اللايكات.")

@bot.message_handler(func=lambda message: "instagram.com" in message.text)
def process_likes(message):
    media_url = message.text.strip()
    bot.reply_to(message, "⏳ جاري بدء العملية...")

    try:
        response = requests.get(FILE_URL)
        accounts = response.json()
    except Exception as e:
        bot.send_message(message.chat.id, f"❌ خطأ في قراءة رابط الحسابات: {e}")
        return

    success_count = 0
    fail_count = 0
    total = len(accounts)

    for index, acc in enumerate(accounts, 1):
        cl = Client()
        try:
            cl.login(acc['username'], acc['password'])
            media_id = cl.media_id(cl.media_pk_from_url(media_url))
            cl.media_like(media_id)
            
            success_count += 1
            print(f"[{index}/{total}] تم: {acc['username']}")
        except Exception as e:
            fail_count += 1
            print(f"[{index}/{total}] فشل: {acc['username']}")

        # فاصل زمني لتجنب الحظر
        time.sleep(random.randint(45, 90))
        
        # استراحة كل 5 حسابات
        if index % 5 == 0 and index != total:
            time.sleep(300)

    # تقرير النهاية
    report = f"✅ اكتملت العملية!\n\n👍 نجاح: {success_count}\n❌ فشل: {fail_count}\n📊 الإجمالي: {total}"
    bot.send_message(message.chat.id, report)

if __name__ == "__main__":
    print("🤖 البوت يعمل الآن...")
    bot.polling(non_stop=True)
