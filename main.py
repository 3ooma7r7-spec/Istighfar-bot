import requests
import time
from datetime import datetime, timedelta
import pytz
from flask import Flask
import threading

# ===== إعداداتك =====
access_token = "EAAPIpeHujnUBPESLRzyYZBou718HCJPVY4w07UFJB3wcknvZBhwRwRB9Ow0SBnGL4EZB0OpJFWAAAjVrAH5IOhrhvH0kmeZC0QUFvEyOrTIe42ZB9tR7e1Gen9rrSNDbKeT4FFC40OlwVz7A5o9LZBDyvyVZBjaFrKIOejXi2ZBGFcOPaHXooLSJZBZCCFb0PdWVbs"
instagram_account_id = "17841473843944761"

images = [
    "https://i.imgur.com/3oOzaqt.jpeg", "https://i.imgur.com/SKoRQ65.jpeg",
    "https://i.imgur.com/9n1dtRu.jpeg", "https://i.imgur.com/R5eWBHX.jpeg",
    "https://i.imgur.com/h3bzSiq.jpeg", "https://i.imgur.com/XLN5LpT.jpeg",
    "https://i.imgur.com/nIbqHed.jpeg", "https://i.imgur.com/55bCsAU.jpeg",
    "https://i.imgur.com/4rR0iUy.jpeg", "https://i.imgur.com/h8tfHSo.jpeg",
    "https://i.imgur.com/Emk1chK.jpeg", "https://i.imgur.com/isMXPI0.jpeg",
    "https://i.imgur.com/Au8ifGE.jpeg", "https://i.imgur.com/dC78HG4.jpeg",
    "https://i.imgur.com/yR45N81.jpeg", "https://i.imgur.com/7pkL3Y9.jpeg",
    "https://i.imgur.com/o5jeDaS.jpeg", "https://i.imgur.com/0O5NQmw.jpeg",
    "https://i.imgur.com/HI05ts4.jpeg", "https://i.imgur.com/O1xdH65.jpeg",
    "https://i.imgur.com/PA1TqkJ.jpeg"
]

egypt_tz = pytz.timezone("Africa/Cairo")
current_index = 0

# ===== Flask Web Server صغير =====
app = Flask(__name__)

@app.route('/')
def home():
    return "Instagram Bot is running ✅"

# تشغيل السيرفر في Thread منفصل
threading.Thread(target=lambda: app.run(host="0.0.0.0", port=3000)).start()

# ===== حلقة النشر اليومي =====
while True:
    now = datetime.now(egypt_tz)
    target_time = now.replace(hour=22, minute=0, second=0, microsecond=0)
    if now >= target_time:
        target_time += timedelta(days=1)

    wait_seconds = (target_time - now).total_seconds()
    print(f"⏳ الانتظار {int(wait_seconds)} ثانية حتى الساعة 10 مساءً...")
    time.sleep(wait_seconds)

    img_url = images[current_index]
    print(f"📤 جاري رفع الصورة {current_index + 1} كـ Post...")

    # ===== نشر الصورة كـ Post =====
    create_url = f"https://graph.facebook.com/v17.0/{instagram_account_id}/media"
    payload = {
        "image_url": img_url,
        "access_token": access_token
    }
    r = requests.post(create_url, data=payload)
    result = r.json()

    if "id" in result:
        creation_id = result["id"]
        publish_url = f"https://graph.facebook.com/v17.0/{instagram_account_id}/media_publish"
        r2 = requests.post(publish_url, data={
            "creation_id": creation_id,
            "access_token": access_token
        })
        print(f"✅ الصورة {current_index + 1} نزلت كـ Post بنجاح:", r2.json())
    else:
        print(f"❌ حصل خطأ مع الـ Post:", result)

    # ===== نشر الصورة كـ Story =====
    print(f"📲 جاري رفع الصورة {current_index + 1} كـ Story...")
    story_url = f"https://graph.facebook.com/v17.0/{instagram_account_id}/media"
    story_payload = {
        "image_url": img_url,
        "is_story": "true",
        "access_token": access_token
    }
    r3 = requests.post(story_url, data=story_payload)
    story_result = r3.json()
    if "id" in story_result:
        print(f"✅ الصورة {current_index + 1} نزلت كـ Story بنجاح:", story_result)
    else:
        print(f"❌ حصل خطأ مع الـ Story:", story_result)

    # التكرار للصور
    current_index = (current_index + 1) % len(images)
