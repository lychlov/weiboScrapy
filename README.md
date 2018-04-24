# 微博爬虫
## 概要设计
https://shimo.im/docs/jzzS9Zp4vS8DL6iq
## 需求
- 根据关键词组和目标微博ID，爬取微博博文、评论等内容
- 将爬取结果保存到MongoDB
- 爬虫可持续运行，增量爬取内容
## 主要模块
- 模拟登录\login：
    - 微博账号模拟登录，维护账号登录状态和cookie。（根据目前测试，登录与否不影响爬取效果）
    - 需手工输入验证码，可接入yundaima实现自动识别。
- IP代理\proxy：爬取免费代理（如：[西刺代理](http://www.xicidaili.com/wn/)),并维护代理池。
    - 每次爬取前自动运行，抓取代理并验证代理可用性。
    - 每个代理的有效期限为10min
- 爬虫\spiders:
    - tweets：根据关键词爬取微博博文和博主信息。
    - tweets_to_id：根据目标微博ID爬取微博博文和博主信息。
    - comments：爬取微博评论和评论人信息
- ITEM\items
    - TweetItem:微博信息字段
    - UserItem:博主信息字段
    - CommentItem:评论信息字段
    - CommentUserItem:评论人信息字段
- Pipeline\pipelines:将爬取信息存入MongoDB
- Middleware\middlewares:
    - User-Agent:随机替换请求使用的user-agent
    - Proxy:每执行150次请求替换当前使用的IP代理
- 任务调度\scheduler:提供调度运行
## 配置文件
'''java
String = 水电费
'''

