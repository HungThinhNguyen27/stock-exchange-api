import redis
from config import Config
from utils.slack_bot import send_error_to_slack

REDIS_PORT = Config.REDIS_PORT
REDIS_HOST = Config.REDIS_HOST
# 6379
# redis


class RedisConnect:
    def __init__(self):
        try:
            self.redis_cache = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, db=0)
            self.redis_cache.ping()
        except redis.exceptions.ConnectionError as e:
            error_message = f"Redis connection error occurred: {str(e)}"
            send_error_to_slack(error_message)
            raise 
    

    def add_to_cache(self, key, value, expire):
        self.redis_cache.set(key, value, ex=expire)

    def get_from_cache(self, key):  
        value = self.redis_cache.get(key)
        if value is None:
            return None
        return value.decode('utf-8')
