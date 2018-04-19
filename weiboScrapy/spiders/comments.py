# -*- coding: utf-8 -*-
import scrapy


class CommentsSpider(scrapy.Spider):
    name = 'comments'
    allowed_domains = ['weibo.cn']
    start_urls = ['http://weibo.cn/']

    def parse(self, response):
        pass
