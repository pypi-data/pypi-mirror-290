# _*_ coding: utf-8 _*_
# @Time : 2024/7/31
# @Author : 杨洋
# @Email ： yangyang@doocn.com
# @File : DigiCore
# @Desc :
import copy
import time
from urllib import parse
from typing import Union

import requests
from loguru import logger
from orjson import orjson

from digiCore.common.decorate import def_retry
from digiCore.db.redis.core import RedisDao
from digiCore.lingxing.config import APP_ID, HEADERS, SC_BASE_URL, NO_SC_BASE_URL
from digiCore.lingxing.util import EncryptTool
from typing import Optional


class SignBase(object):

    @classmethod
    def generate_sign(cls, encrypt_key: str, request_params: dict) -> str:
        """
        生成签名
        """
        canonical_querystring = cls.format_params(request_params)
        md5_str = EncryptTool.md5_encrypt(canonical_querystring).upper()
        sign = EncryptTool.aes_encrypt(encrypt_key, md5_str)
        return sign

    @classmethod
    def format_params(cls, request_params: Union[None, dict] = None) -> str:
        """
        格式化 params
        """
        if not request_params or not isinstance(request_params, dict):
            return ''

        canonical_strs = []
        sort_keys = sorted(request_params.keys())
        for k in sort_keys:
            v = request_params[k]
            if v == "":
                continue
            elif isinstance(v, (dict, list)):
                # 如果直接使用 json, 则必须使用separators=(',',':'), 去除序列化后的空格, 否则 json中带空格就导致签名异常
                # 使用 option=orjson.OPT_SORT_KEYS 保证dict进行有序 序列化(因为最终要转换为 str进行签名计算, 需要保证有序)
                canonical_strs.append(f"{k}={orjson.dumps(v, option=orjson.OPT_SORT_KEYS).decode()}")
            else:
                canonical_strs.append(f"{k}={v}")
        return "&".join(canonical_strs)


class OpenApi(object):
    """"
    获取 sign签名，完成必要参数的获取
    返回字典数据
    data = {
            'api_name': self.api_name, # 传参
            'params': params,
            'lingxing_api': full_api
        }
    :param api_route 领星开发文档的接口路由地址，通过数据库dim_lingxing_api_info_a_mannal 可以查看
    :param access_token 领星接口数据请求 必须参数
    :param app_id   获取 access_token 的必须参数
    :param secret_key   获取 access_token 的必须参数
    """

    def __init__(self,
                 req_body: dict,
                 api_route: str,
                 url_type: Optional[int] = 1  # 1 为 带sc ；2 为 不带 sc
                 ):
        self.redis = RedisDao()
        self.req_body = req_body
        self.api_route = api_route
        self.url_type = url_type

    def get_req_params(self, req_params=None):
        """
        根据传参进行签名，并将签名加入到参数中
        :param req_params:
        :return:
        """
        access_token = self.redis.get_lingxing_api_access_token()
        req_params = req_params or {}
        gen_sign_params = copy.deepcopy(self.req_body) if self.req_body else {}
        if req_params:
            gen_sign_params.update(req_params)

        sign_params = {
            "app_key": APP_ID,
            "access_token": access_token,
            "timestamp": f'{int(time.time())}'
        }
        gen_sign_params.update(sign_params)
        sign = SignBase.generate_sign(APP_ID, gen_sign_params)
        sign_params["sign"] = sign
        req_params.update(sign_params)
        return req_params

    def get_full_api_url(self, params):
        """
        获取完整的怕拼接url
        :param params: 经过sign签名获取到的参数字典
        :return:
        """
        if self.url_type == 1:
            BASE_URL = SC_BASE_URL
        elif self.url_type == 2:
            BASE_URL = NO_SC_BASE_URL
        else:
            BASE_URL = SC_BASE_URL
            logger.error(f'{self.url_type} 参数不正确！只能为1 或 2！')
        base_url = BASE_URL + self.api_route
        str_params = parse.urlencode(params)
        return f'{base_url}?{str_params}'

    def get_lingxing_api(self):
        """
        返回接口请求数据
        :return: dict
        """
        params = self.get_req_params()
        full_api = self.get_full_api_url(params)
        data = {
            'params': params,
            'lingxing_api': full_api
        }
        return data

    @def_retry(msg='请求lingxing api失败！')
    def sync_lingxing_data(self):
        """
        请求lingxing_api，获取response
        :return:
        """
        data = self.get_lingxing_api()
        lingxing_api = data.get('lingxing_api')
        response = requests.post(url=lingxing_api, headers=HEADERS, json=self.req_body, timeout=20).json()
        return response


if __name__ == '__main__':
    task_json = {
        "date": time.strftime("%Y-%m", time.localtime())
    }
    api = OpenApi(
        req_body=task_json,
        api_route='/routing/finance/currency/currencyMonth'
    )
    res = api.sync_lingxing_data()
    print(res)
