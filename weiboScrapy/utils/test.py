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
# r = redis.StrictRedis(host='127.0.0.1', port=6379, db=0)
# print(r.scan())
# print(bool(r.scan()[0]))
print('https://m.weibo.cn/api/container/getIndex?containerid=100103type%3D61%26q%3D%E7%84%A6%E8%99%91+%E6%8A%91%E9%83%81%26t%3D0')