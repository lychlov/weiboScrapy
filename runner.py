# -*- coding: utf-8 -*-

from twisted.internet import reactor, defer
from scrapy.crawler import CrawlerRunner
from scrapy.utils.log import configure_logging

from weiboScrapy.spiders.tweets import TweetsSpider
from weiboScrapy.spiders.tweets_to_id import TweetsInIDSpider
from weiboScrapy.spiders.comments import CommentsSpider
from scrapy.utils.project import get_project_settings

configure_logging()
runner = CrawlerRunner(get_project_settings())


@defer.inlineCallbacks
def crawl():
    yield runner.crawl(TweetsSpider)
    yield runner.crawl(TweetsInIDSpider)
    yield runner.crawl(CommentsSpider)
    reactor.stop()


crawl()
reactor.run()
