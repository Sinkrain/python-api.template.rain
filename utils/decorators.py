# -*- coding: utf-8 -*-
from __future__ import annotations

import json
import time
import traceback
from typing import Any
from flask import Response, request
from functools import wraps
from .logger import logger


def capture_exception(func):
    """
    捕捉异常
    """
    @wraps(func)
    def wrap(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            logger.error(e)
            logger.error(traceback.format_exc())
            raise Exception(e)
    return wrap


def capture_sync_ops(operation: str, m: int = 6, t_unit: int = 5, capture_rsp: Any = False):
    """
    用于捕获具体的 operation 的异常
    :param operation: 操作的名称
    :param m: 超时 minutes
    :param t_unit: 等待时间
    :param capture_rsp: 异常返回信息
    """

    def decorate(func):

        @wraps(func)
        def wrapper(self, *args, **kwargs):
            c_timestamp = time.time()
            # 动态变更 timeout 时， 使用 self 对象的内部属性
            if hasattr(self, "sync_switch") and hasattr(self, "sync_timeout") and getattr(self, "sync_switch"):
                w_timeout = 60 * getattr(self, "sync_timeout")
            else:
                w_timeout = 60 * m
            c_timestamp += w_timeout
            try:
                logger.info(">> sync minutes: {} time_unit: {}s <<".format(int(w_timeout / 60), t_unit))
                while True:
                    is_ok = func(self, *args, **kwargs)
                    if is_ok:
                        return is_ok
                    logger.info("wait for {} ...".format(operation))
                    time.sleep(t_unit)
                    # 判断是否超时
                    if time.time() >= c_timestamp:
                        logger.info("{} timeout, please check and retry".format(operation))
                        return capture_rsp
            except Exception as e:
                logger.error(traceback.format_exc())
                return capture_rsp

        return wrapper
    return decorate


def validate_request_args(method: str, validate_args: (list, tuple), notnull: bool = True):
    """
    校验 flask 的请求参数是否有缺失
    """
    def decorate(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            base_response = {
                "meta": {
                    "code": 200,
                    "type": "OK",
                    "message": "successfully"
                },
                "data": None
            }
            check_method = ("get", "post", "patch")
            if method.lower() not in check_method:
                message = "don't support the method: {}".format(method)
                logger.error(message)
                raise Exception(message)
            # 获取 request 的 data 信息
            if method.lower() == check_method[0]:
                req_args = request.args
            elif method.lower() == check_method[2]:
                req_args = request.view_args
            elif request.is_json:
                req_args = request.json
            else:
                base_response["meta"]["code"] = 400
                base_response["meta"]["type"] = "Bad request"
                base_response["meta"]["message"] = "Request Miss args: {}".format(validate_args)
                return Response(json.dumps(base_response), status=400, mimetype="application/json")
            miss_args = set(validate_args) - set(req_args.keys())
            if len(miss_args) > 0:
                base_response["meta"]["code"] = 400
                base_response["meta"]["type"] = "Bad request"
                base_response["meta"]["message"] = "Miss args: {}".format(miss_args)
                return Response(json.dumps(base_response), status=400, mimetype="application/json")
            if notnull:
                null_args = [arg for arg in validate_args if req_args.get(arg) is None]
                if len(null_args) > 0:
                    base_response["meta"]["code"] = 400
                    base_response["meta"]["type"] = "Bad request"
                    base_response["meta"]["message"] = "Request args not allowed to be null: {}".format(null_args)
                    return Response(json.dumps(base_response), status=400, mimetype="application/json")

            return func(*args, **kwargs)
        return wrapper
    return decorate
