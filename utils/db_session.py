# -*- coding: utf-8 -*-
from __future__ import annotations

from abc import ABC, abstractmethod
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session

from config import DB_CONFIG


SQLALCHEMY_DATABASE_URL = 'mysql://%s:%s@%s/%s?charset=utf8' % (DB_CONFIG["user"], DB_CONFIG["password"], DB_CONFIG["host"],  DB_CONFIG["db"])

engine = create_engine(SQLALCHEMY_DATABASE_URL, encoding='utf-8', echo=False, pool_size=100, pool_recycle=10)

local_session = scoped_session(sessionmaker(bind=engine, autocommit=False, autoflush=True, expire_on_commit=False))


class SQLHandler(ABC):

    def __init__(self):
        self.__session__ = local_session

    @property
    def session(self):
        return self.__session__
