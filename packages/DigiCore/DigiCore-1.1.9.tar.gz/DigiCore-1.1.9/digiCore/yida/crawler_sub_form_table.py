# _*_ coding: utf-8 _*_
# @Time : 2024/7/31
# @Author : 杨洋
# @Email ： yangyang@doocn.com
# @File : DigiCore
# @Desc : 获取子表单数据
from typing import Optional

import requests
from loguru import logger

from digiCore.common.decorate import def_retry
from digiCore.yida.common import YidaCommon
from digiCore.yida.config import USERID, SUB_FORM_TABLE_URL


class CrawlerSubFormTable(YidaCommon):

    def __init__(self, appType,
                 systemToken,
                 table_name,
                 userId: Optional[str] = USERID):
        super().__init__(
            appType=appType,
            systemToken=systemToken,
            userId=userId
        )
        self.table_name = table_name
        self.table_type = 'sub_form'

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
        response = requests.post(url=SUB_FORM_TABLE_URL,
                                 headers=self.init_headers(),
                                 json=body).json()
        return response

    @def_retry()
    def get_form_data_list(self, form_uuid, form_json, sub_form_json, field_id):

        pageNumber = 1
        form_data_list = []
        while True:
            response = self.yida_post(form_uuid, pageNumber)
            totalCount = response.get('totalCount')
            format_data_list = self.format_data(response, form_json, sub_form_json,field_id)
            form_data_list += format_data_list
            if len(form_data_list) >= totalCount:
                break
            pageNumber += 1
        return form_data_list

    def format_data(self, response, form_json, sub_form_json,field_id):
        """
        格式化数据
        """
        format_data_list = []
        data_list = response.get('data', [])
        for data in data_list:
            formData = data.get('formData')
            if not formData:
                continue
            form_data = self.get_form_data(formData, form_json)

            sub_form_field = form_json.get(field_id)
            sub_form_data_list = self.get_sub_form_data(form_data, sub_form_json, sub_form_field)
            form_data[sub_form_field] = sub_form_data_list
            format_data_list.append(form_data)
        return format_data_list

    @def_retry()
    def get_form_data(self, formData, form_json):
        """
        获取子表单外的数据
        """
        form_data = {form_json.get(field_id.replace('_value', '')): value for field_id, value in formData.items() if
                     field_id in form_json.keys()}
        return form_data

    @def_retry()
    def get_sub_form_data(self, form_data, sub_form_json, sub_form_field):
        """
        获取子表单数据
        """
        table_field_data_list = form_data.get(sub_form_field)
        sub_form_data_list = []
        for table_field_data in table_field_data_list:
            sub_form_data = {sub_form_json.get(field_id.replace('_value', '')): value for field_id, value in
                             table_field_data.items()}
            sub_form_data_list.append(sub_form_data)
        return sub_form_data_list

    @def_retry()
    def get_sub_form_data_list(self):
        """
        获取子表单数据
        """
        # 获取表单form_uuid
        form_uuid = self.get_form_uuid(self.table_name)
        if not form_uuid:
            logger.error(f"{self.table_name} 表单名称有误，无法获取到form_uuid！")
            return

        # 获取字段映射关系
        form_json, sub_form_json, field_id = self.get_field_id_json(form_uuid, self.table_type)
        # 获取表单数据
        sub_form_data_list = self.get_form_data_list(form_uuid, form_json, sub_form_json, field_id)
        return sub_form_data_list


if __name__ == '__main__':
    y = CrawlerSubFormTable(
        appType='APP_MNJQQV8Q5IOB3STDZEF5',
        systemToken='CA966X91P18BX3HL8TWLGAAF0FIG22VB9GCILO3',
        table_name='BD-预算提报',
        userId=USERID
    )
    y.get_sub_form_data_list()
