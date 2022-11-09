# -*- coding: utf-8 -*-

# Logging level
LOGGER_LEVEL = "DEBUG"

# 数据库配置
DB_CONFIG = {
    "host": "127.0.0.1",
    "user": "root",
    "password": "",
    "db": "cost_center",
    "port": 3306
}

# Redis 配置
REDIS_CONFIG = {
    "host": "127.0.0.1",
    "port": 6379,
    "db": 2,
    "celery_db": 3
}