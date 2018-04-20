# -*- coding: utf-8 -*-
import scrapy


class TweetsInIDSpider(scrapy.Spider):
    name = 'tweets_in_userid'
    allowed_domains = ['weibo.cn']
    start_urls = ['http://weibo.cn/']

    def start_requests(self):
        pass

    def parse(self, response):
        pass
