# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import pymongo


# class WeiboscrapyPipeline(object):
#     def process_item(self, item, spider):
#         return item


class TweetMongoPipeline(object):
    collection_name = 'tweets'

    def __init__(self, mongo_uri, mongo_db):
        self.mongo_uri = mongo_uri
        self.mongo_db = mongo_db

    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            mongo_uri=crawler.settings.get('MONGO_URI'),
            mongo_db=crawler.settings.get('MONGO_DATABASE', 'items')
        )

    def open_spider(self, spider):
        self.client = pymongo.MongoClient(self.mongo_uri)
        self.db = self.client[self.mongo_db]

    def close_spider(self, spider):
        self.client.close()

    def process_item(self, item, spider):
        # print('-' * 10)
        # print(item['type'])
        # print('-' * 10)
        if 'screen_name' not in item:
            print('-' * 10)
            print(item)
            print('-' * 10)
            self.collection_name = 'tweets'
            self.db[self.collection_name].insert_one(dict(item))
            return item
