from flask import Flask, request, abort
from linebot import LineBotApi, WebhookHandler
from linebot.models import (
    MessageEvent,
    TextMessage,
    TextSendMessage
)
from linebot.exceptions import InvalidSignatureError

import os
import datetime
import holidays
import json
import re
import pytz

# 修正：name 必須改為 __name__
app = Flask(__name__) 

# =====================
# 台灣時間
# =====================
taiwan_tz = pytz.timezone(
    "Asia/Taipei"
)

def taiwan_now():
    return datetime.datetime.now(
        taiwan_tz
    )

# =====================
# LINE 設定
# =====================
line_bot_api = LineBotApi(
    os.getenv("LINE_CHANNEL_ACCESS_TOKEN")
)

handler = WebhookHandler(
    os.getenv("LINE_CHANNEL_SECRET")
)

# =====================
# 資料檔
# =====================
FILE = "data.json"

# =====================
# 固定名單
# =====================
DEFAULT_MEMBERS = [
    "造賓", "佳真", "宗旂", "培昇", 
    "季家", "佳峻", "彥呈", "欣雯"
]

# =====================
# 讀取資料
# =====================
def load_data():
    members = {}
    for name in DEFAULT_MEMBERS:
        members[name] = {    
            "text": "",    
            "start": "",    
            "expire": "",    
            "show_once": False    
        }

    if not os.path.exists(FILE):
        return {    
            "users": [],    
            "groups": [],    
            "members": members    
        }

    with open(FILE, "r", encoding="utf-8") as f:
        data = json.load(f)

    if "members" not in data:
        data["members"] = members

    for name in DEFAULT_MEMBERS:
        if name not in data["members"]:    
            data["members"][name] = {    
                "text": "",    
                "start": "",    
                "expire": "",    
                "show_once": False    
            }

    save_data(data)
    return data

# =====================
# 儲存資料
# =====================
def save_data(data):
    with open(FILE, "w", encoding="utf-8") as f:
        json.dump(    
            data,    
            f,    
            ensure_ascii=False,    
            indent=2    
        )

# =====================
# 記錄好友
# =====================
def add_user(user_id):
    data = load_data()
    if user_id not in data["users"]:
        data["users"].append(user_id)
        save_data(data)

# =====================
# 記錄群組
# =====================
def add_group(group_id):
    data = load_data()
    if group_id not in data["groups"]:
        data["groups"].append(group_id)
        save_data(data)

# =====================
# 台灣假日判斷
# =====================
tw_holidays = holidays.Taiwan()

def is_tomorrow_workday():
    tomorrow = (
        taiwan_now().date()
        + datetime.timedelta(days=1)
    )

    # 星期六日
    if tomorrow.weekday() >= 5:
        return False

    # 台灣國定假日
    if tomorrow in tw_holidays:
        return False

    return True

# =====================
# 判斷是否顯示
# =====================
def should_show(info):
    today = taiwan_now().date()
    tomorrow = (
        today
        + datetime.timedelta(days=1)
    )

    text = info.get("text", "")
    start = info.get("start", "")
    expire = info.get("expire", "")
    show_once = info.get("show_once", False)

    if text == "":
        return False

    # =====================
    # 單日事件
    # 範例：
    # 小明：6/1休假
    # 5/31 回報明日才顯示
    # =====================
    if show_once:
        return False

    # =====================
    # 多日事件
    # 範例：
    # 5/28出差至6/2
    # 5/27開始顯示
    # 6/1停止顯示
    # =====================
    try:
        start_date = datetime.datetime.strptime(    
            start,    
            "%Y/%m/%d"    
        ).date()    

        expire_date = datetime.datetime.strptime(    
            expire,    
            "%Y/%m/%d"    
        ).date()    

        show_start = (    
            start_date    
            - datetime.timedelta(days=1)    
        )    

        show_end = (    
            expire_date    
            - datetime.timedelta(days=2)    
        )    

        if show_start <= today <= show_end:    
            return True    

        return False

    except:
        return False

# =====================
# 清理過期資料
# =====================
def clear_expired():
    data = load_data()
    today = taiwan_now().date()

    for name, info in data["members"].items():
        expire = info.get("expire", "")    
        start = info.get("start", "")    
        show_once = info.get("show_once", False)    

        # =====================    
        # 單日事件    
        # =====================    
        if show_once:    
            try:    
                target_date = datetime.datetime.strptime(    
                    start,    
                    "%Y/%m/%d"    
                ).date()    

                if today > target_date:    
                    data["members"][name] = {    
                        "text": "",    
                        "start": "",    
                        "expire": "",    
                        "show_once": False    
                    }    
            except:    
                pass    

        # =====================    
        # 多日事件    
        # =====================    
        elif expire:    
            try:    
                expire_date = datetime.datetime.strptime(    
                    expire,    
                    "%Y/%m/%d"    
                ).date()    

                if today >= expire_date:    
                    # 注意：你提供的程式碼在這裡被截斷了，請補齊後續邏輯。
                    data["members"][name] = {
                        "text": "",    
                        "start": "",    
                        "expire": "",    
                        "show_once": False
                    }
            except:
                pass
    
    save_data(data)
    
# =====================
# 首頁測試路由 (供瀏覽器點擊檢查)
# =====================
@app.route("/", methods=['GET'])
def index():
    return "Line Bot is running smoothly!", 200

# =====================
# LINE Webhook 接收點
# =====================
@app.route("/callback", methods=['POST'])
def callback():
    # 取得 LINE 傳來的 X-Line-Signature header
    signature = request.headers.get('X-Line-Signature')

    # 取得請求內容
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    # 處理 Webhook 簽名驗證
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        app.logger.error("Invalid signature. Please check your channel access token/channel secret.")
        abort(400)

    return 'OK'

