# -*- coding: utf-8 -*-
import redis

from weiboScrapy.utils.time_transfor import time_trans

# print(time_trans('刚刚'))
# print(time_trans('2分钟前'))
# print(time_trans('13小时前'))
# print(time_trans('昨天 09:03'))
# print(time_trans('04-12'))
# print(time_trans('2017-09-12'))

# a = 11
# b = 1
# print(a == 11 and b == 1)
r = redis.StrictRedis(host='127.0.0.1', port=6379, db=0)
print(r.scan())
print(bool(r.scan()[0]))
