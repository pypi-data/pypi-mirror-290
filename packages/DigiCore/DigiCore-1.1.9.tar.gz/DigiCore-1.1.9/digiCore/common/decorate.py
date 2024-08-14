# _*_ coding: utf-8 _*_
# @Time : 2024/8/2
# @Author : 杨洋
# @Email ： yangyang@doocn.com
# @File : DigiCore
# @Desc :
import time
from functools import wraps
from typing import Optional

from loguru import logger

from digiCore.common.setting import Status


def def_retry(
        msg: Optional[str] = '',
        error_type=Status.BAD_REQUEST,
        max_retry_count: Optional[int] = 5,
        time_interval: Optional[int] = 2):
    """
    任务重试装饰器
    Args:
    max_retry_count: 最大重试次数 默认5次
    time_interval: 每次重试间隔 默认2s
    """

    def _retry(task_func):
        @wraps(task_func)
        def wrapper(*args, **kwargs):
            for _ in range(max_retry_count):
                try:
                    task_result = task_func(*args, **kwargs)
                    return task_result
                except Exception as e:
                    logger.error(Status.describe(error_type))
                    logger.error(f'error message:{e.args}' or msg)
                    time.sleep(time_interval)
            return

        return wrapper

    return _retry
