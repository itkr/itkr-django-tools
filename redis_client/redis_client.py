# -*- coding: utf-8 -*-
import redis
from django.conf import settings


class RedisClient(redis.Redis):

    host = settings.REDIS_HOST
    port = settings.REDIS_PORT
    db = settings.REDIS_DB

    @classmethod
    def connection(cls):
        return cls(host=cls.host, port=cls.port, db=cls.db)
