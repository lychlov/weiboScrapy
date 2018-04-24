# -*- coding: utf-8 -*-
import json

import redis
import scrapy
from scrapy.exceptions import CloseSpider

from weiboScrapy.config.conf import get_max_page_for_comments
from weiboScrapy.items import CommentItem, UserItem, CommentsUserItem
from weiboScrapy.utils.ItemParse import comment_parse, comment_user_parse
from weiboScrapy.utils.time_transfor import time_trans


class CommentsSpider(scrapy.Spider):
    name = 'comments'
    allowed_domains = ['weibo.cn']
    start_urls = ['http://weibo.cn/']

    max_page = get_max_page_for_comments()
    url_for_comments = "https://m.weibo.cn/api/comments/show?id="

    def start_requests(self):
        r = redis.StrictRedis(host='127.0.0.1', port=6379, db=0)
        while True:
            for key in r.scan_iter(match='tweet:*'):
                if str(key).find('tweet') >= 0:
                    tweet_id = r.get(key)
                    r.delete(key)
                    # print(tweet_id.decode(encoding='utf-8'))
                    target_url = self.url_for_comments + tweet_id.decode(encoding='utf-8') + "&page=1"
                    yield scrapy.Request(url=target_url, callback=self.parse)
            if not bool(r.scan(match='tweet:*')[0]):
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
