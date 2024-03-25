import redis
import json


class RedisConnect:
    def __init__(self):
        self.redis_cache = redis.Redis(host='redis', port=6379, db=0)

    def add_to_cache(self, key, value):
        self.redis_cache.set(key, value, ex=3600)

    def get_from_cache(self, key):
        value = self.redis_cache.get(key)
        if value is None:
            return None
        return value.decode('utf-8')
