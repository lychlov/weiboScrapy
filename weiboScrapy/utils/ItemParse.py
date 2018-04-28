# -*- coding: utf-8 -*-
import logging

from weiboScrapy.items import TweetItem, UserItem, CommentItem, CommentsUserItem
from weiboScrapy.utils.time_transfor import time_trans

logger = logging.getLogger(__name__)


def tweet_parse(blog, name, keywords):
    try:
        # print('-'*10)
        # print(blog)
        # print('-'*10)
        # 微博信息
        tweet_item = TweetItem()
        # tweet_item['type'] = 'tweet'
        tweet_item['_id'] = blog['id']
        created_at = time_trans(blog['created_at'])
        tweet_item['created_at'] = created_at
        tweet_item['crawl_type'] = name
        content = ''
        # print(not blog['isLongText'])
        # print('longText' not in blog)
        if not blog['isLongText']:
            content = blog['text']
        else:
            if 'longText' in blog:
                content = blog['longText']['longTextContent']
            else:
                content = blog['text']
        tweet_item['content'] = content
        tweet_item['reposts_count'] = blog['reposts_count']
        tweet_item['comments_count'] = blog['comments_count']
        tweet_item['attitudes_count'] = blog['attitudes_count']
        tweet_item['user_id'] = blog['user']['id']
        tweet_item['source'] = blog['source']
        if 'pics' in blog:
            tweet_item['pics'] = blog['pics']
        tags = str('')
        for key_word in keywords:
            word_list = key_word['word'].split('+')
            for word in word_list:
                if content.find(word) >= 0:
                    if tags.find(word) < 0:
                        tags = tags + word + ";"
        tweet_item['tags'] = tags
        if 'retweeted_status' in blog:
            tweet_item['retweeted_tweetid'] = blog['retweeted_status']['id']
            retweeted_content = ""
            if not blog['retweeted_status']['isLongText']:
                retweeted_content = blog['retweeted_status']['text']
            else:
                retweeted_content = blog['retweeted_status']['longText']['longTextContent']
                tweet_item['retweeted_content'] = retweeted_content
        # print("返回了tweet_item")
        return tweet_item
    except Exception as e:
        # logger.error('生成tweet发生错误：')
        # logger.error(e)
        pass

def user_parse(usr_info):
    try:
        user_item = UserItem()
        # tweet_item['type'] = 'user'
        user_item['_id'] = usr_info['id']
        user_item['screen_name'] = usr_info['screen_name']
        user_item['profile_image_url'] = usr_info['profile_image_url']
        user_item['profile_url'] = usr_info['profile_url']
        user_item['statuses_count'] = usr_info['statuses_count']
        user_item['verified'] = usr_info['verified']
        user_item['verified_type'] = usr_info['verified_type']
        if 'verified_reason' in user_item:
            user_item['verified_reason'] = usr_info['verified_reason']
        user_item['description'] = usr_info['description']
        user_item['gender'] = usr_info['gender']
        user_item['followers_count'] = usr_info['followers_count']
        user_item['follow_count'] = usr_info['follow_count']
        return user_item
    except Exception as e:
        logger.error('生成博主发生错误：')
        logger.error(e)


def comment_parse(data):
    try:
        comment_item = CommentItem()
        comment_item['_id'] = data['id']
        created_at = time_trans(data['created_at'])
        comment_item['created_at'] = created_at
        comment_item['source'] = data['source']
        comment_item['user_id'] = data['user']['id']
        comment_item['content'] = data['text']
        if 'reply_id' in data:
            comment_item['reply_id'] = data['reply_id']
            comment_item['reply_content'] = data['reply_text']
        comment_item['like_counts'] = data['like_counts']
        return comment_item
    except Exception as e:
        logger.error('生成评论发生错误：')
        logger.error(e)


def comment_user_parse(usr_info):
    user_item = CommentsUserItem()
    try:
        user_item['_id'] = usr_info['id']
        user_item['screen_name'] = usr_info['screen_name']
        user_item['profile_image_url'] = usr_info['profile_image_url']
        user_item['profile_url'] = usr_info['profile_url']
        user_item['verified'] = usr_info['verified']
        user_item['verified_type'] = usr_info['verified_type']
        if 'verified_reason' in user_item:
            user_item['verified_reason'] = usr_info['verified_reason']
        return user_item
    except Exception as e:
        logger.error('生成评论用户发生错误：')
        logger.error(e)
