import datetime
try:
 from workalendar.asia import Taiwan
 cal=Taiwan()
except Exception: cal=None
def is_workday(d):
    return d.weekday()<5 and (not cal or cal.is_working_day(d))
