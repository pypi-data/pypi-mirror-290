# _*_ coding: utf-8 _*_
# @Time : 2024/7/30
# @Author : 杨洋
# @Email ： yangyang@doocn.com
# @File : DigiCore
# @Desc :
import concurrent.futures

from loguru import logger


def crawl(func, max_workers, *args, **kwargs):
    """
    多线程启动爬虫任务
    """

    with concurrent.futures.ThreadPoolExecutor(max_workers=11) as executor:
        futures = [executor.submit(func, ) for _ in range(max_workers)]
    for future in concurrent.futures.as_completed(futures):
        try:
            future.result()
        except Exception as e:
            logger.error(f'------- 任务执行中发生了异常: {e} -------')

