# -*- coding: utf-8 -*-
import json

import logging

import datetime
import redis
import scrapy
from scrapy.exceptions import CloseSpider

from weiboScrapy.config.conf import get_max_page_for_comments, get_before_date
from weiboScrapy.items import CommentItem, UserItem, CommentsUserItem
from weiboScrapy.utils.ItemParse import comment_parse, comment_user_parse
from weiboScrapy.utils.time_transfor import time_trans
import dotenv
from getenv import env

dotenv.read_dotenv('weiboScrapy/.env')

SI_REDIS_CRAWLER_URL = env("SI_REDIS_CRAWLER_URL", "redis://:pass@127.0.0.1:8379/0")
logger = logging.getLogger(__name__)

class CommentsSpider(scrapy.Spider):
    name = 'comments'
    allowed_domains = ['weibo.cn']
    start_urls = ['http://weibo.cn/']

    max_page = get_max_page_for_comments()
    url_for_comments = "https://m.weibo.cn/api/comments/show?id="

    before_date_enable = get_before_date()['enable']
    before_date = datetime.datetime.strptime(get_before_date()['date'], "%Y-%m-%d %H:%M")

    def start_requests(self):
        r = redis.StrictRedis.from_url(SI_REDIS_CRAWLER_URL)
        while True:
            for key in r.scan_iter(match='tweet:*'):
                if str(key).find('tweet') >= 0:
                    tweet_id = r.get(key)
                    r.delete(key)
                    # print(tweet_id.decode(encoding='utf-8'))
                    target_url = self.url_for_comments + tweet_id.decode(encoding='utf-8') + "&page=1"
                    yield scrapy.Request(url=target_url, callback=self.parse)
            if len(r.scan(match='tweet:*')[1]) == 0:
                break

    def parse(self, response):
        # print(response.status)
        if response.status in [404, 403, 418]:
            raise CloseSpider('IP-baned')
        data_json = json.loads(response.body.decode('utf-8'))
        # print(response.body.decode('utf-8'))
        # print(data_json['ok'])
        if data_json['ok'] == 0:
            return
        for data in data_json['data']['data']:
            comment_item = comment_parse(data)
            if self.before_date_enable:
                creat_at = datetime.datetime.strptime(comment_item['created_at'], "%Y-%m-%d %H:%M")
                # print(creat_at.strftime("%Y-%m-%d %H:%M:%S"))
                if (creat_at - self.before_date).total_seconds() < 0:
                    logger.info('挖掘消息超过历史消息门限')
                    return
            yield comment_item
            # usr_info = data['user']
            # user_item = comment_user_parse(usr_info)
            # yield user_item
        target_url = response.url
        if target_url.find('&page=') >= 0:
            current_page = int(target_url.split('&page=')[1]) + 1
            if current_page > self.max_page:
                return
            target_url = target_url.split('&page=')[0] + '&page=' + str(current_page)
            yield scrapy.Request(url=target_url, callback=self.parse)
