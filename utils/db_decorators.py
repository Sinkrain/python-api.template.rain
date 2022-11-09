# -*- coding: utf-8 -*-
from functools import wraps

from utils.logger import logger


def transactional(func):
    """
    service中的函数装饰器，用来开启事务和提交事务以及遇到错误时的事务回滚
    :param func: 需要被装饰的函数
    :return:
    """
    @wraps(func)
    def wrapper(self, *args, **kwargs):
        is_commit = True
        try:
            return func(self, *args, **kwargs)
        except Exception as e:
            is_commit = False
            logger.error('%s', e)
            raise
        finally:
            if is_commit:
                self.session.commit()
            else:
                logger.info('close transaction, is_commit=%s', str(is_commit))
                self.session.rollback()
            self.session.remove()
    return wrapper
