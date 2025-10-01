from elasticsearch import Elasticsearch
import redis
import time

es = None
cache = None

# Retry logic for Elasticsearch
for attempt in range(10):
    try:
        # Elasticsearch client
        es = Elasticsearch("http://elasticsearch:9200")
        if es.ping():
            break
        else:
            raise ConnectionError("Elasticsearch cluster is not reachable")
    except Exception as e:
        if attempt < 9:
            time.sleep(10)  # Wait for 10 seconds before retrying
        else:
            raise RuntimeError(f"Failed to initialize Elasticsearch client after 10 attempts: {e}")

# Redis client
try:
    cache = redis.Redis(host="redis", port=6379, db=0)
    if not cache.ping():
        raise ConnectionError("Redis server is not reachable")
except (redis.ConnectionError, ConnectionError) as e:
    raise RuntimeError(f"Failed to initialize Redis client: {e}")