# -*- coding: utf-8 -*-
import json

f = open('/home/docker/work_space/weiboScrapy/json.txt', 'r')
string = f.read()
data_json = json.loads(string)
if data_json['ok'] == 0:
    print("没了")
