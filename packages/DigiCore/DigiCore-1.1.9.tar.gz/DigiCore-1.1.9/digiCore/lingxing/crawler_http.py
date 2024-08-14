# _*_ coding: utf-8 _*_
# @Time : 2024/7/31
# @Author : 杨洋
# @Email ： yangyang@doocn.com
# @File : DigiCore
# @Desc :
import requests

from digiCore.common.decorate import def_retry
from digiCore.db.redis.core import RedisDao


class RequestHelper:

    def __init__(self):
        self.redis = RedisDao()

    @def_retry()
    def init_lx_headers(self):
        token = self.redis.get_lingxing_crawler_auth_token()
        headers = {
            'X-AK-Company-Id': '901140007506993664',
            'auth-token': token
        }
        return headers

    @def_retry()
    def lx_api_post(self, url, json_data):
        """
        获取领星页面数据
        """
        headers = self.init_lx_headers()
        return requests.post(url=url, headers=headers, json=json_data).json()

    @def_retry()
    def lx_api_get(self, url):
        return requests.get(url=url, headers=self.init_lx_headers()).json()