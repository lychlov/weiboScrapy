# -*- coding: utf-8 -*-
import json
import logging
import sys
from twisted.internet import reactor, defer
from scrapy.crawler import CrawlerRunner
from scrapy.utils.log import configure_logging

from weiboScrapy.spiders.tweets import TweetsSpider
from weiboScrapy.spiders.tweets_to_id import TweetsInIDSpider
from weiboScrapy.spiders.comments import CommentsSpider
from scrapy.utils.project import get_project_settings

logger = logging.getLogger(__name__)

configure_logging()
runner = CrawlerRunner(get_project_settings())


@defer.inlineCallbacks
def crawl():
    yield runner.crawl(TweetsSpider)
    yield runner.crawl(TweetsInIDSpider)
    yield runner.crawl(CommentsSpider)
    reactor.stop()


if __name__ == '__main__':
    try:
        crawl()
        reactor.run()
    except RuntimeError as e:
        logger.error(e)
    except KeyboardInterrupt as e:
        logger.error(e)
    sys.exit(0)
