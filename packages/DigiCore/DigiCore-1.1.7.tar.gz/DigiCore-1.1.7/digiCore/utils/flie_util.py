# _*_ coding: utf-8 _*_
# @Time : 2024/7/31
# @Author : 杨洋
# @Email ： yangyang@doocn.com
# @File : DigiCore
# @Desc :
from __future__ import annotations

import os
import chardet
import pandas as pd
import pdfplumber
from loguru import logger
from io import BytesIO
from typing import Optional, Any


class PdfReader:
    """
    PdfReader类用于处理PDF文件的读取和数据提取。

    该类的构造函数接受文件的二进制流或文件路径作为输入，并可选地接受文件名。
    如果提供了文件路径，则会自动提取文件名。

    参数:
    - io: 文件的二进制流（BytesIO）或文件路径（str）
    - file_name: 可选参数，文件名（str）

    如果提供了BytesIO对象但未提供文件名，将抛出异常。
    """
    def __init__(self, io: str | BytesIO, file_name: str = None):
        self.io = io
        self.filename = file_name
        # 如果提供了BytesIO对象但未提供文件名，抛出异常
        if isinstance(io, BytesIO) and self.filename is None:
            raise Exception('缺少必要参数值！ file_name')
        # 如果提供了文件路径，则提取文件名
        if isinstance(io, str) and self.filename is None:
            self.filename = os.path.basename(io)

    def extract_pages_data(self):
        """
        从PDF文件中提取每页的文本数据。

        使用pdfplumber库打开PDF文件，并迭代访问每页的内容。
        提取每页的页码和文本内容，并将其存储在一个列表中返回。

        返回:
        包含每页数据的列表，每个元素包含页码和提取的文本。
        """
        with pdfplumber.open(self.io) as pdf:
            p = 1
            pages_data = []
            for page in pdf.pages:
                # 提取每页的文本并存储
                data = {
                    'page': p,
                    'text': page.extract_text()
                }
                pages_data.append(data)
                p += 1

            return pages_data


# 用于读取和解析Excel文件的类
# 支持xlsx、xls和csv格式
class ExcelReader:
    """
    提取数据
    """
    def __init__(self, io: str | BytesIO, file_name: str = None):
        """
        初始化方法

        :param io: 包含Excel数据的字符串路径或BytesIO对象
        :param file_name: Excel文件的名称，可选，用于确定文件类型
        """
        self.io = io
        self.file_name = file_name
        if isinstance(io, BytesIO) and self.file_name is None:
            raise Exception('缺少必要参数值！ file_name')
        if isinstance(io, str) and self.file_name is None:
            self.file_name = io

        self.file_type = os.path.splitext(file_name)[-1]

    @property
    def sheet_names(self) -> list:
        """
        获取Excel中的所有工作表名称

        :return: 工作表名称列表
        """
        ef = pd.ExcelFile(path_or_buffer=self.io)

        return list(ef.sheet_names)

    def read_csv(
            self,
            dtype: str = None,
            rename_columns: Optional[dict] = None,
            skiprows: Optional[Any] = None,
            skipfooter: int = 0,
            engine: str = None
    ) -> pd.DataFrame:
        """
        从BytesIO对象中读取CSV文件并返回DataFrame

        :param dtype: 数据类型映射
        :param rename_columns: 列重命名的字典
        :param skiprows: 跳过的行数
        :param skipfooter: 跳过的末尾行数
        :param engine: 读取引擎
        :return: 读取后的DataFrame
        """
        """
        读取 csv 文件
        处理过程:
            1: 获取csv数据格式
            2: pd读取csv数据, 去掉前后不要的行
            3: 重命名表头
        """
        # 获取io数据
        io_data = self.io.getvalue()
        # 获取数据编码格式
        encod_data = chardet.detect(io_data)
        # 打开数据
        df = pd.read_csv(self.io, dtype=dtype, encoding=encod_data['encoding'], skiprows=skiprows,
                         skipfooter=skipfooter, engine=engine)
        if rename_columns is not None:
            df = df.rename(columns=rename_columns)

        return df

    def read_excel(
            self,
            sheet_name: str | int | None = 0,
            dtype: str = None,
            rename_columns: Optional[dict] = None,
            skiprows: Optional[Any] = None,
            skipfooter: int = 0,
            engine: str = None
    ) -> pd.DataFrame:
        """
        从BytesIO对象中读取Excel文件的指定工作表并返回DataFrame

        :param sheet_name: 工作表名称或索引
        :param dtype: 数据类型映射
        :param rename_columns: 列重命名的字典
        :param skiprows: 跳过的行数
        :param skipfooter: 跳过的末尾行数
        :param engine: 读取引擎
        :return: 读取后的DataFrame
        """
        """
        读取 xlsx 文件
        处理过程:
            1: pd读取xlsx数据, 去掉前后不要的行
            2: 重命名表头
        """
        # 打开数据
        df = pd.read_excel(self.io, sheet_name=sheet_name, dtype=dtype, skiprows=skiprows, skipfooter=skipfooter,
                           engine=engine)
        if rename_columns is not None:
            df = df.rename(columns=rename_columns)

        return df

    def get_dataframe(
            self,
            sheet_name: str | int | None = 0,
            dtype=None,
            rename_columns: Optional[dict] = None,
            skiprows: Optional[Any] = None,
            skipfooter: int = 0
    ) -> pd.DataFrame:
        """
        根据文件类型自动选择读取CSV或Excel，并返回DataFrame

        :param sheet_name: 工作表名称或索引
        :param dtype: 数据类型映射
        :param rename_columns: 列重命名的字典
        :param skiprows: 跳过的行数
        :param skipfooter: 跳过的末尾行数
        :return: 读取后的DataFrame
        """
        df = pd.DataFrame()

        kw_params = dict(dtype=dtype, sheet_name=sheet_name, rename_columns=rename_columns, skiprows=skiprows,
                         skipfooter=skipfooter)

        try:
            if self.file_type == '.xlsx':
                df = self.read_excel(**kw_params)
            elif self.file_type == '.xls':
                df = self.read_excel(**kw_params, engine='xlrd')
            elif self.file_type == '.csv':
                del kw_params['sheet_name']
                df = self.read_csv(**kw_params, engine='python')
        except Exception as e:
            logger.error(f'error file:{e.__traceback__.tb_frame.f_globals["__file__"]}')
            logger.error(f'error line:{e.__traceback__.tb_lineno}')
            logger.error(f'error message:{e.args}')
        finally:
            return df


def load_excel_data(file_type: str, file_path: str, sheet=None, skiprows: int = 0):
    """
    :param file_type: 文件类型 ：
    :param file_path: 文件路径
    :param sheet: 子表名称
    :param
    :return: 数据列表
    """
    with open(file_path, 'rb') as f:
        data = chardet.detect(f.read())
        encoding = data['encoding']
    try:
        if file_type == 'excel':
            df = pd.read_excel(file_path, sheet, skiprows=skiprows)
        elif file_type == 'csv':
            df = pd.read_csv(file_path, encoding=encoding, skiprows=skiprows)
        else:
            logger.error(f"{file_type} 文件类型错误。参数为：excel、csv")
            return
    except Exception as e:
        logger.error(f'error file:{e.__traceback__.tb_frame.f_globals["__file__"]}')
        logger.error(f'error line:{e.__traceback__.tb_lineno}')
        logger.error(f'error message:{e.args}')
        return
    return df
