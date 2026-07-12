from storage import load_data, save_data
from config import DEFAULT_MEMBERS, VERSION, BUILD
from holiday import today
import datetime

# ==========================
# HELP
# ==========================

HELP_TEXT = """
LINE 回報 Bot 使用說明

====================

【臨時事故】

宗旂：休

→ 今日14:55發送一次
→ 發送後自動清除

====================

【單日事故】

宗旂：7/1休假

→ 6/30回報一次

====================

【多日事故】

宗旂：7/1-7/3休假

→ 6/30開始
→ 7/2最後一次
→ 7/3自動清除

====================

管理指令

/help
/h

/list

/status

/members

/version

/clear 姓名

/reset

#測試

/測試
"""

# ==========================
# HELP
# ==========================

def help_text():
    return HELP_TEXT

# ==========================
# MEMBERS
# ==========================

def member_text():

    text = "固定名單\n"

    for name in DEFAULT_MEMBERS:

        text += f"\n{name}"

    return text

# ==========================
# VERSION
# ==========================

def version_text():

    return f"""

LINE Reminder Bot

{VERSION}

Build

{BUILD}
"""

# ==========================
# STATUS
# ==========================

def status_text():

    data = load_data()

    msg = "目前資料庫狀態\n"

    for name, info in data["members"].items():

        msg += f"""

{name}

type : {info['type']}

text : {info['text']}

start : {info['start']}

expire : {info['expire']}
"""

    return msg

# ==========================
# LIST
# ==========================

def list_text():

    data = load_data()

    msg = "目前事故\n"

    for name, info in data["members"].items():

        text = info["text"]

        if text == "":

            text = "無"

        msg += f"\n{name}：{text}"

    return msg

# ==========================
# RESET
# ==========================

def reset_all():

    data = load_data()

    for name in data["members"]:

        data["members"][name] = {

            "text": "",

            "start": "",

            "expire": "",

            "show_once": False,

            "type": ""

        }

    save_data(data)

    return "✅ 已全部清除"

# ==========================
# CLEAR
# ==========================

def clear_member(name):

    data = load_data()

    if name not in data["members"]:

        return "找不到此人"

    data["members"][name] = {

        "text": "",

        "start": "",

        "expire": "",

        "show_once": False,

        "type": ""

    }

    save_data(data)

    return f"✅ 已清除 {name}"

# ==========================
# 預覽明日回報
# ==========================

def preview():

    from scheduler import build_message

    return build_message()
