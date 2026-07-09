import json
import os


DATA_FILE = "data.json"



def load_data():

    if not os.path.exists(DATA_FILE):

        return {
            "members": [],
            "events": [],
            "users": [],
            "groups": []
        }


    with open(
        DATA_FILE,
        "r",
        encoding="utf-8"
    ) as f:

        return json.load(f)



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



def get_members():

    return load_data()["members"]



def save_user(user_id):

    data = load_data()

    if user_id not in data["users"]:

        data["users"].append(user_id)

        save_data(data)



def save_group(group_id):

    data = load_data()

    if group_id not in data["groups"]:

        data["groups"].append(group_id)

        save_data(data)
