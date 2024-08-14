# _*_ coding: utf-8 _*_
# @Time : 2024-08-05
# @Author : 李仕春
# @Email ： scli@doocn.com
# @File : DigiCore
# @Desc :
from io import BytesIO
from urllib import parse

import requests
from loguru import logger

from digiCore.common.decorate import def_retry
from digiCore.confluence.config import confluence_url, confluence_headers

class DownloadPath:
    """
    获取title文件名称下的文件下载地址
    """

    @def_retry()
    def get_attachment_url(self, title):
        """
        获取采集附件的url
        """
        url = f"{confluence_url}/rest/api/content?title={title}"
        response = requests.request("GET", url, headers=confluence_headers).json()
        results = response.get("results")
        page_id = results[0].get("id")
        attachment_url = f"{confluence_url}/rest/api/content/{page_id}/child/attachment"
        return attachment_url

    @def_retry()
    def get_all_attachment_list(self, attachment_url, title):
        """
        获取Doocn盘货表上传资源ODS所有数据
        """
        response = requests.request("GET", attachment_url, headers=confluence_headers).json()

        attachment_list = response.get("results")

        logger.info(f'获取数据表下载地址列表成功， {title} 表总数量为：{len(attachment_list)} 张')
        return attachment_list

    @def_retry()
    def get_file_data_list(self, title):
        """
        获取文件列表信息
        :return:
        """
        attachment_url = self.get_attachment_url(title)
        attachment_list = self.get_all_attachment_list(attachment_url, title)
        return attachment_list

    @def_retry()
    def read_confluence_data(self, title):
        """
        获取指定位置confluence上传的文件数据
        """
        file_path_list = []
        attachment_list = self.get_file_data_list(title)
        for attachment_data in attachment_list:
            file_path_dict = {}
            _links = attachment_data.get("_links")
            download = _links.get("download")
            download_url = confluence_url + parse.unquote(download)
            response = requests.get(download_url, headers=confluence_headers)
            assert response.status_code == 200
            file_path = BytesIO(response.content)
            file_path_dict['file_path'] = file_path
            file_path_dict['file_name'] = attachment_data.get('title')
            file_path_list.append(file_path_dict)
        return file_path_list