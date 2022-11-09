# -*- coding: utf-8 -*-
from __future__ import annotations

from datetime import datetime

from sqlalchemy import Column, DateTime, func, String, types
from sqlalchemy.orm import declared_attr, class_mapper, InstanceState
from sqlalchemy.ext.declarative import as_declarative

from utils import local_session


@as_declarative()
class BasicModel:

    update_by = Column(String, default="cost_center")
    create_by = Column(String, default="cost_center")
    update_time = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    create_time = Column(DateTime, default=datetime.utcnow)

    def __init__(self):
        super(BasicModel, self).__init__()
        self.__session__ = local_session

    @declared_attr
    def __tablename__(cls):
        return cls.__name__.lower()

    @property
    def session(self):
        return self.__session__

    def serialize(self) -> dict:
        column_list = [c.key for c in class_mapper(self.__class__).columns]
        return dict((c, getattr(self, c)) for c in column_list)

    def generate_resource_uuid(self) -> str:
        return "|".join(("{}:{}".format(k, v) for k, v in vars(self).items() if not isinstance(v, InstanceState)))


class ChoicesType(types.TypeDecorator):

    impl = types.String
    cache_ok = True

    def __init__(self, choice: dict, **kwargs):
        self.choices = dict(choice)
        super(ChoicesType, self).__init__(**kwargs)

    def process_bind_param(self, value, dialect):
        return [k for k, v in self.choices.items() if v == value][0]

    def process_result_value(self, value: str, dialect):
        return self.choices[value]
