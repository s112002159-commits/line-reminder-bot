import datetime
import holidays

from config import TIMEZONE

tw_holidays = holidays.Taiwan()


def now():

    return datetime.datetime.now(TIMEZONE)


def today():

    return now().date()


def tomorrow():

    return today() + datetime.timedelta(days=1)


def is_workday(date):

    if date.weekday() >= 5:
        return False

    if date in tw_holidays:
        return False

    return True


def tomorrow_is_workday():

    return is_workday(
        tomorrow()
    )
