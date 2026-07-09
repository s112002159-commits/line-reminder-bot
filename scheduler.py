from holiday import is_workday
import datetime

def run():
 tomorrow=datetime.date.today()+datetime.timedelta(days=1)
 return is_workday(tomorrow)
