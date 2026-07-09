import re
from datetime import datetime


from storage import (
    load_data,
    save_data
)



def parse_event(text):


    data = load_data()

    members = data["members"]


    target = None


    for name in members:

        if text.startswith(name):

            target = name

            break



    if not target:

        return "格式錯誤，請使用：\n姓名：事故"



    if "：" not in text:

        return "請加入冒號，例如：\n宗旂：休"



    content = text.split("：",1)[1]


    today = datetime.now().strftime("%Y-%m-%d")



    event = {

        "name":target,

        "content":content,

        "start":today,

        "end":today,

        "type":"temporary"

    }



    # 多日

    date_range = re.search(
        r"(\d{1,2}/\d{1,2})-(\d{1,2}/\d{1,2})",
        content
    )


    if date_range:


        event["type"]="range"


        event["start"]=date_range.group(1)

        event["end"]=date_range.group(2)



    else:


        # 單日

        single = re.search(
            r"(\d{1,2}/\d{1,2})",
            content
        )


        if single:

            event["type"]="single"

            event["start"]=single.group(1)

            event["end"]=single.group(1)



    data["events"].append(event)


    save_data(data)



    return (
        f"已登記：\n"
        f"{target}：{content}"
    )





def get_today_events():

    data = load_data()

    today=datetime.now()


    result=[]


    for e in data["events"]:


        if e["type"]=="temporary":

            continue



        result.append(
            f'{e["name"]}：{e["content"]}'
        )


    return result





def clear_event(name):

    data=load_data()


    data["events"]=[

        e for e in data["events"]

        if e["name"]!=name

    ]


    save_data(data)


    return f"{name}事故已清除"





def reset_events():

    data=load_data()

    data["events"]=[]

    save_data(data)


    return "全部事故已清空"
