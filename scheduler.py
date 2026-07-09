from linebot.v3.messaging import (
    Configuration,
    ApiClient,
    MessagingApi,
    PushMessageRequest,
    TextMessage
)

from config import (
    LINE_CHANNEL_ACCESS_TOKEN
)

from holiday import (
    tomorrow_is_workday
)

from storage import (
    load_data,
    save_data
)

from event_manager import (
    build_report
)

configuration = Configuration(
    access_token=LINE_CHANNEL_ACCESS_TOKEN
)


# =====================================
# 發送每日回報
# =====================================

def send_daily_report():

    if not tomorrow_is_workday():

        print("⛔ 明日非工作日")

        return False

    data = load_data()

    message = build_report()

    with ApiClient(configuration) as api_client:

        api = MessagingApi(api_client)

        # =========================
        # 發送好友
        # =========================

        for user in data["users"]:

            try:

                api.push_message(

                    PushMessageRequest(

                        to=user,

                        messages=[
                            TextMessage(
                                text=message
                            )
                        ]

                    )

                )

                print(f"User OK {user}")

            except Exception as e:

                print(e)

        # =========================
        # 發送群組
        # =========================

        for group in data["groups"]:

            try:

                api.push_message(

                    PushMessageRequest(

                        to=group,

                        messages=[
                            TextMessage(
                                text=message
                            )
                        ]

                    )

                )

                print(f"Group OK {group}")

            except Exception as e:

                print(e)

    clear_show_once()

    print("✅ 每日回報完成")

    return True


# =====================================
# 發送後清除單次事件
# =====================================

def clear_show_once():

    data = load_data()

    changed = False

    for member in data["members"]:

        info = data["members"][member]

        if info["show_once"]:

            data["members"][member] = {

                "text": "",

                "start": "",

                "expire": "",

                "show_once": False

            }

            changed = True

    if changed:

        save_data(data)
