# -*- coding: utf-8 -*-
import json

import dotenv
import pymongo
from getenv import env

dotenv.read_dotenv('weiboScrapy/.env')

SI_MONGODB_CRAWLER_URL = env("SI_MONGODB_CRAWLER_URL", "mongodb://user:pass@127.0.0.1:27017/crawler")
client = pymongo.MongoClient(SI_MONGODB_CRAWLER_URL)
db = client.get_database()
print(db.name)
