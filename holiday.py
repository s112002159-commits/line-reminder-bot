import holidays
from datetime import datetime, timedelta


tw_holidays = holidays.Taiwan()



def is_workday(date=None):

    if date is None:
        date = datetime.now()


    # 六日
    if date.weekday() >= 5:
        return False


    # 國定假日
    if date.date() in tw_holidays:
        return False


    return True



def is_tomorrow_workday():

    tomorrow = datetime.now() + timedelta(days=1)

    return is_workday(tomorrow)
