# -*- coding: utf-8 -*-
import json
import logging
import sys
from twisted.internet import reactor, defer
from scrapy.crawler import CrawlerRunner
from scrapy.utils.log import configure_logging
from yaml import load
from weiboScrapy.spiders.tweets import TweetsSpider
from weiboScrapy.spiders.tweets_to_id import TweetsInIDSpider
from weiboScrapy.spiders.comments import CommentsSpider
from scrapy.utils.project import get_project_settings

logger = logging.getLogger(__name__)

configure_logging()
runner = CrawlerRunner(get_project_settings())


@defer.inlineCallbacks
def crawl(run_args):
    yield runner.crawl(TweetsSpider, run_args=run_args)
    yield runner.crawl(TweetsInIDSpider, run_args=run_args)
    yield runner.crawl(CommentsSpider, run_args=run_args)
    reactor.stop()


if __name__ == '__main__':
    try:
        args = sys.argv[1:]
        input_file_path = args[0]
        with open(input_file_path, 'r') as f:
            input_data = load(f)
        crawl(run_args=input_data)
        reactor.run()
    except RuntimeError as e:
        logger.error(e)
        sys.exit(0)
    except KeyboardInterrupt as e:
        logger.error(e)
        sys.exit(0)
