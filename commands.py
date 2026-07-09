from storage import load,save
from config import VERSION

def command(t):
 d=load()
 if t=='/help': return '/list /members /status /reset /clear /version'
 if t=='/members': return str(list(d['members'].keys()))
 if t=='/list': return str(d['events'])
 if t=='/status': return 'OK'
 if t=='/reset' or t=='/clear': d['events']={};save(d);return '清除完成'
 if t=='/version': return VERSION
 return None
