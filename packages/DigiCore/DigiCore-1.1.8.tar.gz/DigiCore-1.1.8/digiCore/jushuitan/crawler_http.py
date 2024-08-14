# -*- coding: utf-8 -*-
# @Time     : 2024/08/06 09:45
# @Author   : 刘云飞
# @Email    : yfliu@doocn.com
# @FileName : crawler_http.py
import json

from bs4 import BeautifulSoup
from loguru import logger
from requests import Session, Response

from digiCore.common.decorate import def_retry
from digiCore.db.redis.core import RedisDao
from digiCore.jushuitan.config import JUSHUITAN_CRAWLER_HEADERS


# 聚水潭爬虫请求工具类
class RequestHelper:
    def __init__(self):
        redis = RedisDao()
        self.session = Session()
        self.session.headers.update(JUSHUITAN_CRAWLER_HEADERS)
        self.session.cookies.update(redis.get_erp321_cookie())

    @def_retry()
    def jst_crawler_post(self, url, data=None, json=None, **kwargs) -> Response:
        """
        获取聚水潭页面数据
        """
        return self.session.post(url=url, data=data, json=json, **kwargs)

    @def_retry()
    def jst_crawler_get(self, url, params=None, **kwargs) -> Response:
        """
        获取聚水潭页面数据
        """
        return self.session.get(url=url, params=params, **kwargs)

    @def_retry()
    def get_viewstate(self, url):
        """
        获取页面的视图状态和视图状态生成器
        """
        url += '?_c=jst-epaas'
        resp = self.jst_crawler_get(url)
        soup = BeautifulSoup(resp.text, 'html.parser')
        __viewstate = soup.find('input', {'name': '__VIEWSTATE'})['value']
        __viewstate_generator = soup.find('input', {'name': '__VIEWSTATEGENERATOR'})['value']

        return {'viewstate': __viewstate, 'viewstate_generator': __viewstate_generator}

    @def_retry()
    @staticmethod
    def check_response(response: Response):
        """
        校验聚水潭爬虫响应, 返回其中的数据
        :param response:
        :return:
        """
        if response.status_code == 200:
            text = response.text[2:]
            try:
                data = json.loads(text)
            except Exception:
                logger.error(f'请求失败!\n{response.text}')
                return f'请求失败!\n{response.text}'
            is_success = data.get('IsSuccess')
            if is_success:
                result = json.loads(data['ReturnValue'])
                return result
            else:
                logger.error(f'请求失败!\n{response.text}')
                return f'请求失败!\n{response.text}'
        else:
            logger.error('请求失败! ')
            return f'请求失败! {response.text}'
