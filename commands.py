from storage import load_data, save_data
from event_manager import build_report
from config import DEFAULT_MEMBERS, ADMIN_USERS

VERSION = "2.0.0"


def is_admin(user_id):

    return user_id in ADMIN_USERS


# =========================
# /help
# =========================
def help_message():

    return """📖 LINE 回報機器人使用說明

【事故輸入】

無日期
宗旂：休
佳峻：公差

今天14:55發送一次後自動清除

--------------------

單日

宗旂：6/29休假

僅於6/28回報一次

--------------------

多日

宗旂：6/29-7/3出國

6/28開始回報

一直回報到7/2

7/3自動恢復空白

--------------------

查詢

/help
/h

查看說明

/list

查看目前所有事故

/status

查看目前儲存資料

/members

查看固定名單

/version

查看版本

#測試
/測試

預覽今天14:55將發送內容
"""


# =========================
# /members
# =========================
def members():

    msg = "固定人員：\n"

    for member in DEFAULT_MEMBERS:

        msg += f"\n• {member}"

    return msg


# =========================
# /version
# =========================
def version():

    return f"LINE Reminder Bot\nVersion {VERSION}"


# =========================
# /list
# =========================
def list_events():

    data = load_data()

    msg = "目前事故：\n"

    for name, info in data["members"].items():

        if info["text"]:

            msg += f"\n{name}：{info['text']}"

    return msg


# =========================
# /status
# =========================
def status():

    data = load_data()

    return f"""目前狀態

好友數：

{len(data['users'])}

群組數：

{len(data['groups'])}

人員：

{len(data['members'])}
"""


# =========================
# /clear
# =========================
def clear(user_id):

    if not is_admin(user_id):

        return "❌ 沒有權限"

    data = load_data()

    for member in data["members"]:

        data["members"][member] = {

            "text": "",

            "start": "",

            "expire": "",

            "show_once": False

        }

    save_data(data)

    return "✅ 已清除全部事故"


# =========================
# /reset
# =========================
def reset(user_id):

    if not is_admin(user_id):

        return "❌ 沒有權限"

    data = {

        "users": [],

        "groups": [],

        "members": {}

    }

    for member in DEFAULT_MEMBERS:

        data["members"][member] = {

            "text": "",

            "start": "",

            "expire": "",

            "show_once": False

        }

    save_data(data)

    return "✅ 系統已重置"


# =========================
# 預覽
# =========================
def preview():

    return build_report()
