# -*- coding: utf-8 -*-
from scrapy import cmdline

cmdline.execute('scrapy crawl tweets'.split())
cmdline.execute('scrapy crawl tweets_to_id'.split())
cmdline.execute('scrapy crawl comments'.split())
