import json
import os

from config import (
    DATA_FILE,
    DEFAULT_MEMBERS
)

def create_default_data():

    members = {}

    for name in DEFAULT_MEMBERS:

        members[name] = {

            "text": "",

            "start": "",

            "expire": "",

            "show_once": False,

            "type": ""

        }

    return {

        "users": [],

        "groups": [],

        "members": members

    }

def load_data():

    if not os.path.exists(DATA_FILE):

        data = create_default_data()

        save_data(data)

        return data

    with open(
        DATA_FILE,
        "r",
        encoding="utf-8"
    ) as f:

        data = json.load(f)

    if "members" not in data:

        data["members"] = {}

    for name in DEFAULT_MEMBERS:

        if name not in data["members"]:

            data["members"][name] = {

                "text": "",

                "start": "",

                "expire": "",

                "show_once": False,

                "type": ""

            }

    return data

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
            indent=2
        )

def add_user(user_id):

    data = load_data()

    if user_id not in data["users"]:

        data["users"].append(user_id)

        save_data(data)

def add_group(group_id):

    data = load_data()

    if group_id not in data["groups"]:

        data["groups"].append(group_id)

        save_data(data)
