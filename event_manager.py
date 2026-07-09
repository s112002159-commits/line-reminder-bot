from storage import load,save
import datetime

def add_event(user,text,start=None,end=None):
 d=load(); d['events'][user]={'text':text,'start':start or str(datetime.date.today()),'end':end or start}; save(d)
def clear():
 d=load();d['events']={};save(d)
