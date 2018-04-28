# -*- coding: utf-8 -*-
import logging

from scrapy import signals

logger = logging.getLogger(__name__)


class SpiderCloseExtension(object):
    def __init__(self, stats):
        self.stats = stats

    @classmethod
    def from_crawler(cls, crawler):
        s = cls(crawler.stats)
        crawler.signals.connect(s.spider_closed, signal=signals.spider_closed)
        return s

    def spider_closed(self, spider):
        logger.warning("Spider:%s 停止运行...", spider.name)
        logger.warning("本次爬取概况：")
        start_time = self.stats.get_value('start_time').strftime('%Y-%m-%d %H:%M:%S')
        finish_time = self.stats.get_value('finish_time').strftime('%Y-%m-%d %H:%M:%S')

        logger.warning("开始时间：%s      结束时间：%s" % (start_time, finish_time))
        logger.warning("共计发送请求 %s 次，成功 %s 次；" % (self.stats.get_value('downloader/request_method_count/GET', 0),
                                                 self.stats.get_value('downloader/response_status_count/200', 0)))
        proxy_error = 0
        proxy_error = proxy_error + int(
            self.stats.get_value('retry/reason_count/twisted.internet.error.ConnectionRefusedError', 0))
        proxy_error = proxy_error + int(self.stats.get_value(
            'retry/reason_count/twisted.internet.error.TimeoutError', 0))
        proxy_error = proxy_error + int(self.stats.get_value(
            'retry/reason_count/twisted.web._newclient.ResponseNeverReceived', 0))
        logger.warning("因代理原因失败的请求数为：%s ;" % proxy_error)
        logger.warning("共计获取数据 %s 条。" % self.stats.get_value('item_scraped_count', 0))
        logger.warning("结束原因：%s 。" % self.stats.get_value('finish_reason'))
        # print(self.stats.get_stats())
