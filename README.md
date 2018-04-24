# 微博爬虫
## 概要设计
https://shimo.im/docs/jzzS9Zp4vS8DL6iq
## 需求
- 根据关键词组和目标微博ID，爬取微博博文、评论等内容
- 将爬取结果保存到MongoDB
- 爬虫可持续运行，增量爬取内容
## 主要模块
- 模拟登录\login：
- IP代理\proxy:

- 爬虫\spiders:
    - tweets：
    - tweets_to_id
    - comments：
- ITEM\items
    - TweetItem:
    - UserItem:
    - CommentItem:
    - CommentUserItem:
- Pipeline\pipelines:
- 任务调度\scheduler:

