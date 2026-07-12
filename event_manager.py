import datetime
import re

from holiday import today
from storage import (
    load_data,
    save_data
)

def parse_event(name, content):

    data = load_data()

    year = today().year

    # 多日
    multi = re.search(
        r"(\d{1,2})/(\d{1,2})-(\d{1,2})/(\d{1,2})",
        content
    )

    if multi:

        sm = int(multi.group(1))
        sd = int(multi.group(2))

        em = int(multi.group(3))
        ed = int(multi.group(4))

        data["members"][name] = {

            "text": content,

            "start": f"{year}/{sm:02d}/{sd:02d}",

            "expire": f"{year}/{em:02d}/{ed:02d}",

            "show_once": False,

            "type": "multi"

        }

        save_data(data)

        return

    # 單日
    single = re.search(
        r"(\d{1,2})/(\d{1,2})",
        content
    )

    if single:

        month = int(single.group(1))
        day = int(single.group(2))

        data["members"][name] = {

            "text": content,

            "start": f"{year}/{month:02d}/{day:02d}",

            "expire": "",

            "show_once": True,

            "type": "single"

        }

        save_data(data)

        return

    # 臨時
    data["members"][name] = {

        "text": content,

        "start": today().strftime(
            "%Y/%m/%d"
        ),

        "expire": "",

        "show_once": True,

        "type": "temp"

    }

    save_data(data)

def clear_expired():

    data = load_data()

    current = today()

    for name, info in data["members"].items():

        event_type = info.get(
            "type",
            ""
        )

        if event_type == "temp":

            continue

        if event_type == "single":

            target = datetime.datetime.strptime(
                info["start"],
                "%Y/%m/%d"
            ).date()

            if current > target:

                data["members"][name] = {

                    "text": "",

                    "start": "",

                    "expire": "",

                    "show_once": False,

                    "type": ""

                }

        if event_type == "multi":

            expire = datetime.datetime.strptime(
                info["expire"],
                "%Y/%m/%d"
            ).date()

            if current > expire:

                data["members"][name] = {

                    "text": "",

                    "start": "",

                    "expire": "",

                    "show_once": False,

                    "type": ""

                }

    save_data(data)
