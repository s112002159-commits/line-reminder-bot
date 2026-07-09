from storage import load_data
from event_manager import parse_event, clear_event, reset_events
from scheduler import generate_report



HELP_TEXT = """
LINE事故回報系統

指令：

/help /h
使用說明

/test #test
預覽15:00回報內容

/list
查看所有事故

/status
查看目前儲存事件

/members
查看固定名單

/clear 人名
清除指定事故

/reset
清空所有事故

/version
查看版本
"""



def is_member_event(text):

    if "：" not in text:
        return False


    name = text.split("：")[0]


    data = load_data()


    return name in data["members"]





def process_command(text):


    text = text.strip()



    # HELP

    if text in [
        "/help",
        "/h"
    ]:

        return HELP_TEXT





    # 測試發送

    if text.lower() in [
        "/test",
        "#test"
    ]:

        return generate_report()





    # 查看固定名單

    if text == "/members":

        data = load_data()


        return (
            "固定名單：\n"
            +
            "\n".join(
                data["members"]
            )
        )





    # 查看事件

    if text == "/list":


        data = load_data()


        if not data["events"]:

            return "目前沒有事故"



        result="目前事故：\n"



        for event in data["events"]:

            result += (
                f'{event["name"]}：'
                f'{event["content"]}\n'
            )


        return result





    # 系統狀態

    if text == "/status":

        data=load_data()


        return str(data)





    # 清除指定人員

    if text.startswith("/clear"):


        name=text.replace(
            "/clear",
            ""
        ).strip()


        if not name:

            return "格式：/clear 人名"


        return clear_event(name)





    # 清空全部

    if text == "/reset":

        return reset_events()





    # 版本

    if text == "/version":

        return "LINE Reminder Bot v2.1"





    # 只有固定名單+冒號才判斷事故

    if is_member_event(text):


        return parse_event(text)





    return (
        "無法辨識指令\n"
        "請輸入 /help"
    )
