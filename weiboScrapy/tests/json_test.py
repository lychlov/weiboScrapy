# -*- coding: utf-8 -*-
import json

import dotenv
import pymongo
from getenv import env

from weiboScrapy.constans import SI_MONGODB_CRAWLER_URL


client = pymongo.MongoClient(SI_MONGODB_CRAWLER_URL)
db = client.get_database()
print(db.name)
