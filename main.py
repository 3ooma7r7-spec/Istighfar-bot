import requests
import time
from datetime import datetime
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

# ===== حلقة النشر كل 15 ثانية (للتجريب) =====
while True:
    wait_seconds = 15
    print(f"⏳ الانتظار {wait_seconds} ثانية...")
    time.sleep(wait_seconds)

    img_url = images[current_index]
    print(f"📤 جاري رفع الصورة {current_index + 1}...")
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
        print(f"✅ الصورة {current_index + 1} اترفعت بنجاح:", r2.json())
    else:
        print(f"❌ حصل خطأ مع الصورة {current_index + 1}:", result)

    current_index = (current_index + 1) % len(images)
