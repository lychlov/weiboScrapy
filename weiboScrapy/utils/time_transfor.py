# -*- coding: utf-8 -*-
import time

import re


def time_trans(interval):
    """
    刚刚、x分钟前、x小时前、昨天 09:03、MM-dd、yyyy-MM-dd
    :param interval: 
    :return: yyyy-MM-dd hh:mm
    """
    if not interval.find('刚刚') < 0:
        return time.strftime("%Y-%m-%d %H:%M", time.localtime())
    if not interval.find('分钟前') < 0:
        min_num = int(interval.replace('分钟前', ''))
        return time.strftime("%Y-%m-%d %H:%M", time.localtime(time.time() - min_num * 60))
    if not interval.find('小时前') < 0:
        hour_mun = int(interval.replace('小时前', ''))
        return time.strftime("%Y-%m-%d %H:%M", time.localtime(time.time() - hour_mun * 60 * 60))
    if not interval.find('昨天 ') < 0:
        hour_min = interval.replace('昨天 ', '')
        return time.strftime("%Y-%m-%d ", time.localtime(time.time() - 24 * 60 * 60)) + hour_min
    temp = interval
    temp.split('-')
    if len(temp.split('-')) == 2:
        return time.strftime("%Y-", time.localtime()) + interval + " 00:00"
    if len(temp.split('-')) == 3:
        return interval + " 00:00"
    return
