import os
import time
import random
from flask import Flask
from threading import Thread
from instagrapi import Client

app = Flask(__name__)

@app.route('/')
def home():
    return "Instagram Auto-Liker is running active!"

def run_web():
    port = int(os.environ.get("PORT", 8080))
    app.run(host='0.0.0.0', port=port)

ACCOUNTS = [
    {"username": "realestate_surr", "password": "suR_1212"},
    {"username": "surcityonan", "password": "suR_1212"},
]

# تنظيف الرابط من المعلمات الزائدة لضمان استخراج media_pk بنجاح
TARGET_POST_URL = "https://www.instagram.com/reel/Daz0BYcICsP/?igsh=bnJ5c3lodTAzejVp"

def perform_likes():
    time.sleep(10)
    print("⏳ بدأ تنفيذ عملية الإعجابات...")

    for acc in ACCOUNTS:
        username = acc["username"]
        password = acc["password"]

        cl = Client()
        # إضافة مهلة زمنية إضافية للطلبات لتجنب قطع الاتصال
        cl.request_timeout = 10 
        
        session_file = f"session_{username}.json"

        try:
            print(f"🔑 جاري تسجيل الدخول للحساب: {username}")

            if os.path.exists(session_file):
                cl.load_settings(session_file)
                cl.login(username, password)
            else:
                cl.login(username, password)
                cl.dump_settings(session_file)

            # جلب معرف المنشور
            media_pk = cl.media_pk_from_url(TARGET_POST_URL)
            print(f"🆔 معرف المنشور (Media PK): {media_pk}")

            # تنفيذ الإعجاب
            cl.media_like(media_pk)
            print(f"✅ تم وضع إعجاب بنجاح بواسطة: {username}")

        except Exception as e:
            print(f"❌ حدث خطأ أثناء معالجة الحساب {username}: {e}")

        time.sleep(random.randint(5, 15))

if __name__ == "__main__":
    t = Thread(target=run_web)
    t.start()
    perform_likes()
