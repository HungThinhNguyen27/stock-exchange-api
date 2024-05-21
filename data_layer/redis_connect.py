import redis
from config import Config

REDIS_PORT = Config.REDIS_PORT
REDIS_HOST = Config.REDIS_HOST
# 6379
# redis


class RedisConnect:
    def __init__(self):
        self.redis_cache = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, db=0)

    def add_to_cache(self, key, value, expire):
        self.redis_cache.set(key, value, ex=expire)

    def get_from_cache(self, key):
        value = self.redis_cache.get(key)
        if value is None:
            return None
        return value.decode('utf-8')
