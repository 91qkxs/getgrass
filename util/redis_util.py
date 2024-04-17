import redis
from config.redis import *


class RedisUtils:
    def __init__(self):
        self.redis_client = self.init_redis()

    def init_redis(self):
        """
        初始化 Redis 连接
        """
        redis_client = redis.StrictRedis(
            host=redis_web3_host,
            port=redis_web3_port,
            db=redis_web3_db,
            password=redis_web3_password,
            decode_responses=True  # 设置为True以便返回字符串而不是字节
        )
        return redis_client

    def set(self, key, value, expiration=None):
        """
        设置缓存
        """
        self.redis_client.set(key, value, ex=expiration)

    def get(self, key):
        """
        获取缓存
        """
        return self.redis_client.get(key)

    def delete(self, key):
        """
        删除缓存
        """
        self.redis_client.delete(key)

    def sadd(self, key, *values):
        """
        将一个或多个元素添加到集合中
        """
        return self.redis_client.sadd(key, *values)

    def sismember(self, key, value):
        """
        检查元素是否在集合中
        """
        return self.redis_client.sismember(key, value)

    def smembers(self, key):
        """
        获取集合中的所有成员
        """
        return self.redis_client.smembers(key)

    def srem(self, key, *values):
        """
        从集合中移除一个或多个元素
        """
        return self.redis_client.srem(key, *values)

