# -*- coding: utf-8 -*-
import os

from yaml import load

config_path = os.path.join(os.path.dirname(__file__), "configure.yaml")

with open(config_path, encoding='utf-8') as f:
    cont = f.read()

cf = load(cont)


def get_weibo_id():
    return cf.get('weiboID')


def get_keywords():
    return cf.get('keywords')
