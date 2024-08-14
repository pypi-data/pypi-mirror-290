# _*_ coding: utf-8 _*_
# @Time : 2024/7/30
# @Author : 杨洋
# @Email ： yangyang@doocn.com
# @File : DigiCore
# @Desc :
from loguru import logger


def format_log_msg(e):
    """
    格式化错误信息
    :param e:
    :return:
    """
    logger.error(f'error file:{e.__traceback__.tb_frame.f_globals["__file__"]}')
    logger.error(f'error line:{e.__traceback__.tb_lineno}')
    logger.error(f'error message:{e.args}')
    error_msg = {'error_file': e.__traceback__.tb_frame.f_globals["__file__"],
                 'error_line': e.__traceback__.tb_lineno,
                 'error_message': e.args}
    return error_msg