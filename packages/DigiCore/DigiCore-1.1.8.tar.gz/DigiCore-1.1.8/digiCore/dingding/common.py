# _*_ coding: utf-8 _*_
# @Time : 2024/8/2
# @Author : 杨洋
# @Email ： yangyang@doocn.com
# @File : DigiCore
# @Desc :
from typing import Optional

import requests

from loguru import logger

from digiCore.common.decorate import def_retry
from digiCore.common.setting import Status
from digiCore.db.redis.core import RedisDao


class DingdingCommon:

    def __init__(self):
        self.redis_ob = RedisDao()

    def init_dingding_headers(self):
        """
        初始化headers
        """
        access_token = self.redis_ob.get_dingding_access_token()
        headers = {
            "x-acs-dingtalk-access-token": f"{access_token}"
        }
        return headers

    @def_retry()
    def get_online_last_row(self,
                            table_id: str,
                            operatorId: str,
                            sheets: Optional[str] = 'Sheet1', ):
        """
        查询在线表格中最后一行的数据位置
        """
        url = f"https://api.dingtalk.com/v1.0/doc/workbooks/{table_id}/sheets/{sheets}?operatorId={operatorId}"
        headers = self.init_dingding_headers()
        response = requests.get(url, headers).json()
        last_row = response['lastNonEmptyRow']
        return last_row + 1

    @def_retry()
    def read_dingding_onlne_excel_data(self,
                                       table_id: str,
                                       array_range: str,
                                       operatorId: str,
                                       sheets: Optional[str] = 'Sheet1'):
        """
        获取物流商报价数据
        :return:
        """
        url = f'https://api.dingtalk.com/v1.0/doc/workbooks/{table_id}/sheets/{sheets}/ranges/{array_range}?operatorId={operatorId}'
        headers = self.init_dingding_headers()
        response = requests.get(url, headers).json()
        displayValues = response['displayValues']
        if displayValues:
            return displayValues

    @def_retry()
    def write_dingding_onlne_excel_data(self,
                                        table_id: str,
                                        array_range: str,
                                        operatorId: str,
                                        body: dict,
                                        sheets: Optional[str] = 'Sheet1'
                                        ):
        """
        待发货信息同步写入到物流商现在表格
        :return:
        """
        url = f'https://api.dingtalk.com/v1.0/doc/workbooks/{table_id}/sheets/{sheets}/ranges/{array_range}?operatorId={operatorId}'
        headers = self.init_dingding_headers()
        response = requests.put(url=url, headers=headers, json=body)
        if response.status_code == Status.OK.value:
            logger.info(f"更新完成！")
        return Status.OK.value
