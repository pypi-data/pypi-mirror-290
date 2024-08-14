# -*- coding: utf-8 -*-
# @Time    : 2023/09/06 10:37
# @Author  : 刘云飞
# @FileName: tool_smba.py
# @Email   ：yfliu@doocm.com
import os
import traceback
from smb.SMBConnection import SMBConnection
from smb.smb_structs import OperationFailure
from loguru import logger
from digiCore.common.decorate import def_retry


class SMBClient(object):
    def __init__(self, host, username, password):
        """
        SMB连接服务
        :param host:
        :param username:
        :param password:
        """
        self.host = host
        self.username = username
        self.password = password
        self.conn = None
        self.status = False
        self.connection()

    def __enter__(self):
        # 建立SMB连接
        self.conn = None
        self.connection()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        # 关闭SMB连接
        self.close()

    def connection(self):
        try:
            self.conn = SMBConnection(self.username, self.password, '', '', use_ntlm_v2=True)
            self.conn.connect(self.host, 445, timeout=90)
            self.status = self.conn.auth_result
            if self.status:
                logger.success(f"SMB服务器连接成功:[{self.host}]")
            else:
                logger.error(f'smb服务器连接失败！status: {self.status}')
        except Exception:
            self.conn.close()
            logger.error('SMB服务器连接失败！')
            print(traceback.format_exc())

    def close(self):
        # 关闭SMB连接
        if self.conn:
            self.conn.close()
            self.conn = None

    def listshares(self):
        """
        列出smb服务器下的所有共享目录
        """
        share_directory = list()
        share_list = self.conn.listShares()
        for s in share_list:
            share_directory.append(s.name)
        return share_directory

    def listdir(self, service_name, dir_path=""):
        """
        列出文件夹内所有文件名
        :param service_name: 服务名(smb中的文件夹名, 一级目录)
        :param dir_path: 二级目录及以下的文件目录(不传返回所有)
        :return:
        """
        filenames = list()
        try:
            for el in self.conn.listPath(service_name, dir_path):
                if el.filename[0] != '.':  # （会返回一些.的文件，需要过滤）
                    filenames.append(el.filename)
        except OperationFailure as e:
            logger.warning(e.message)
        return filenames

    def last_updatetime(self, service_name, file_path):
        """
        返回samba server上的文件更新时间(时间戳), 如果出现OperationFailure说明无此文件, 返回0
        :param service_name:
        :param file_path:
        :return:
        """
        try:
            sharedfile_obj = self.conn.getAttributes(service_name, file_path)
            return sharedfile_obj.last_write_time
        except OperationFailure:
            return 0

    def create_dir(self, service_name, dir_path):
        """
        创建文件夹
        :param service_name:
        :param dir_path:
        :return:
        """
        try:
            self.conn.createDirectory(service_name, dir_path)
        except OperationFailure as e:
            logger.error(e.message)

    def download(self, service_name, filepath, localpath):
        """
        下载文件
        :param service_name:服务名（smb中的文件夹名）
        :param filepath: 服务器上的文件路径
        :param localpath: 下载到本地的文件路径
        :return:
        """
        fi = open(localpath, 'wb')
        self.conn.retrieveFile(service_name, filepath, fi)
        fi.close()

    def upload(self, service_name, filepath, localpath):
        """
        上传文件
        :param service_name:服务名（smb中的文件夹名）
        :param filepath: 服务器上的文件路径
        :param localpath: 本地的文件路径
        :return:
        """
        fi = open(localpath, 'rb')
        self.conn.storeFile(service_name, filepath, fi)  # 第二个参数path包含文件全路径
        fi.close()

    def delete(self, service_name, filepath):
        """
        删除文件
        :param service_name:服务名（smb中的文件夹名）
        :param filepath: 服务器上的文件路径
        :return:
        """
        self.conn.deleteFiles(service_name, filepath)

    @def_retry(msg=f"共享盘: 下载文件失败！")
    def download_synology(self, server, server_path, local_path):
        """
        上传文件到共享盘
        server: 共享盘名称
        server_path：下载文件文件路径
        local_path：下载后文件存放路径
        :return:
        """
        # smb = SMBClient(**smb_root)
        if self.last_updatetime(server, os.path.dirname(server_path)) == 0:
            self.create_dir(server, os.path.dirname(server_path))
        self.download(server, server_path, local_path)
        logger.success(f'下载共享盘文件成功! [{server_path}]')

    @def_retry(msg=f"共享盘: 上传文件失败！")
    def upload_synology(self, server, server_path, local_path):
        """
        上传文件到共享盘
        :return:
        """
        # smb = SMBClient(**smb_root)
        if self.last_updatetime(server, os.path.dirname(server_path)) == 0:
            self.create_dir(server, os.path.dirname(server_path))
        self.upload(server, server_path, local_path)
        logger.success(f'上传共享盘成功! [{server_path}]')
