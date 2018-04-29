# -*- coding: utf-8 -*-
import json

import dotenv
from getenv import env

dotenv.read_dotenv()

SI_MONGODB_CRAWLER_URL = env("SI_MONGODB_CRAWLER_URL", "mongodb://user:pass@127.0.0.1:27017/crawler")
SI_REDIS_CRAWLER_URL = env("SI_REDIS_CRAWLER_URL", "redis://127.0.0.1:6379/0")

