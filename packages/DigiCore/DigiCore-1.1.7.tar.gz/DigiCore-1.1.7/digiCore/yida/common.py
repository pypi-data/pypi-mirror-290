# _*_ coding: utf-8 _*_
# @Time : 2024/7/31
# @Author : 杨洋
# @Email ： yangyang@doocn.com
# @File : DigiCore
# @Desc :
import json

import requests
from loguru import logger

from digiCore.db.redis.core import RedisDao
from digiCore.yida.config import YIDA_FORMS_URL, USERID, DEFINITIONS_URL
from typing import Optional


class YidaCommon:

    def __init__(self,
                 appType: str,
                 systemToken: str,
                 userId: Optional[str] = USERID,
                 ):
        self.appType = appType
        self.systemToken = systemToken
        self.userId = userId
        self.redis = RedisDao()

    def init_headers(self):
        """
        初始化headers
        """
        access_token = self.redis.get_dingding_access_token()
        headers = {
            "x-acs-dingtalk-access-token": access_token
        }
        return headers

    def query_forms(self):
        """
        查询应用下的所有表单信息
        {
				"formType":"process",
				"creator":"16810885426326527",
				"formUuid":"FORM-JH9660C1M1HDZMOH9TVVB4KH1R1C2YNZ09KLLN",
				"gmtCreate":"2023-08-31T10:38Z",
				"title":{
					"zhCN":"调整交期表",
					"enUS":"UnNamed Process Form"
				}
			}
        """
        url = f'{YIDA_FORMS_URL}?appType={self.appType}&systemToken={self.systemToken}&userId={self.userId}'
        response = requests.get(url=url,
                                headers=self.init_headers()).json()
        result = response.get('result', {})
        data_list = result.get('data', [])
        forms_json = {}
        for data in data_list:
            formUuid = data.get('formUuid')
            title = data.get('title', {})
            zhCN = title.get('zhCN')
            forms_json[zhCN] = formUuid
        return forms_json or {}

    def get_form_uuid(self, table_name):
        """
        获取表名称对应的form_uuid
        """
        forms_json = self.query_forms()
        form_uuid = forms_json.get(table_name)
        return form_uuid or None

    def get_field_id_json(self, form_uuid, table_type):
        """
        获取表单中的字段与宜搭字段的映射
        {
			"label":"{\"en_US\":\"NumberField\",\"pureEn_US\":\"NumberField\",\"type\":\"JSExpression\",\"zh_CN\":\"运费赔付金额\"}",
			"componentName":"NumberField",
			"parentId":"formContainer_lv6dy3hv",
			"fieldId":"numberField_lv6dyp1k"
		}
        """
        url = f'{DEFINITIONS_URL}?appType={self.appType}&systemToken={self.systemToken}&formUuid={form_uuid}&userId={self.userId}'
        response = requests.get(url=url, headers=self.init_headers()).json()
        result = response.get('result', [])
        if table_type == 'form':
            field_id_json = self.get_form_json(result)
            return field_id_json
        elif table_type == 'sub_form':
            form_json, sub_form_json = self.get_sub_form_json(result)
            field_id = self.get_sub_form_field_id(result)
            return form_json, sub_form_json,field_id
        else:
            logger.error('表单类型传递错误！使用 form / sub_form')
            return {}

    def get_sub_form_field_id(self, result):
        """
        获取自表单的字段名称及字段id
        """
        for data in result:
            componentName = data.get('componentName')
            if componentName != "TableField":
                continue
            field_id = data.get('fieldId')
            return field_id

    def get_form_json(self, result):
        """
        获取表单字段映射
        """
        field_id_json = {}
        for data in result:
            label = data.get('label')
            zh_CN = label.get('zh_CN')
            if not zh_CN:
                continue
            fieldId = data.get('fieldId')
            field_id_json[fieldId] = zh_CN
        return field_id_json or {}

    def get_sub_form_json(self, result):
        """
        获取子表单字段映射
        """

        form_json = self.get_form_json(result)
        for data in result:
            children = data.get('children')
            if not children:
                continue
            sub_form_json = self.get_form_json(children)
            return form_json, sub_form_json
