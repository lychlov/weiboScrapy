# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import pymongo
import logging
import redis

#         return item



logger = logging.getLogger(__name__)
import dotenv
from getenv import env

dotenv.read_dotenv()

SI_MONGODB_CRAWLER_HOST = env("SI_MONGODB_CRAWLER_HOST", "mongodb://user:pass@127.0.0.1:27017/crawler")
SI_MONGODB_CRAWLER_DB = env("SI_MONGODB_CRAWLER_DB", "test")
SI_REDIS_CRAWLER_HOST = env("SI_REDIS_CRAWLER_HOST", "127.0.0.1")
SI_REDIS_CRAWLER_PORT = env("SI_REDIS_CRAWLER_PORT", "6379")
SI_REDIS_CRAWLER_PASS = env("SI_REDIS_CRAWLER_PASS", None)


class TweetMongoPipeline(object):
    collection_name = 'tweets'

    def __init__(self, mongo_uri, mongo_db):
        self.mongo_uri = mongo_uri
        self.mongo_db = mongo_db
        self.r = redis.StrictRedis(host=SI_REDIS_CRAWLER_HOST, password=SI_REDIS_CRAWLER_PASS,
                                   port=SI_REDIS_CRAWLER_PORT, db=0)

    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            mongo_uri=SI_MONGODB_CRAWLER_HOST,
            mongo_db=SI_MONGODB_CRAWLER_DB
            # mongo_uri=crawler.settings.get('MONGO_URI'),
            # mongo_db=crawler.settings.get('MONGO_DATABASE', 'items')
        )

    def open_spider(self, spider):
        self.client = pymongo.MongoClient(self.mongo_uri)
        self.db = self.client[self.mongo_db]

    def close_spider(self, spider):
        self.client.close()

    def process_item(self, item, spider):
        # 在名为tweets的Collection中存储微博内容信息
        if spider.name == 'tweets' or spider.name == 'tweets_to_id':
            if 'screen_name' not in item:
                self.collection_name = 'tweets'
                try:
                    self.db[self.collection_name].insert_one(dict(item))
                    # 存入redis
                    self.r.set('tweet:' + item['_id'], str(item['_id']))
                    return item
                except Exception as e:
                    logger.info('微博入库失败,ID:' + str(item['_id']))
            # logger.info(e)
            # 在名为users的Collection中存储用户信息
            if 'screen_name' in item:
                self.collection_name = 'users'
                try:
                    self.db[self.collection_name].insert_one(dict(item))
                except Exception as e:
                    pass
                    # logger.info('博主入库失败,ID:' + str(item['_id']))
                # logger.info(e)
                return item

        if spider.name == 'comments':
            if 'screen_name' not in item:
                self.collection_name = 'comments'
                try:
                    self.db[self.collection_name].insert_one(dict(item))
                    return item
                except Exception as e:
                    logger.info('评论入库失败,ID:' + str(item['_id']))
                    # logger.info(e)
            if 'screen_name' in item:
                self.collection_name = 'comments_users'
                try:
                    self.db[self.collection_name].insert_one(dict(item))
                except Exception as e:
                    logger.info('评论人入库失败,ID:' + str(item['_id']))
                    # logger.info(e)
                return item
