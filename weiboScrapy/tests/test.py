# -*- coding: utf-8 -*-
import dotenv
from getenv import env

dotenv.read_dotenv('../')

SI_MONGODB_CRAWLER_HOST = env("SI_MONGODB_CRAWLER_HOST", "mongodb://user:pass@127.0.0.1:27017/crawler")
print(SI_MONGODB_CRAWLER_HOST)
