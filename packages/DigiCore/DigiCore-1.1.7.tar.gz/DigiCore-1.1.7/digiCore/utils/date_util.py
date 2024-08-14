# _*_ coding: utf-8 _*_
# @Time : 2024/7/30
# @Author : 杨洋
# @Email ： yangyang@doocn.com
# @File : DigiCore
# @Desc :

import datetime
import time

import pandas as pd
from dateutil.relativedelta import relativedelta


def get_month_delta_date(month_delta=1, date_format="%Y%m%d"):
    """
    获取查询时间,起止时间
    默认查询上月数据
    :param month_delta: 间隔月数，少一月为1. 多一月为负一
    :param date_format: 日期格式，少一月为1. 多一月为负一
    :return: ("20230101","20230201")
    """
    last_month_today = datetime.date.today() - relativedelta(months=month_delta)
    start_date = datetime.date(last_month_today.year, last_month_today.month, 1).strftime(date_format)
    this_month_today = datetime.date.today() - relativedelta(months=month_delta - 1)
    end_date = datetime.date(this_month_today.year, this_month_today.month, 1).strftime(date_format)
    return start_date, end_date


def get_date_list(begin_date: str, end_date: str, date_format="%Y%m%d") -> list:
    """
    获取起始时间内每天的日期列表
    :param begin_date: 开始日期
    :param end_date: 结束日期
    :param date_format: 日期格式
    :return list:日期列表
    """
    # 前闭后闭
    date_list = []
    start_date = datetime.datetime.strptime(begin_date, date_format)
    end_date = datetime.datetime.strptime(end_date, date_format)
    while start_date <= end_date:
        date_str = start_date.strftime(date_format)
        date_list.append(date_str)
        start_date += datetime.timedelta(days=1)
    return date_list


def get_date_cycle_list(start_date: str, end_date: str, cycle: int, date_format="%Y-%m-%d") -> list:
    """
    获取日期列表
    :param start_date: 开始时间
    :param end_date: 结束时间
    :param cycle: 查询的时间
    :param date_format: 日期格式
    :return list: 返回日期列表
    """
    date_list = []
    start_date = datetime.datetime.strptime(start_date, date_format)
    end_date = datetime.datetime.strptime(end_date, date_format)
    while True:
        date = {}
        middle_date = start_date + datetime.timedelta(days=cycle)
        # 结束时间
        if middle_date >= end_date:
            date["start"] = start_date
            date["end"] = end_date
            date_list.append(date)
            break
        else:
            date["start"] = start_date
            date["end"] = middle_date
            date_list.append(date)
            start_date = middle_date
    return date_list


def get_begin_end_date(days, date_format="%Y-%m-%d"):
    """
    获取今天，以及前days天的日期
    """
    end_date = time.strftime(date_format, time.localtime())
    offset = datetime.timedelta(days=-int(days))
    start_date = (datetime.datetime.now() + offset).strftime(date_format)
    return start_date, end_date

def get_date_list_by_days(days, date_format="%Y-%m-%d"):
    """
    获取今天时间格式，以及今天之前的前几天
    根据时间范围获取时间列表
    :param days: 间隔天数
    :param date_format: 日期格式

    """
    start_date, end_date = get_begin_end_date(days, date_format)
    return get_date_list(start_date, end_date, date_format)


def get_last_month_date(date_format='%Y-%m-%d'):
    """
    获取上个月的第一天和最后一天的日期
    :return:
    """
    # 获取今天的日期
    today = datetime.date.today()

    # 获取上个月的第一天
    first_day_of_last_month = today.replace(day=1) - datetime.timedelta(days=1)
    first_day_of_last_month = first_day_of_last_month.replace(day=1)

    # 获取上个月的最后一天
    last_day_of_last_month = today.replace(day=1) - datetime.timedelta(days=1)

    begin_date, end_date = first_day_of_last_month.strftime(date_format), last_day_of_last_month.strftime(
        date_format)
    return begin_date, end_date


def process_date(para):
    """
    将天数格式的日期，改为日期格式
    :param para:
    :return:
    """
    try:
        delta = pd.Timedelta(str(int(para)) + 'days')
        time = pd.to_datetime('1899-12-30') + delta
        return time
    except ValueError:
        # 如果字符串不能被转换为日期，返回原始字符串
        return para


if __name__ == '__main__':
    print(get_date_list_by_days(90))
