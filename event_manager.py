import re
import datetime

from storage import (
    load_data,
    save_data
)

from holiday import today


# =====================================
# 新增事件
# =====================================

def update_event(

    name,

    content

):

    data = load_data()

    year = today().year

    # ==========================
    # 多日
    # 6/1-6/20
    # ==========================

    m = re.search(

        r"(\d{1,2})/(\d{1,2})-(\d{1,2})/(\d{1,2})",

        content

    )

    if m:

        sm = int(m.group(1))

        sd = int(m.group(2))

        em = int(m.group(3))

        ed = int(m.group(4))

        data["members"][name] = {

            "text": content,

            "start": f"{year}/{sm:02d}/{sd:02d}",

            "expire": f"{year}/{em:02d}/{ed:02d}",

            "show_once": False

        }

        save_data(data)

        return

    # ==========================
    # 單日
    # 6/25休假
    # ==========================

    s = re.search(

        r"(\d{1,2})/(\d{1,2})",

        content

    )

    if s:

        month = int(s.group(1))

        day = int(s.group(2))

        data["members"][name] = {

            "text": content,

            "start": f"{year}/{month:02d}/{day:02d}",

            "expire": "",

            "show_once": True

        }

        save_data(data)

        return

    # ==========================
    # 沒日期
    # ==========================

    data["members"][name] = {

        "text": content,

        "start": today().strftime("%Y/%m/%d"),

        "expire": "",

        "show_once": True

    }

    save_data(data)


# =====================================
# 是否顯示
# =====================================

def should_show(info):

    if info["text"] == "":

        return False

    # -----------------------
    # 今天
    # -----------------------

    t = today()

    # -----------------------
    # 無日期
    # -----------------------

    if info["show_once"]:

        return True

    # -----------------------
    # 多日
    # -----------------------

    try:

        start = datetime.datetime.strptime(

            info["start"],

            "%Y/%m/%d"

        ).date()

        end = datetime.datetime.strptime(

            info["expire"],

            "%Y/%m/%d"

        ).date()

        if (

            start - datetime.timedelta(days=1)

        ) <= t <= (

            end - datetime.timedelta(days=1)

        ):

            return True

    except:

        pass

    return False


# =====================================
# 清除過期
# =====================================

def clear_expired():

    data = load_data()

    t = today()

    changed = False

    for member in data["members"]:

        info = data["members"][member]

        if info["text"] == "":

            continue

        # ---------------------
        # 多日
        # ---------------------

        if info["expire"] != "":

            end = datetime.datetime.strptime(

                info["expire"],

                "%Y/%m/%d"

            ).date()

            if t > end:

                data["members"][member] = {

                    "text": "",

                    "start": "",

                    "expire": "",

                    "show_once": False

                }

                changed = True

        # ---------------------
        # 單次
        # ---------------------

        else:

            start = datetime.datetime.strptime(

                info["start"],

                "%Y/%m/%d"

            ).date()

            if t > start:

                data["members"][member] = {

                    "text": "",

                    "start": "",

                    "expire": "",

                    "show_once": False

                }

                changed = True

    if changed:

        save_data(data)


# =====================================
# 建立每日回報
# =====================================

def build_report():

    clear_expired()

    data = load_data()

    msg = "明日是否在營及事故回報：\n"

    for name in data["members"]:

        text = ""

        if should_show(

            data["members"][name]

        ):

            text = data["members"][name]["text"]

        msg += f"\n{name}：{text}"

    return msg
