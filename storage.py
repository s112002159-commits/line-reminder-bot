import json
import os

from config import (
    DATA_FILE,
    DEFAULT_MEMBERS
)

# =====================================
# 建立預設資料
# =====================================

def default_data():

    members = {}

    for name in DEFAULT_MEMBERS:

        members[name] = {

            "text": "",

            "start": "",

            "expire": "",

            "show_once": False

        }

    return {

        "users": [],

        "groups": [],

        "members": members

    }


# =====================================
# 讀取
# =====================================

def load_data():

    if not os.path.exists(DATA_FILE):

        data = default_data()

        save_data(data)

        return data

    with open(

        DATA_FILE,

        "r",

        encoding="utf-8"

    ) as f:

        data = json.load(f)

    for member in DEFAULT_MEMBERS:

        if member not in data["members"]:

            data["members"][member] = {

                "text": "",

                "start": "",

                "expire": "",

                "show_once": False

            }

    save_data(data)

    return data


# =====================================
# 儲存
# =====================================

def save_data(data):

    with open(

        DATA_FILE,

        "w",

        encoding="utf-8"

    ) as f:

        json.dump(

            data,

            f,

            ensure_ascii=False,

            indent=4

        )


# =====================================
# 新增好友
# =====================================

def add_user(user_id):

    data = load_data()

    if user_id not in data["users"]:

        data["users"].append(user_id)

        save_data(data)


# =====================================
# 新增群組
# =====================================

def add_group(group_id):

    data = load_data()

    if group_id not in data["groups"]:

        data["groups"].append(group_id)

        save_data(data)
