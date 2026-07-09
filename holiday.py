import holidays
from datetime import date, timedelta


tw_holidays = holidays.Taiwan()


def is_workday(target_date):
    """
    判斷指定日期是否工作日
    """
    if target_date.weekday() >= 5:
        return False

    if target_date in tw_holidays:
        return False

    return True


def is_tomorrow_workday():
    """
    判斷明天是否上班
    """
    tomorrow = date.today() + timedelta(days=1)

    return is_workday(tomorrow)
