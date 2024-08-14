# -*- coding: utf-8 -*-
# @Time     : 2024/08/06 10:05
# @Author   : 刘云飞
# @Email    : yfliu@doocn.com
# @FileName : crawler_http.py
from __future__ import annotations

import traceback
from loguru import logger
from requests import Session


# 群晖文件服务器API请求辅助类
class RequestHelper:
    """
    请求辅助类，用于处理与特定主机的API交互。
    初始化时，会设置登录参数，并准备一个基础URL用于后续请求。
    """

    def __init__(self, host: str, port: int | str, username: str, password: str):
        # 初始化成员变量
        self.host = host
        self.port = port
        self.username = username
        self.password = password

        # 构建基础URL，用于后续的API请求
        self.synology_base_url = f'http://{self.host}:{self.port}'

        # 初始化登录状态和Token
        self.login_status = False
        self.synology_token = None

        # API会话对象，用于管理与API的交互
        self._synology_api_session = None

    @property
    def synology_api_session(self) -> Session:
        """
        管理与API的会话。
        如果会话对象不存在，则创建一个新的会话，并尝试登录。
        返回API会话对象。
        """
        login_params = {
            'api': 'SYNO.API.Auth',
            'version': '7',
            'method': 'login',
            'account': self.username,
            'passwd': self.password,
            'session': 'FileStation',
            'format': 'cookie',
            'enable_syno_token': 'yes'
        }

        if self._synology_api_session is None:
            # 初始化一个新的会话对象
            self._synology_api_session = Session()
            self._synology_api_session.headers.update({'Content-Type': 'application/x-www-form-urlencoded'})
            # 设置最大重试次数
            maximum_retry = 5
            # 构建登录URL
            login_url = f'{self.synology_base_url}/webapi/auth.cgi'
            # 循环尝试登录，直到成功或达到最大重试次数
            while not self.login_status and maximum_retry > 0:
                try:
                    # 发送登录请求
                    response = self._synology_api_session.get(login_url, params=login_params)
                    # 解析登录结果
                    login_result = response.json()
                    self.login_status = login_result['success']
                    if self.login_status:
                        # 登录成功，记录Token
                        login_data = login_result['data']
                        self.synology_token = login_data['synotoken']
                        self._synology_api_session.headers.update({'X-SYNO-TOKEN': self.synology_token})
                        logger.success(f'登录成功[{self.username}]')
                    else:
                        # 登录失败，记录错误
                        logger.error(f'登录失败，错误代码：{login_result["error"]["code"]}')
                except Exception:
                    # 异常处理，记录错误并减少重试次数
                    self.login_status = False
                    maximum_retry -= 1
                    logger.error(f'登录失败，剩余尝试次数：{maximum_retry}\n错误信息: \n{traceback.format_exc()}')
            if not self.login_status and maximum_retry == 0:
                # 达到最大重试次数仍未登录成功，记录错误
                logger.error('登录失败，已达到最大重试次数')
                return self._synology_api_session

        # 返回API会话对象
        return self._synology_api_session
