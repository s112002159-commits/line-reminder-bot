# =====================
# 台灣假日
# =====================
tw_holidays = holidays.Taiwan()

def is_tomorrow_workday():

    tomorrow = (
        taiwan_now().date()
        + datetime.timedelta(days=1)
    )

    # 六日
    if tomorrow.weekday() >= 5:

        return False

    # 國定假日
    if tomorrow in tw_holidays:

        return False

    return True
