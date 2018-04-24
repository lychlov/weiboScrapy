# -*- coding: utf-8 -*-
import os

from yaml import load

config_path = os.path.join(os.path.dirname(__file__), "configure.yaml")

with open(config_path, encoding='utf-8') as f:
    # with open(config_path) as f:
    cont = f.read()

cf = load(cont)


def get_target_ids():
    return cf.get('targetID')


def get_weibo_id_for_tweets():
    return cf.get('weiboIDForTweets')


def get_weibo_id_for_comments():
    return cf.get('weiboIDForComments')


def get_keywords():
    return cf.get('keywords')


def get_redis():
    return cf.get('redis')


def get_mongodb():
    return cf.get('mongodb')


def get_max_page_for_tweets():
    return cf.get('maxPageForTweets')


def get_before_date():
    return cf.get('beforeDate')


def get_max_page_for_comments():
    return cf.get('maxPageForComments')
