# -*- coding: utf-8 -*-
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

        r = redis.StrictRedis(host='127.0.0.1', port=6379, db=0)
        for id_pair in self.weibo_id:
            username = id_pair['username']
            self.cookies = r.get(username + '--' + self.name)
            if self.cookies.le == 0:
                flag = spider_login(username, id_pair['password'], self.name)
                if flag:
                    self.cookies = r.get(username + '--' + self.name)
                else:
                    return
        for keyword in self.keywords:
            url_for_keyword = self.url_for_keywords + keyword
            yield scrapy.Request(url=url_for_keyword, cookies=self.cookies, callback=self.parse)

    def parse(self, response):
        pass
