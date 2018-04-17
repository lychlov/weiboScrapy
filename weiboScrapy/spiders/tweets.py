# -*- coding: utf-8 -*-
import scrapy


class TweetsSpider(scrapy.Spider):
    name = 'tweets'
    allowed_domains = ['weibo.com']
    start_urls = ['http://weibo.com/']

    def parse(self, response):
        pass
