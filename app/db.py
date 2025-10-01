from elasticsearch import Elasticsearch
import redis

# Elasticsearch client
es = Elasticsearch("http://elasticsearch:9200")

# Redis client
cache = redis.Redis(host="redis", port=6379, db=0)