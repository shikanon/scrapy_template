#coding:utf8
import json
import codecs
data_list = []
n= 0
with codecs.open("renwu_data_utf8.json","r",encoding="utf8") as f:
    for line in f:
        n = n+1
        #data_list.append(json.loads(line))

data = json.loads(line)
