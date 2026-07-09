from datetime import datetime


from storage import (
    load_data,
    save_data
)


from holiday import (
    is_tomorrow_workday
)



from datetime import datetime

from storage import load_data



def generate_report():


    data=load_data()


    today=datetime.now()


    message="明日是否在營及事故回報：\n\n"


    for member in data["members"]:


        result=""


        for event in data["events"]:


            if event["name"]==member:


                result=event["content"]



        message += (
            f"{member}：{result}\n"
        )


    return message





def daily_report():


    if not is_tomorrow_workday():

        return "明日非工作日，不發送"



    message=generate_report()



    # 清除臨時事故

    data=load_data()


    data["events"]=[

        e for e in data["events"]

        if e["type"]!="temporary"

    ]


    save_data(data)


    return message
