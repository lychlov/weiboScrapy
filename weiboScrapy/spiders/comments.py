# -*- coding: utf-8 -*-
import json

import redis
import scrapy

from weiboScrapy.items import CommentItem, UserItem, CommentsUserItem
from weiboScrapy.utils.time_transfor import time_trans


class CommentsSpider(scrapy.Spider):
    name = 'comments'
    allowed_domains = ['weibo.cn']
    start_urls = ['http://weibo.cn/']

    max_page = 3
    url_for_comments = "https://m.weibo.cn/api/comments/show?id="

    def start_requests(self):
        r = redis.StrictRedis(host='127.0.0.1', port=6379, db=0)
        while True:
            for key in r.scan_iter():
                if str(key).find('tweet') >= 0:
                    tweet_id = r.get(key)
                    r.delete(key)
                    print(tweet_id.decode(encoding='utf-8'))
                    target_url = self.url_for_comments + tweet_id.decode(encoding='utf-8') + "&page=1"
                    yield scrapy.Request(url=target_url, callback=self.parse)
            if not bool(r.scan()[0]):
                break

    def parse(self, response):
        data_json = json.loads(response.body.decode('utf-8'))
        print(response.body.decode('utf-8'))
        print(data_json['ok'])
        if data_json['ok'] == 0:
            return
        for data in data_json['data']['data']:
            comment_item = CommentItem()
            comment_item['_id'] = data['id']
            created_at = time_trans(data['created_at'])
            comment_item['created_at'] = created_at
            comment_item['source'] = data['source']
            comment_item['user_id'] = data['user']['id']
            comment_item['content'] = data['text']
            if 'reply_id' in data:
                comment_item['reply_id'] = data['reply_id']
                comment_item['reply_content'] = data['reply_text']
            comment_item['like_counts'] = data['like_counts']
            yield comment_item
            user_item = CommentsUserItem()
            usr_info = data['user']
            user_item['_id'] = usr_info['id']
            user_item['screen_name'] = usr_info['screen_name']
            user_item['profile_image_url'] = usr_info['profile_image_url']
            user_item['profile_url'] = usr_info['profile_url']
            user_item['verified'] = usr_info['verified']
            user_item['verified_type'] = usr_info['verified_type']
            if 'verified_reason' in user_item:
                user_item['verified_reason'] = usr_info['verified_reason']
            yield user_item
        target_url = response.url
        if target_url.find('&page=') >= 0:
            current_page = int(target_url.split('&page=')[1]) + 1
            if current_page > self.max_page:
                return
            target_url = target_url.split('&page=')[0] + '&page=' + str(current_page)
            yield scrapy.Request(url=target_url, callback=self.parse)
