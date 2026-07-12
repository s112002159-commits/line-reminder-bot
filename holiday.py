import holidays
import datetime
import pytz

taiwan_tz = pytz.timezone(
    "Asia/Taipei"
)

tw_holidays = holidays.Taiwan()

def now():

    return datetime.datetime.now(
        taiwan_tz
    )

def today():

    return now().date()

def tomorrow():

    return (
        today()
        + datetime.timedelta(days=1)
    )

def is_workday(date_obj):

    if date_obj.weekday() >= 5:

        return False

    if date_obj in tw_holidays:

        return False

    return True

def is_tomorrow_workday():

    return is_workday(
        tomorrow()
    )
