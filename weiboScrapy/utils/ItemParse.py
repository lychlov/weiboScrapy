# -*- coding: utf-8 -*-
from weiboScrapy.items import TweetItem, UserItem, CommentItem, CommentsUserItem
from weiboScrapy.utils.time_transfor import time_trans


def tweet_parse(card, name, keywords):
    item = TweetItem()
    try:
        # 微博信息
        tweet_item = TweetItem()
        # tweet_item['type'] = 'tweet'
        tweet_item['_id'] = card['mblog']['id']
        created_at = time_trans(card['mblog']['created_at'])
        tweet_item['created_at'] = created_at
        tweet_item['crawl_type'] = name
        content = ''
        if not card['mblog']['isLongText']:
            content = card['mblog']['text']
        else:
            content = card['mblog']['longText']['longTextContent']
        tweet_item['content'] = content
        tweet_item['reposts_count'] = card['mblog']['reposts_count']
        tweet_item['comments_count'] = card['mblog']['comments_count']
        tweet_item['attitudes_count'] = card['mblog']['attitudes_count']
        tweet_item['user_id'] = card['mblog']['user']['id']
        tweet_item['source'] = card['mblog']['source']
        if 'pics' in card['mblog']:
            tweet_item['pics'] = card['mblog']['pics']
        tags = ''
        for key_word in keywords:
            word_list = key_word['word'].split('+')
            for word in word_list:
                if content.find(word) >= 0:
                    if not tags.find(word):
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
    except Exception as e:
        print(e)
    return item


def user_parse(usr_info):
    user_item = UserItem()
    try:
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
        print(e)


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
        print(e)


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
        print(e)
