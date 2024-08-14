# -*- coding: utf-8 -*-
# @Time     : 2024/08/05 17:53
# @Author   : 刘云飞
# @Email    : yfliu@doocn.com
# @FileName : crawler_form_attachments.py
import io
import json
import requests
from loguru import logger
from datetime import datetime

from digiCore.common.decorate import def_retry
from digiCore.yida.common import YidaCommon


# 获取表单附件
class YidaCrawlerFromAttachments(YidaCommon):

    @def_retry()
    def get_form_data(
            self,
            form_id: str,
            create_from_time: str = '',
            create_to_time: str = '',
            modified_from_time: str = '',
            modified_to_time: str = '',
            current_page: int = 1,
            page_size: int = 100,
            search_field: dict = None
    ):
        """
        获取钉钉表单的数据。

        参数:
        - form_id: str，表单的ID。
        - create_from_time: str，创建时间的起始时间，默认为空。
        - create_to_time: str，创建时间的结束时间，默认为空。
        - modified_from_time: str，修改时间的起始时间，默认为空。
        - modified_to_time: str，修改时间的结束时间，默认为空。
        - current_page: int，当前页码，默认为1。
        - page_size: int，每页的数据条数，默认为100。
        - search_field: dict，搜索字段，默认为空。

        返回:
        - list，包含表单数据的列表。
        """
        # 构建请求URL
        # 定义钉钉表单实例查询的API URL
        url = 'https://api.dingtalk.com/v1.0/yida/forms/instances/search'
        # 构建请求体
        # 构建查询表单实例的请求体
        body = {
            'appType': self.appType,  # 应用编码
            'systemToken': self.systemToken,  # 应用密钥
            'userId': self.userId,  # 用户id
            'formUuid': form_id,  # 表单
            'createFromTimeGMT': create_from_time,  # 查询创建数据列表的开始时间, 格式：yyyy-MM-dd
            'createToTimeGMT': create_to_time,  # 查询创建数据列表的结束时间, 格式：yyyy-MM-dd
            'modifiedFromTimeGMT': modified_from_time,  # 查询修改数据列表的开始时间, 格式：yyyy-MM-dd
            'modifiedToTimeGMT': modified_to_time,  # 查询修改数据列表的结束时间, 格式：yyyy-MM-dd
            'currentPage': current_page,  # 分页参数，当前页。
            'pageSize': page_size,  # 分页参数，每页显示条数。
        }
        # 如果提供了搜索字段，则添加到请求体中
        # 如果提供了搜索字段，则添加到请求体中
        if search_field:
            body['searchFieldJson'] = f'{search_field}'

        # 初始化总记录数和结果数据列表
        total_count = 1
        result_data = []
        # 循环获取所有页的数据，直到获取完所有记录
        while len(result_data) < total_count:
            # 发送POST请求获取表单实例数据
            response = requests.post(url, headers=self.init_headers(), json=body)
            result = response.json()
            # 更新当前页和总记录数
            current_page = result.get('currentPage')
            total_count = result.get('totalCount')
            # 将当前页的数据添加到结果列表
            result_data.extend(result.get('data'))
            # 记录日志信息
            logger.info('当前页: %s, 表单总条数: %s' % (current_page, total_count))
            # 更新请求体中的页码
            body['currentPage'] += 1

        return result_data

    @def_retry()
    @staticmethod
    def get_form_attachment_information(form_data, attachment_field):
        """
        获取表单附件的存储路径。

        参数:
        - form_data: list，包含表单数据的列表。
        - attachment_field: str，附件字段的名称。

        返回:
        - list，包含附件信息的列表。
        """
        # 初始化附件数据列表
        form_data_list = []
        # 处理每条表单数据，提取附件信息
        for form in form_data:
            # 创建时间的datetime对象
            created_time_ob = datetime.strptime(form.get('createdTimeGMT'), '%Y-%m-%dT%H:%MZ')
            # 格式化日期字符串
            dt = created_time_ob.strftime('%Y%m%d')
            created_time = created_time_ob.strftime('%Y-%m-%d %H:%M')

            # 提取表单数据中的序列号、创建人信息、表单数据和附件信息
            serial_no = form.get('serialNo', '0')  # 序列号
            originator = form.get('originator', 'None')  # 创建人信息
            from_data = form.get('formData')  # 表单数据
            creator = originator.get('userName')['nameInChinese']  # 创建人姓名
            attachments = json.loads(from_data.get(attachment_field))  # 附件信息

            # 遍历附件列表，构建每份附件的数据字典，并添加到附件数据列表
            for attachment in attachments:
                download_path = attachment.get('downloadUrl')
                attachment_name = attachment.get('name')
                attachment_data = {
                    'dt': dt,
                    'serial_number': serial_no,
                    'creator': creator,
                    'created_time': created_time,
                    'file_name': attachment_name,
                    'download_path': download_path,
                }
                form_data_list.append(attachment_data)
        logger.info('获取到 %s 个附件!' % len(form_data_list))

        # 返回附件数据列表
        return form_data_list

    @def_retry()
    def get_attachment_download_url(self, download_path):
        """
        获取附件的下载URL。

        参数:
        - download_path: str，附件的临时下载路径。

        返回:
        - str，附件的下载URL。
        """

        # 定义附件下载URL的API URL
        download_url = fr'https://api.dingtalk.com/v1.0/yida/apps/temporaryUrls/{self.appType}'
        # 构建请求体
        body = {
            'systemToken': self.systemToken,
            'userId': self.userId,
            'language': 'zh_CN',
            'fileUrl': download_path,
            'timeout': 3600
        }
        # 发送GET请求获取附件的下载URL
        response = requests.get(download_url, headers=self.init_headers(), params=body)
        # 返回附件的下载URL
        result = response.json() if response.status_code == 200 else {}
        return result.get('result')

    @def_retry()
    def get_attachment_io(self, url):
        """
        获取附件的IO流。

        :param url: 附件的下载URL。
        :return: 附件的IO流，如果下载失败则返回空字节串。
        """
        # 发送GET请求下载附件
        response = requests.get(url, headers=self.init_headers())
        # 返回附件的IO流
        return io.BytesIO(response.content) if response.status_code == 200 else io.BytesIO(b'')
