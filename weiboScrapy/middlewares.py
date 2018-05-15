# -*- coding: utf-8 -*-

# Define here the models for your spider middleware
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/spider-middleware.html
import os
import random
import scrapy
from time import sleep
import logging

from scrapy.downloadermiddlewares.retry import RetryMiddleware
from scrapy.exceptions import CloseSpider

from weiboScrapy.config.user_agents import agents

from scrapy import signals

from weiboScrapy.proxy.proxy_crawl import ProxyCrawl

logger = logging.getLogger(__name__)


class WeiboscrapySpiderMiddleware(object):
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the spider middleware does not modify the
    # passed objects.

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_spider_input(self, response, spider):
        # Called for each response that goes through the spider
        # middleware and into the spider.

        # Should return None or raise an exception.
        return None

    def process_spider_output(self, response, result, spider):
        # Called with the results returned from the Spider, after
        # it has processed the response.

        # Must return an iterable of Request, dict or Item objects.
        for i in result:
            yield i

    def process_spider_exception(self, response, exception, spider):
        # Called when a spider or process_spider_input() method
        # (from other spider middleware) raises an exception.

        # Should return either None or an iterable of Response, dict
        # or Item objects.
        pass

    def process_start_requests(self, start_requests, spider):
        # Called with the start requests of the spider, and works
        # similarly to the process_spider_output() method, except
        # that it doesn’t have a response associated.

        # Must return only requests (not items).
        for r in start_requests:
            yield r

    def spider_opened(self, spider):
        spider.logger.info('Spider opened: %s' % spider.name)


class WeiboscrapyDownloaderMiddleware(object):
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the downloader middleware does not modify the
    # passed objects.

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_request(self, request, spider):
        # Called for each request that goes through the downloader
        # middleware.

        # Must either:
        # - return None: continue processing this request
        # - or return a Response object
        # - or return a Request object
        # - or raise IgnoreRequest: process_exception() methods of
        #   installed downloader middleware will be called
        return None

    def process_response(self, request, response, spider):
        # Called with the response returned from the downloader.

        # Must either;
        # - return a Response object
        # - return a Request object
        # - or raise IgnoreRequest

        return response

    def process_exception(self, request, exception, spider):
        # Called when a download handler or a process_request()
        # (from other downloader middleware) raises an exception.

        # Must either:
        # - return None: continue processing this exception
        # - return a Response object: stops process_exception() chain
        # - return a Request object: stops process_exception() chain
        pass

    def spider_opened(self, spider):
        spider.logger.info('Spider opened: %s' % spider.name)


class UserAgentDownloaderMiddleware(object):
    def process_request(self, request, spider):
        agent = random.choice(agents)
        request.headers["User-Agent"] = agent


class ProxyAPIDownloaderMiddleware(object):
    def __init__(self):
        self.proxy_crawl = ProxyCrawl()
        # self.proxy_crawl.load_page()
        self.count = 0
        self.proxy_list = []
        self.proxy_str = ""

    def get_proxy_str(self):
        while len(self.proxy_list) == 0:
            self.proxy_list = self.proxy_crawl.get_proxy_from_api()
            if len(self.proxy_list) > 0:
                break
            else:
                logger.warning("当前代理池中代理资源不足，等待中")
                sleep(30)
        return "https://" + self.proxy_list.pop()

    def process_response(self, request, response, spider):
        # logger.info(str(response.status) + ":" + response.url)
        if response.status in [404, 403, 418]:
            logger.error(str(response.status) + ":" + response.url)
            # raise CloseSpider('IP-baned')
            self.proxy_crawl.delete_proxy_from_api(self.proxy_str)
            self.proxy_str = self.get_proxy_str()
            self.count = 0
            # return
        return response

    def process_request(self, request, spider):
        # 每150次请求换一个代理
        if self.proxy_str == "":
            self.proxy_str = self.get_proxy_str()
        request.meta['proxy'] = self.proxy_str
        self.count = self.count + 1
        if self.count > 150:
            self.proxy_str = self.get_proxy_str()
            self.count = 0

    def process_exception(self, request, exception, spider):
        if isinstance(exception, RetryMiddleware.EXCEPTIONS_TO_RETRY):
            # 删除该代理
            # raise CloseSpider('IP-baned')
            self.proxy_crawl.delete_proxy_from_api(self.proxy_str)
            self.proxy_str = self.get_proxy_str()
            self.count = 0
            return request


class ProxyDownloaderMiddleware(object):
    def __init__(self):
        self.proxy_crawl = ProxyCrawl()
        # self.proxy_crawl.load_page()
        self.count = 0
        self.proxy_json = self.proxy_crawl.get_one_proxy()

    def process_response(self, request, response, spider):
        # logger.info(str(response.status) + ":" + response.url)
        if response.status in [404, 403, 418]:
            logger.error(str(response.status) + ":" + response.url)
            # raise CloseSpider('IP-baned')
            self.proxy_crawl.delete_one_proxy(self.proxy_json['key'])
            self.proxy_json = self.proxy_crawl.get_one_proxy()
            self.count = 0
            return None
        return response

    # def process_exception(self, request, exception, spider):
    #     if isinstance(exception, RetryMiddleware.EXCEPTIONS_TO_RETRY):
    #         # 删除该代理
    #         # raise CloseSpider('IP-baned')
    #         self.proxy_json = self._get_one_proxy()
    #         self.count = 0
    #         return request

    def process_request(self, request, spider):
        # 每150次请求换一个代理
        # proxy = self.proxy_crawl.get_one_proxy()
        # print(self.proxy_json['proxy_string'])
        request.meta['proxy'] = self.proxy_json['proxy_string']
        self.count = self.count + 1
        if self.count > 150:
            self.proxy_crawl.delete_one_proxy(self.proxy_json['key'])
            self.proxy_json = self.proxy_crawl.get_one_proxy()
            self.count = 0
