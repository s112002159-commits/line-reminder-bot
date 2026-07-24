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
    "造賓",
    "佳真",
    "宗旂",
    "培昇",
    "季家",
    "佳峻",
    "彥呈",
    "欣雯"
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
        try:  
            target_date = datetime.datetime.strptime(  
                start,  
                "%Y/%m/%d"  
            ).date()  

            if tomorrow == target_date:  
                return True  

            return False  

        except:  
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
# 發送每日回報
# =====================
def send_job(force_send=False):
    if not force_send and not is_tomorrow_workday():  
        print("⛔ 明日是假日，不發送")  
        return "Skip: Tomorrow is holiday"

    clear_expired()  

    data = load_data()  
    users = data.get("users", [])
    groups = data.get("groups", [])

    msg = "明日是否在營及事故回報：\n"  

    for name, info in data["members"].items():  
        text = ""  

        if should_show(info):  
            text = info.get("text", "")  

        msg += f"\n{name}：{text}"  

    # 發送好友  
    for user in users:  
        try:  
            line_bot_api.push_message(  
                user,  
                TextSendMessage(text=msg)  
            )  
        except Exception as e:  
            print("User Error:", e)  

    # 發送群組  
    for group in groups:  
        try:  
            line_bot_api.push_message(  
                group,  
                TextSendMessage(text=msg)  
            )  
        except Exception as e:  
            print("Group Error:", e)  

    print("✅ 發送完成")

# =====================
# 首頁
# =====================
@app.route("/")
def home():
return "OK", 200

# =====================
# cron-job 觸發
# =====================
@app.route("/trigger")
def trigger():
    try:  
        force = request.args.get('force', 'false').lower() == 'true'
        result = send_job(force_send=force)  
        return f"success: {result}", 200  

    except Exception as e:  
        return str(e), 500


# =====================
# LINE callback
# =====================
@app.route("/callback", methods=['POST'])
def callback():
    signature = request.headers.get(  
        'X-Line-Signature'  
    )  

    body = request.get_data(  
        as_text=True  
    )  

    try:  
        handler.handle(  
            body,  
            signature  
        )  

    except InvalidSignatureError:  
        abort(400)  

    return 'OK'

# =====================
# 接收訊息
# =====================
@handler.add(
    MessageEvent,
    message=TextMessage
)
def handle_message(event):
    text = event.message.text.strip()  

    # 自動記錄發送者/群組 ID
    if event.source.type == "user":  
        add_user(event.source.user_id)  
    elif event.source.type == "group":  
        add_group(event.source.group_id)  

    data = load_data()  

    # =====================
    # 指令處理區塊
    # =====================
    if text.startswith("/"):
        # 1. /h 使用說明
        if text.lower() == "/h":
            reply_text = (
                "📖 使用說明指令表：\n\n"
                "• /h - 查看說明清單\n"
                "• /l - 查看所有成員事故\n"
                "• /s - 查看系統目前儲存事件\n"
                "• /c [姓名] - 清除指定人員事故 (例: /c 宗旂)\n"
                "• /r - 清空所有成員事故\n\n"
                "💡 回報格式範例：\n"
                "• 單日：宗旂：6/1休假\n"
                "• 多日：佳真：5/28出差至6/2"
            )
            line_bot_api.reply_message(event.reply_token, TextSendMessage(text=reply_text))
            return

        # 2. /l 查看所有事故
        elif text.lower() == "/l":
            clear_expired()
            data = load_data()
            msg_lines = ["📋 目前事故列表：\n"]
            for name, info in data["members"].items():
                status = info.get("text", "無")
                if not status:
                    status = "無"
                msg_lines.append(f"• {name}：{status}")
            
            line_bot_api.reply_message(event.reply_token, TextSendMessage(text="\n".join(msg_lines)))
            return

        # 3. /s 查看目前儲存事件 (Json格式詳情)
        elif text.lower() == "/s":
            clear_expired()
            data = load_data()
            has_event = False
            msg_lines = ["🔍 目前系統儲存之有效事件：\n"]
            for name, info in data["members"].items():
                if info.get("text"):
                    has_event = True
                    start = info.get("start", "-")
                    expire = info.get("expire", "-")
                    msg_lines.append(f"• {name}：{info['text']} (起:{start} 迄:{expire})")
            
            if not has_event:
                msg_lines.append("目前沒有儲存任何事件。")
                
            line_bot_api.reply_message(event.reply_token, TextSendMessage(text="\n".join(msg_lines)))
            return

        # 4. /c 某人 (清除指定人員)
        elif text.lower().startswith("/c"):
            target_name = text[2:].strip()
            if not target_name:
                line_bot_api.reply_message(event.reply_token, TextSendMessage(text="⚠️ 請指定要清除的人員，例：/c 宗旂"))
                return

            if target_name in data["members"]:
                data["members"][target_name] = {
                    "text": "",
                    "start": "",
                    "expire": "",
                    "show_once": False
                }
                save_data(data)
                line_bot_api.reply_message(event.reply_token, TextSendMessage(text=f"✅ 已清除 {target_name} 的事故紀錄"))
            else:
                line_bot_api.reply_message(event.reply_token, TextSendMessage(text=f"❌ 找不到成員：{target_name}"))
            return

        # 5. /r 清空所有事故
        elif text.lower() == "/r":
            for name in data["members"]:
                data["members"][name] = {
                    "text": "",
                    "start": "",
                    "expire": "",
                    "show_once": False
                }
            save_data(data)
            line_bot_api.reply_message(event.reply_token, TextSendMessage(text="✅ 已清空所有人事故資料"))
            return

    # =====================  
    # 一般更新事件格式處理：  
    # 宗旂：6/1休假  
    # 佳真：5/28出差至6/2  
    # =====================  
    match = re.match(  
        r"(.+?)：(.+)",  
        text  
    )  

    if match:  
        name = match.group(1).strip()  
        content = match.group(2).strip()  

        if name not in data["members"]:  
            return

# =====================
# 接收訊息
# =====================
@handler.add(
    MessageEvent,
    message=TextMessage
)
def handle_message(event):
    text = event.message.text.strip()  

    # 自動記錄發送者/群組 ID
    if event.source.type == "user":  
        add_user(event.source.user_id)  
    elif event.source.type == "group":  
        add_group(event.source.group_id)  

    data = load_data()  

    # =====================
    # 斜線指令處理區塊
    # =====================
    if text.startswith("/"):
        # 1. /h 使用說明
        if text.lower() == "/h":
            reply_text = (
                "📖 使用說明指令表：\n\n"
                "• /h - 查看說明清單\n"
                "• /l - 查看所有成員事故\n"
                "• /s - 查看目前儲存事件\n"
                "• /c [姓名] - 清除指定人員事故 (例: /c 宗旂)\n"
                "• /r - 清空所有成員事故\n\n"
                "💡 回報格式範例：\n"
                "• 單日：宗旂：6/1休假\n"
                "• 多日：佳真：5/28出差至6/2"
            )
            line_bot_api.reply_message(event.reply_token, TextSendMessage(text=reply_text))
            return

        # 2. /l 查看所有事故
        elif text.lower() == "/l":
            clear_expired()
            data = load_data()
            msg_lines = ["📋 目前事故列表：\n"]
            for name, info in data["members"].items():
                status = info.get("text", "無")
                if not status:
                    status = "無"
                msg_lines.append(f"• {name}：{status}")
            
            line_bot_api.reply_message(event.reply_token, TextSendMessage(text="\n".join(msg_lines)))
            return

        # 3. /s 查看目前儲存事件詳情
        elif text.lower() == "/s":
            clear_expired()
            data = load_data()
            has_event = False
            msg_lines = ["🔍 目前系統儲存之有效事件：\n"]
            for name, info in data["members"].items():
                if info.get("text"):
                    has_event = True
                    start = info.get("start", "-")
                    expire = info.get("expire", "-")
                    msg_lines.append(f"• {name}：{info['text']} (起:{start} 迄:{expire})")
            
            if not has_event:
                msg_lines.append("目前沒有儲存任何事件。")
                
            line_bot_api.reply_message(event.reply_token, TextSendMessage(text="\n".join(msg_lines)))
            return

        # 4. /c 某人 (清除指定人員)
        elif text.lower().startswith("/c"):
            target_name = text[2:].strip()
            if not target_name:
                line_bot_api.reply_message(event.reply_token, TextSendMessage(text="⚠️ 請指定要清除的人員，例：/c 宗旂"))
                return

            if target_name in data["members"]:
                data["members"][target_name] = {
                    "text": "",
                    "start": "",
                    "expire": "",
                    "show_once": False
                }
                save_data(data)
                line_bot_api.reply_message(event.reply_token, TextSendMessage(text=f"✅ 已清除 {target_name} 的事故紀錄"))
            else:
                line_bot_api.reply_message(event.reply_token, TextSendMessage(text=f"❌ 找不到成員：{target_name}"))
            return

        # 5. /r 清空所有事故
        elif text.lower() == "/r":
            for name in data["members"]:
                data["members"][name] = {
                    "text": "",
                    "start": "",
                    "expire": "",
                    "show_once": False
                }
            save_data(data)
            line_bot_api.reply_message(event.reply_token, TextSendMessage(text="✅ 已清空所有人事故資料"))
            return

    # =====================  
    # 一般更新事件格式處理：  
    # 宗旂：6/1休假  
    # 佳真：5/28出差至6/2  
    # =====================  
    match = re.match(  
        r"(.+?)：(.+)",  
        text  
    )  

    if match:  
        name = match.group(1).strip()  
        content = match.group(2).strip()  

        if name not in data["members"]:  
            return  

        today = taiwan_now().date()
        year = today.year  

        # 多日事件  
        multi_match = re.search(  
            r"(\d{1,2})/(\d{1,2}).*至(\d{1,2})/(\d{1,2})",  
            content  
        )  

        if multi_match:  
            start_month = int(multi_match.group(1))  
            start_day = int(multi_match.group(2))  
            end_month = int(multi_match.group(3))  
            end_day = int(multi_match.group(4))  

            start_year = year + 1 if start_month < today.month else year
            end_year = start_year + 1 if end_month < start_month else start_year

            data["members"][name] = {  
                "text": content,  
                "start": f"{start_year}/{start_month:02d}/{start_day:02d}",  
                "expire": f"{end_year}/{end_month:02d}/{end_day:02d}",  
                "show_once": False  
            }  

        else:  
            # 單日事件  
            single_match = re.search(  
                r"(\d{1,2})/(\d{1,2})",  
                content  
            )  

            if single_match:  
                month = int(single_match.group(1))  
                day = int(single_match.group(2))  

                target_year = year + 1 if month < today.month else year

                data["members"][name] = {  
                    "text": content,  
                    "start": f"{target_year}/{month:02d}/{day:02d}",  
                    "expire": "",  
                    "show_once": True  
                }  

        save_data(data)  

        line_bot_api.reply_message(  
            event.reply_token,  
            TextSendMessage(  
                text=f"✅ 已更新 {name}"  
            )  
        )

# =====================
# 啟動
# =====================
# 修正 2：__name__ 判斷修正
if __name__ == "__main__":
    app.run(  
        host="0.0.0.0",  
        port=5000  
    )
