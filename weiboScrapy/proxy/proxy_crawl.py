# -*- coding: utf-8 -*-
import json
import os
import random

import logging
import redis
import requests
from lxml import etree
import dotenv
from getenv import env

from weiboScrapy.constans import SI_REDIS_CRAWLER_URL, API_URL

logger = logging.getLogger(__name__)


class ProxyCrawl:
    def __init__(self):
        self.url = 'http://www.xicidaili.com/wn/'
        self.r = redis.StrictRedis.from_url(SI_REDIS_CRAWLER_URL)
        self.count = 0
        self.api_url = API_URL

    def get_proxy_from_api(self):
        api_https_weibo = self.api_url + 'https/weibo.cn'
        json_data = json.loads(requests.get(api_https_weibo).text)
        proxy_list = json_data.get('proxy_list', [])
        return proxy_list

    def delete_proxy_from_api(self, proxy):
        delete_proxy = self.api_url + 'invalid?proxy=' + proxy
        requests.get(delete_proxy)
        pass

    def load_page(self):

        logger.warning('开始爬取代理')
        self.count = 0
        headers = {
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.186 Safari/537.36',
        }

        html = requests.get(self.url, headers=headers)
        # print(html.text)
        selector = etree.HTML(html.text)

        content_field = selector.xpath('//table[@id="ip_list"]//tr')
        # print(len(content_field))
        for num in range(1, 50):
            ip = content_field[num].xpath('td[2]/text()')[0]
            port = content_field[num].xpath('td[3]/text()')[0]
            proctol = content_field[num].xpath('td[6]/text()')[0]
            proxy_string = proctol.lower() + "://" + ip + ":" + port
            try:
                res = requests.get(url='https://httpbin.org/ip', proxies={'https': ip + ":" + port}, timeout=2).json()
                self.r.set('proxy-' + str(num - 1), proxy_string, ex=600)
                # logger.info("发现可用代理：" + proxy_string)
                self.count = self.count + 1
            except Exception as e:
                pass
        logger.warning("爬取代理完成：共爬取 %s 个代理...", self.count)
        # print(res)

    def get_one_proxy(self):
        proxy_list = self.r.scan(cursor=0, match='proxy-*', count=100)[1]
        if len(proxy_list) == 0:
            self.load_page()
            return self.get_one_proxy()
        key = random.choice(proxy_list)
        ip_string = {'key': key,
                     'proxy_string': bytes.decode(self.r.get(key))}
        return ip_string

    def delete_one_proxy(self, key):
        self.r.delete(key)


if __name__ == '__main__':
    crawl = ProxyCrawl()
    crawl.load_page()
    # print(crawl.get_one_proxy())
