import redis


class Redis:
    redis_client = redis.StrictRedis(host='localhost', port=6379, db=0)

    @classmethod
    def save(cls, key, value, expire_time):
        return cls.redis_client.setex(key, expire_time, value)

    @classmethod
    def get(cls, key):
        return cls.redis_client.get(key)
