# -*- coding: utf-8 -*-
import json

import redis
import scrapy

from weiboScrapy.config import get_weibo_id_for_tweets, get_keywords
from weiboScrapy.items import TweetItem, UserItem
from weiboScrapy.login import spider_login
from weiboScrapy.utils.ItemParse import tweet_parse, user_parse
from weiboScrapy.utils.time_transfor import time_trans


class TweetsSpider(scrapy.Spider):
    name = 'tweets'
    allowed_domains = ['weibo.cn']
    start_urls = ['http://m.weibo.cn/']
    weibo_id = get_weibo_id_for_tweets()
    keywords = get_keywords()
    # max_page = 100
    max_page = 3
    cookies = ""
    url_for_keywords = "https://m.weibo.cn/api/container/getIndex?containerid=100103type%3D1%26q%3D"

    def start_requests(self):
        # r = redis.StrictRedis(host='127.0.0.1', port=6379, db=0)
        # for id_pair in self.weibo_id:
        #     username = id_pair['username']
        #     self.cookies = r.get(username + '--' + self.name)
        #     if self.cookies.le == 0:
        #         flag = spider_login(username, id_pair['password'], self.name)
        #         if flag:
        #             self.cookies = r.get(username + '--' + self.name)
        #         else:
        #             return
        # 似乎无需登录
        # for id_pair in self.weibo_id:
        #     username = id_pair['username']
        #     password = id_pair['password']
        # self.cookies = spider_login(username, password, self.name)
        for keyword in self.keywords:
            url_for_keyword = self.url_for_keywords + keyword['word']
            yield scrapy.Request(url=url_for_keyword,  callback=self.parse)

    def parse(self, response):
        """
        JSON结构
        {ok:0,1   1代表有数据
        data：
            cards： 数组结构
                "card_type":11,
                "show_type":1, 代表微博
                card_group： 数组，包含微博数据
                    mblog： 微博数据
                        "created_at":"04-17",
                        "id":"4229884136505236",
                        "idstr":"4229884136505236",
                        "mid":"4229884136505236",
                        "can_edit":false,
                        "text":"只要每天进，
                        "textLength":236,
                        "source":"微博 weibo.com",
                        user:用户数据
                        "reposts_count":2008,
                        "comments_count":0,
                        "attitudes_count":1476,
                        "isLongText":false,
                        pics：图片
        """
        data_json = json.loads(response.body.decode('utf-8'))
        # string = json.dumps(data_json)
        # print('--' * 10)
        # print(string)
        # print('--' * 10)
        # f = open('/home/docker/work_space/weiboScrapy/json.txt', 'w')
        # f.write(string)
        # f.close()
        # print('-' * 10)
        # print(data_json['ok'])
        # print('-' * 10)
        if data_json['ok'] == 0:
            return
        cards_list = data_json['data']['cards']
        for cards in cards_list:
            print('进入cards')
            print(cards['card_type'])
            print(cards['show_type'])
            if cards['card_type'] == 11 and cards['show_type'] == 1:
                print('发现微博组')
                for card in cards['card_group']:
                    tweet_item = tweet_parse(card,self.name,self.keywords)
                    yield tweet_item
                    usr_info = card['mblog']['user']
                    user_item = user_parse(usr_info)
                    yield user_item
        # 生成下一页连接
        target_url = response.url
        if target_url.find('&page=') >= 0:
            current_page = int(target_url.split('&page=')[1]) + 1
            if current_page > self.max_page:
                return
            target_url = target_url.split('&page=')[0] + '&page=' + str(current_page)
            yield scrapy.Request(url=target_url, callback=self.parse)
        else:
            target_url = target_url + '&page=2'
            yield scrapy.Request(url=target_url,  callback=self.parse)
