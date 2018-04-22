# -*- coding: utf-8 -*-
import json

import scrapy

from weiboScrapy.config import get_weibo_id_for_tweets, get_keywords
from weiboScrapy.items import TweetItem
from weiboScrapy.utils.ItemParse import tweet_parse, user_parse
from weiboScrapy.utils.time_transfor import time_trans


class TweetsInIDSpider(scrapy.Spider):
    name = 'tweets_in_userid'
    allowed_domains = ['weibo.cn']
    start_urls = ['http://weibo.cn/']
    keywords = get_keywords()
    target_ids = get_weibo_id_for_tweets()

    def start_requests(self):
        for id in self.target_ids:
            target_url = 'https://m.weibo.cn/api/container/getIndex?uid=' + id + '&luicode=20000174&type=uid&value=' + id + '&containerid=107603' + id + '&page=1'
            yield scrapy.Request(url=target_url, callback=self.parse)

    def parse(self, response):
        data_json = json.loads(response.body.decode('utf-8'))
        for card in data_json['data']['cards']:
            tweet_item = tweet_parse(card, self.name, self.keywords)
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

        pass
