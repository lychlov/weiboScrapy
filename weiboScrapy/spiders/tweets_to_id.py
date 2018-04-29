# -*- coding: utf-8 -*-
import json

import datetime

import logging
import scrapy

from weiboScrapy.config import get_target_ids, get_keywords
from weiboScrapy.config.conf import get_max_page_for_tweets, get_before_date
from weiboScrapy.items import TweetItem
from weiboScrapy.utils.ItemParse import tweet_parse, user_parse
from weiboScrapy.utils.time_transfor import time_trans

logger = logging.getLogger(__name__)


class TweetsInIDSpider(scrapy.Spider):
    name = 'tweets_to_id'
    allowed_domains = ['weibo.cn']
    start_urls = ['http://weibo.cn/']
    keywords = get_keywords()
    target_ids = get_target_ids()
    max_page = get_max_page_for_tweets()
    before_date_enable = get_before_date()['enable']
    before_date = datetime.datetime.strptime(get_before_date()['date'], "%Y-%m-%d %H:%M")

    def __init__(self, run_args, *args, **kwargs):
        super(TweetsInIDSpider, self).__init__(*args, **kwargs)
        self.keywords = run_args.get('keywords', [])
        self.before_date_enable = run_args.get('beforeDate').get('enable', 'False') == str(True)
        self.max_page = run_args.get('maxPageForTweets', 100)
        self.before_date = datetime.datetime.strptime(run_args.get('beforeDate').get('date', '2000-01-01 00:00'),
                                                      "%Y-%m-%d %H:%M")
        self.target_ids = run_args.get('targetID', [])

    def start_requests(self):
        if len(self.target_ids) == 0:
            return
        for id_dict in self.target_ids:
            # print(id_dict)
            target_id = id_dict['userid']
            target_url = 'https://m.weibo.cn/api/container/getIndex?uid=' + target_id + '&luicode=20000174&type=uid&value=' + target_id + '&containerid=107603' + target_id + '&page=1'
            yield scrapy.Request(url=target_url, callback=self.parse)

    def parse(self, response):
        data_json = json.loads(response.body.decode('utf-8'))
        # print(data_json)
        if data_json['ok'] == 0:
            return
        for card in data_json['data']['cards']:
            if card['card_type'] == 9:
                blog = card['mblog']
                tweet_item = tweet_parse(blog, self.name, self.keywords)
                if self.before_date_enable:
                    creat_at = datetime.datetime.strptime(tweet_item['created_at'], "%Y-%m-%d %H:%M")
                    # print(creat_at.strftime("%Y-%m-%d %H:%M:%S"))
                    if (creat_at - self.before_date).total_seconds() < 0:
                        logger.warning('挖掘消息超过历史消息门限')
                        return
                yield tweet_item
                usr_info = card['mblog']['user']
                user_item = user_parse(usr_info)
                yield user_item
        target_url = response.url
        if target_url.find('&page='):
            current_page = int(target_url.split('&page=')[1]) + 1
            if current_page > self.max_page:
                return
            target_url = target_url.split('&page=')[0] + '&page=' + str(current_page)
            yield scrapy.Request(url=target_url, callback=self.parse)
        else:
            target_url = target_url + '&page=2'
            yield scrapy.Request(url=target_url, callback=self.parse)
