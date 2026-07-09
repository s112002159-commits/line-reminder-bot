from event_manager import (
    parse_event,
    clear_event,
    reset_events
)

from storage import load_data



HELP_TEXT = """

LINE事故回報系統

指令：

/help /h
使用說明

#測試 /測試
預覽今天15:00發送內容

/list
查看所有事故

/status
查看目前儲存事件

/members
查看固定名單

/clear 姓名
清除指定事故

/reset
清空所有事故

"""



def process_command(text):


    text=text.strip()



    if text in [
        "/help",
        "/h"
    ]:

        return HELP_TEXT



    if text.lower() in [
    "#test",
    "/test"
        
    ]:

    from scheduler import generate_report

    return generate_report()


    if text=="/members":

        data=load_data()

        return (
            "固定名單：\n"
            +
            "\n".join(data["members"])
        )



    if text=="/status":

        data=load_data()

        return str(data["events"])



    if text=="/list":

        data=load_data()

        if not data["events"]:

            return "目前無事故"


        return "\n".join(

            [
                f'{e["name"]}：{e["content"]}'
                for e in data["events"]
            ]

        )



    if text.startswith("/clear"):


        name=text.replace(
            "/clear",
            ""
        ).strip()


        if not name:

            return "請輸入姓名"


        return clear_event(name)



    if text=="/reset":

        return reset_events()



    if text=="/version":

        return "LINE Reminder Bot v2.0"



    #事故格式

    if "：" in text:

        return parse_event(text)



    return (
        "未知指令\n"
        "輸入 /help 查看"
    )
