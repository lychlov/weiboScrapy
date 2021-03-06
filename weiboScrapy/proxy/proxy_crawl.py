# -*- coding: utf-8 -*-
import os
import random

import logging
import redis
import requests
from lxml import etree

logger = logging.getLogger(__name__)

class ProxyCrawl:
    def __init__(self):
        self.url = 'http://www.xicidaili.com/wn/'
        self.r = redis.StrictRedis(host='127.0.0.1', port=6379, db=0)

    def load_page(self):
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
            # print(ip)
            # print(str(ip))
            port = content_field[num].xpath('td[3]/text()')[0]
            # print(port)
            proctol = content_field[num].xpath('td[6]/text()')[0]
            # print(proctol)
            proxy_string = proctol.lower() + "://" + ip + ":" + port
            # print(proxy_string)
            try:
                res = requests.get(url='https://httpbin.org/ip', proxies={'https': ip + ":" + port}, timeout=2).json()
                self.r.set('proxy-' + str(num - 1), proxy_string, ex=600)
                logger.info("发现可用代理：" + proxy_string)
            except Exception as e:
                pass
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
