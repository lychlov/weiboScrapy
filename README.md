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
- 爬虫设置\settings:scrapy框架总体设置
- 任务调度\scheduler:提供调度运行
## 配置文件
``` yaml
#登录使用的微博
weiboID:
    - username: '15678264837'
      password: 'poiu11292'
    - username: '15577724762'
      password: 'poiu11292'

keywords:
  - word: '绝地求生+XDD'    #词组使用加号连接
  - word: '绝地求生+呆妹儿'
  - word: '焦虑'
  - word: '抑郁+亢奋'

#目标微博ID
targetID:
  - userid: '1575168515'

#翻页上限：
maxPageForTweets: 10000
maxPageForComments: 10000

#当enable为True时，仅爬取date值之前的信息。
beforeDate:
  enable: False
  date: '2018-04-22 00:00'
```
## 输出数据
### tweets
```json
 {
    "_id": "4232336612629942",
    "crawl_type": "tweets",
    "created_at": "2018-04-24 14:26",
    "user_id": 1660334823,
    "reposts_count": 0,
    "tags": "焦虑;",
    "source": "微博 weibo.com",
    "attitudes_count": 0,
    "comments_count": 0,
    "content": "<a class='k' href='https://m.weibo.cn/k/%E8%81%8C%E5%9C%BA%E5%A6%88%E5%A6%88%E7%84%A6%E8%99%91%E5%90%97?from=feed'>#职场妈妈焦虑吗#</a> 发布了头条文章：《Lecoo倍爱宝缓解了我初为人母的焦虑》  <a data-url=\"http://t.cn/RuGmiTm\" href=\"http://media.weibo.cn/article?object_id=1022%3A2309404232336609809699&luicode=10000011&lfid=100103type%3D61%26q%3D%E7%84%A6%E8%99%91%26t%3D0&id=2309404232336609809699&ep=GdzdPb2aq%252C1660334823%252CGdzdPb2aq%252C1660334823\" data-hide=\"\"><span class=\"url-icon\"><img src=\"https://h5.sinaimg.cn/upload/2015/09/25/3/timeline_card_small_article_default.png\"></span></i><span class=\"surl-text\">Lecoo倍爱宝缓解了我初为人母的焦虑</a> ​"
  },
  {
    "_id": "4232336427553235",
    "crawl_type": "tweets",
    "created_at": "2018-04-24 14:25",
    "user_id": 2235986002,
    "reposts_count": 0,
    "tags": "焦虑;",
    "source": "iPhone客户端",
    "attitudes_count": 0,
    "comments_count": 0,
    "content": "焦虑 ​"
  },
  {
    "_id": "4232336243566199", //博文ID
    "crawl_type": "tweets",
    "created_at": "2018-04-24 14:25",//博文发表时间
    "user_id": 3557810930,//博主ID
    "reposts_count": 0,//转发量
    "tags": "抑郁;焦虑;",//包含关键词
    "source": "微博 weibo.com",//来源
    "pics": [],//图片
    "attitudes_count": 0,//点赞量
    "comments_count": 0,//评论量
    "content": "" // 博文内容
  }
```
### users
```json
{
    "_id": 1943878631, //用户ID
    "profile_url": "", //主页地址
    "gender": "f",  //性别
    "verified_type": 220, //认证类型
    "follow_count": 365, //关注量
    "description": "", //用户简介
    "profile_image_url": "",//头像地址
    "verified": false, //是否认证
    "statuses_count": 5593, //发博数量
    "screen_name": "小胖妹纸yun", //昵称
    "followers_count": 517  //粉丝数
  }
```
### comments
```json
{
    "_id": 4221763652693325, //评论ID
    "reply_content": "", //评论中回复原文
    "user_id": 1605254480, //
    "reply_id": 4221634686272064,//评论中回复原文ID
    "created_at": "2018-03-26 00:00",//评论时间
    "source": "微博手机版",//评论终端
    "content": "",   //评论内容
    "like_counts": 0  //评论赞次数
  }
```
## 安装与运行
### 环境要求
- Python 3.5
- MongoDB
- Redis
#### MongoDB和Redis配置
使用django-dotenv 和 django-getenv管理,在.env文件中。
```env
SI_MONGODB_CRAWLER_HOST=mongodb://czk:czk10101@127.0.0.1
SI_MONGODB_CRAWLER_DB=test
SI_REDIS_CRAWLER_HOST=127.0.0.1
SI_REDIS_CRAWLER_PORT=6379
SI_REDIS_CRAWLER_PASS=xxx
```
### 安装
```shell
git clone https://github.com/social-innovation/crawler-weibo.git
cd crawler-weibo
pip3 install -r requirements.txt
```
### 运行
#### 手动运行
```shell
python3 -m scrapy crawl tweets
python3 -m scrapy crawl tweets_to_id
python3 -m scrapy crawl comments
```
#### 自动运行
```shell

```
### 运行测试
```yaml
keywords:
  - word: '绝地求生+XDD'
  - word: '绝地求生+呆妹儿'
  - word: '焦虑'
  - word: '抑郁+亢奋'

#目标微博ID
targetID:
  - userid: '1575168515'

#翻页上限：
maxPageForTweets: 10000
maxPageForComments: 10000
```
2018-04-24 17:04:54 开始执行
2018-04-24 17:26:45 完成
#### 执行结果
所有请求均为200，没有被ban，没有404,403,418等
评论：17345条
微博：2074条
用户：1456人
