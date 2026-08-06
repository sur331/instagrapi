import os
import time
import random
import requests
from flask import Flask
from threading import Thread

app = Flask(__name__)

@app.route('/')
def home():
    return "Instagram Auto-Liker (Cookies Mode) is active!"

def run_web():
    port = int(os.environ.get("PORT", 8080))
    app.run(host='0.0.0.0', port=port)

# ---------------------------------------------------------
# قائمة الحسابات الثلاثة بالكوكيز المدمجة
# ---------------------------------------------------------
ACCOUNTS_COOKIES = [
    {
        "name": "Account 1 (57673072874)",
        "cookie": "datr=ys9zak7a6-ztpY5_2oTGrJ_1;ds_user_id=57673072874;csrftoken=Tt3TGLSxb1hzY-t-QQK_Jq;ig_did=5382263C-CE97-4BAC-A8B1-F108F2572852;wd=384x639;mid=anPPygABAAHsQJlGfUoOqWUiO95x;sessionid=57673072874%3APYs5gteOsNc432%3A14%3AAYjNpybTxUWqRO4C2cHXcQqc5gQ1AX8D2cj563kQwA;dpr=2.8125;rur=CLN%2C17841457626229134%2C1787184729%3A01ff51c42fa78efead41b838bf50abc689290affced24afeb36a197442014a52206f1fb"
    },
    {
        "name": "Account 2 (62001265034)",
        "cookie": "ps_n=1;datr=7cpzavPKNKCQ-GWDpEB6Sfsc;ds_user_id=62001265034;csrftoken=WopANixMRBF1JVdg3v54EmI6bQbhtTK9;ig_did=8DA59788-5420-44DB-9ECE-D45DC20D836A;ps_l=1;wd=384x639;mid=anPK7QABAAFvFW-Xl7Z0qAN9tOIC;sessionid=62001265034%3AUg1GXh5TcGaD7P%3A18%3AAYhlE1zO8PN6ZIaT8Iac3AxnKcRcNNFpuii3LeU__g;dpr=2.8125;rur=LDC%2C17841461951030158%2C1787183451%3A01ff0434b8fc4884aaaf478a7bd16fd144413aad2aaa54680e31d134022c8239ac9334ca"
    },
    {
        "name": "Account 3 (63782954883)",
        "cookie": "ps_n=1;datr=7cpzavPKNKCQ-GWDpEB6Sfsc;ds_user_id=63782954883;csrftoken=5Jp5exwTMSlpqzq1F2xq2zGKdfFut283;ig_did=8DA59788-5420-44DB-9ECE-D45DC20D836A;ps_l=1;wd=384x639;mid=anPK7QABAAFvFW-Xl7Z0qAN9tOIC;sessionid=63782954883%3ATgNnIH0Djvo5Jq%3A24%3AAYjU6uZqFvonpBlN-V5aYW4uk7tJoDq5JEUFGPHDqQ;dpr=2.8125;rur=LDC%2C17841463686512869%2C1787185592%3A01ff24f24b676c9f1b4307b55646ce9ef93d6470d14a3d4e59c128c0038adcbae782237f"
    }
]

# رابط المنشور أو الريلز المستهدف
TARGET_POST_URL = "https://www.instagram.com/reel/Cogh86CqESU/?igsh=MTZlZzZncnJ4MnY0bg=="

def extract_csrf_token(cookie_str):
    """استخراج رمز csrftoken من نص الكوكي تلقائياً"""
    for item in cookie_str.split(";"):
        if "csrftoken=" in item:
            return item.split("=")[1].strip()
    return ""

def get_media_id_from_url(url):
    """جلب ID المنشور عبر API الرسمية من الرابط"""
    try:
        req = requests.get(f"https://api.instagram.com/oembed/?url={url}")
        if req.status_code == 200:
            return req.json().get("media_id")
    except Exception as e:
        print(f"❌ خطأ في الحصول على ID المنشور: {e}")
    return None

def perform_likes():
    time.sleep(5)
    print("⏳ جاري بدء العملية...")

    media_id = get_media_id_from_url(TARGET_POST_URL)
    if not media_id:
        print("❌ لم يتم العثور على ID المنشور! تأكد من صحة الرابط.")
        return

    print(f"🆔 معرف المنشور (Media ID): {media_id}\n")

    for acc in ACCOUNTS_COOKIES:
        account_name = acc["name"]
        cookie_data = acc["cookie"]

        csrf_token = extract_csrf_token(cookie_data)
        like_url = f"https://www.instagram.com/web/likes/{media_id}/like/"

        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            "X-CSRFToken": csrf_token,
            "Content-Type": "application/x-www-form-urlencoded",
            "Cookie": cookie_data,
            "Origin": "https://www.instagram.com",
            "Referer": TARGET_POST_URL
        }

        try:
            print(f"🔑 إرسال الإعجاب من [{account_name}]...")
            response = requests.post(like_url, headers=headers)

            if response.status_code == 200 and response.json().get("status") == "ok":
                print(f"✅ تم وضع الإعجاب بنجاح بواسطة [{account_name}]")
            else:
                print(f"❌ فشل وضع الإعجاب بواسطة [{account_name}] - الاستجابة: {response.text}")

        except Exception as e:
            print(f"❌ خطأ أثاء معالجة [{account_name}]: {e}")

        # وقت انتظار عشوائي بين 15 إلى 30 ثانية لتجنب الحظر
        wait_time = random.randint(15, 30)
        print(f"⏸️ انتظار لمدة {wait_time} ثانية قبل الانتقال للحساب التالي...\n")
        time.sleep(wait_time)

if __name__ == "__main__":
    t = Thread(target=run_web)
    t.start()
    perform_likes()
