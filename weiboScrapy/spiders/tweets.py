# -*- coding: utf-8 -*-
import json

import redis
import scrapy

from weiboScrapy.config import get_weibo_id, get_keywords
from weiboScrapy.login import spider_login


class TweetsSpider(scrapy.Spider):
    name = 'tweets'
    allowed_domains = ['weibo.cn']
    start_urls = ['http://m.weibo.cn/']
    weibo_id = get_weibo_id()
    keywords = get_keywords()

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
        for id_pair in self.weibo_id:
            username = id_pair['username']
            password = id_pair['password']
        self.cookies = spider_login(username, password, self.name)
        for keyword in self.keywords:
            url_for_keyword = self.url_for_keywords + keyword['word']
            yield scrapy.Request(url=url_for_keyword, cookies=self.cookies, callback=self.parse)

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
        string = json.dumps(data_json)
        print('--' * 10)
        print(string)
        print('--' * 10)
        f = open('/Users/zhikuncheng/IdeaProjects/weiboScrapy/json.txt', 'w')
        f.write(string)
        f.close()

        pass
