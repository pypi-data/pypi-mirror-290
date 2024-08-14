# _*_ coding: utf-8 _*_
# @Time : 2024/7/31
# @Author : 杨洋
# @Email ： yangyang@doocn.com
# @File : DigiCore
# @Desc : 获取表单数据
import json

import requests
from loguru import logger

from digiCore.common.decorate import def_retry
from digiCore.yida.common import YidaCommon
from digiCore.yida.config import FORM_TABLE_URL, USERID
from typing import Optional


class YidaCrawlerFromTable(YidaCommon):

    def __init__(self, appType, systemToken, table_name, userId: Optional[str] = USERID):
        super().__init__(
            appType=appType,
            systemToken=systemToken,
            userId=userId
        )
        self.table_name = table_name
        self.table_type = 'form'

    @def_retry()
    def yida_post(self, form_uuid, pageNumber):
        """
        获取表单数据
        """

        body = {
            "systemToken": self.systemToken,
            "formUuid": form_uuid,
            "userId": self.userId,
            "appType": self.appType,
            "pageNumber": pageNumber,
            "pageSize": 100
        }
        response = requests.post(url=FORM_TABLE_URL,
                                 headers=self.init_headers(),
                                 json=body).json()
        return response

    @def_retry()
    def format_data(self, response, field_id_json):
        """
        解析数据
        """
        data_list = response.get('data')
        format_data_list = []
        for data in data_list:
            formData = data.get('formData')
            if not formData:
                continue
            data = {field_id_json.get(field_id.replace('_value', '')): value for field_id, value in formData.items()}

            format_data_list.append(data)
        return format_data_list

    @def_retry()
    def get_form_data_list(self):

        # 获取表单form_uuid
        form_uuid = self.get_form_uuid(self.table_name)
        if not form_uuid:
            logger.error(f"{self.table_name} 表单名称有误，无法获取到form_uuid！")
            return

        # 获取字段映射关系
        field_id_json = self.get_field_id_json(form_uuid, self.table_type)

        # 获取表单数据
        pageNumber = 1
        form_data_list = []
        while True:
            response = self.yida_post(form_uuid, pageNumber)
            format_data_list = self.format_data(response, field_id_json)
            form_data_list += format_data_list
            if not format_data_list:
                break
            pageNumber += 1
        return form_data_list


if __name__ == '__main__':
    y = YidaCrawlerFromTable(appType='APP_VWP5WMVB2BLM0IP7IXDY',
                             systemToken='7C766871KQABVU4770F6ZCMOZQE43XXSFGFIL92',
                             table_name='物流关税数据填报')
    y.get_form_data_list()
