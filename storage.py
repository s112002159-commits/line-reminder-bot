import json,os
FILE='data.json'
def load():
    if not os.path.exists(FILE): return {'members':{},'groups':{},'events':{}}
    with open(FILE,'r',encoding='utf8') as f:return json.load(f)
def save(d):
    with open(FILE,'w',encoding='utf8') as f: json.dump(d,f,ensure_ascii=False,indent=2)
