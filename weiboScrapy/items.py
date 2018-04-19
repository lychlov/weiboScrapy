# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class WeiboscrapyItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass


class TweetItem(scrapy.Item):
    # type = scrapy.Field()
    _id = scrapy.Field()
    tags = scrapy.Field()
    created_at = scrapy.Field()
    crawl_type = scrapy.Field()
    content = scrapy.Field()
    reposts_count = scrapy.Field()
    comments_count = scrapy.Field()
    attitudes_count = scrapy.Field()
    id_user = scrapy.Field()
    source = scrapy.Field()
    pics = scrapy.Field()
    retweeted_tweetid = scrapy.Field()
    retweeted_content = scrapy.Field()




class UserItem(scrapy.Item):
    _id = scrapy.Field()
    screen_name = scrapy.Field()
    profile_image_url = scrapy.Field()
    profile_url = scrapy.Field()
    statuses_count = scrapy.Field()
    verified = scrapy.Field()
    verified_type = scrapy.Field()
    verified_reason = scrapy.Field()
    description = scrapy.Field()
    gender = scrapy.Field()
    followers_count = scrapy.Field()
    follow_count = scrapy.Field()



class CommentItem(scrapy.Item):
    pass
