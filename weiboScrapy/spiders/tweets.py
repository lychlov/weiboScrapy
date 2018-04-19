# -*- coding: utf-8 -*-
import json

import redis
import scrapy

from weiboScrapy.config import get_weibo_id, get_keywords
from weiboScrapy.items import TweetItem, UserItem
from weiboScrapy.login import spider_login
from weiboScrapy.utils.time_transfor import time_trans


class TweetsSpider(scrapy.Spider):
    name = 'tweets'
    allowed_domains = ['weibo.cn']
    start_urls = ['http://m.weibo.cn/']
    weibo_id = get_weibo_id()
    keywords = get_keywords()
    # max_page = 100
    max_page = 3
    cookies = ""
    url_for_keywords = "https://m.weibo.cn/api/container/getIndex?containerid=100103type%3D1%26q%3D"

    def start_requests(self):
        # r = redis.StrictRedis(host='127.0.0.1', port=6379, db=0)
        # for id_pair in self.weibo_id:
        #     username = id_pair['username']
        #     self.cookies = r.get(username + '--' + self.name)
        #     if self.cookies.le == 0:
        #         flag = spider_login(username, id_pair['password'], self.name)
        #         if flag:
        #             self.cookies = r.get(username + '--' + self.name)
        #         else:
        #             return
        for id_pair in self.weibo_id:
            username = id_pair['username']
            password = id_pair['password']
        self.cookies = spider_login(username, password, self.name)
        for keyword in self.keywords:
            url_for_keyword = self.url_for_keywords + keyword['word']
            yield scrapy.Request(url=url_for_keyword, cookies=self.cookies, callback=self.parse)

    def parse(self, response):
        """
        JSON结构
        {ok:0,1   1代表有数据
        data：
            cards： 数组结构
                "card_type":11,
                "show_type":1, 代表微博
                card_group： 数组，包含微博数据
                    mblog： 微博数据
                        "created_at":"04-17",
                        "id":"4229884136505236",
                        "idstr":"4229884136505236",
                        "mid":"4229884136505236",
                        "can_edit":false,
                        "text":"只要每天进，
                        "textLength":236,
                        "source":"微博 weibo.com",
                        user:用户数据
                        "reposts_count":2008,
                        "comments_count":0,
                        "attitudes_count":1476,
                        "isLongText":false,
                        pics：图片
        """
        data_json = json.loads(response.body.decode('utf-8'))
        string = json.dumps(data_json)
        # print('--' * 10)
        # print(string)
        # print('--' * 10)
        f = open('/home/docker/work_space/weiboScrapy/json.txt', 'w')
        f.write(string)
        f.close()
        print('-' * 10)
        print(data_json['ok'])
        print('-' * 10)
        if data_json['ok'] == 0:
            return
        cards_list = data_json['data']['cards']
        for cards in cards_list:
            print('进入cards')
            print(cards['card_type'])
            print(cards['show_type'])
            if cards['card_type'] == 11 and cards['show_type'] == 1:
                print('发现微博组')
                for card in cards['card_group']:
                    try:
                        # 微博信息
                        tweet_item = TweetItem()
                        # tweet_item['type'] = 'tweet'
                        tweet_item['_id'] = card['mblog']['id']
                        created_at = time_trans(card['mblog']['created_at'])
                        tweet_item['created_at'] = created_at
                        tweet_item['crawl_type'] = self.name
                        content = ''
                        if not card['mblog']['isLongText']:
                            content = card['mblog']['text']
                        else:
                            content = card['mblog']['longText']['longTextContent']
                        tweet_item['content'] = content
                        tweet_item['reposts_count'] = card['mblog']['reposts_count']
                        tweet_item['comments_count'] = card['mblog']['comments_count']
                        tweet_item['attitudes_count'] = card['mblog']['attitudes_count']
                        tweet_item['id_user'] = card['mblog']['user']['id']
                        tweet_item['source'] = card['mblog']['source']
                        if 'pics' in card['mblog']:
                            tweet_item['pics'] = card['mblog']['pics']
                        tags = ''
                        for key_word in self.keywords:
                            word_list = key_word['word'].split('+')
                            for word in word_list:
                                if content.find(word) >= 0:
                                    tags = tags + word + ";"
                        tweet_item['tags'] = tags
                        if 'retweeted_status' in card['mblog']:
                            tweet_item['retweeted_tweetid'] = card['mblog']['retweeted_status']['id']
                            retweeted_content = ""
                            if not card['mblog']['retweeted_status']['isLongText']:
                                retweeted_content = card['mblog']['retweeted_status']['text']
                            else:
                                retweeted_content = card['mblog']['retweeted_status']['longText']['longTextContent']
                                tweet_item['retweeted_content'] = retweeted_content
                        print("返回了tweet_item")
                        yield tweet_item
                        # 用户信息
                        user_item = UserItem()
                        usr_info = card['mblog']['user']
                        # tweet_item['type'] = 'user'
                        user_item['_id'] = usr_info['id']
                        user_item['screen_name'] = usr_info['screen_name']
                        user_item['profile_image_url'] = usr_info['profile_image_url']
                        user_item['profile_url'] = usr_info['profile_url']
                        user_item['statuses_count'] = usr_info['statuses_count']
                        user_item['verified'] = usr_info['verified']
                        user_item['verified_type'] = usr_info['verified_type']
                        user_item['verified_reason'] = usr_info['verified_reason']
                        user_item['description'] = usr_info['description']
                        user_item['gender'] = usr_info['gender']
                        user_item['followers_count'] = usr_info['followers_count']
                        user_item['follow_count'] = usr_info['follow_count']
                        yield user_item
                    except Exception as e:
                        print('-' * 10)
                        print('发生了异常')
                        print(e)
                        print('-' * 10)

        # 生成下一页连接
        target_url = response.url
        if target_url.find('&page=') >= 0:
            current_page = int(target_url.split('&page=')[1]) + 1
            if current_page > self.max_page:
                return
            target_url = target_url.split('&page=')[0] + '&page=' + str(current_page)
            yield scrapy.Request(url=target_url, cookies=self.cookies, callback=self.parse)
        else:
            target_url = target_url + '&page=2'
            yield scrapy.Request(url=target_url, cookies=self.cookies, callback=self.parse)
