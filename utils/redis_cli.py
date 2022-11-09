# -*- coding: utf-8 -*-
from __future__ import annotations
import redis

from config import REDIS_CONFIG
from utils import logger


class RedisClient:

    redis_pool = False

    def __init__(self):
        host = REDIS_CONFIG["host"]
        port = REDIS_CONFIG["port"]
        num = REDIS_CONFIG["db"]
        if self.redis_pool:
            pass
        else:
            logger.info("init redis pool")
            self.redis_pool = redis.ConnectionPool(host=host, port=port, db=num, decode_responses=True)
            RedisClient.redis_pool = self.redis_pool

    def get_redis_client(self):
        return redis.Redis(connection_pool=self.redis_pool, health_check_interval=15)

    def get_redis_pool(self):
        return self.redis_pool
