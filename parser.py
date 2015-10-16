import json
from celery import Celery

def counter(word, dic):
    keys = dic.keys()
    for key in keys:
        if word == key:
            dic[key] +=1

def parser(tweets, dic):
    with open(tweets, 'r') as f:
        rows = f.readlines()
        for row in rows:
            if not row == '\n':
                json_object = json.loads(row)
                if 'retweeted_status' not in json_object:
                    words = json_object['text'].split()
                    for word in words:
                        counter(word.lower(), dic)
    print dic
    return dic
