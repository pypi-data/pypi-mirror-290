# _*_ coding: utf-8 _*_
# @Time : 2024/7/31
# @Author : 杨洋
# @Email ： yangyang@doocn.com
# @File : DigiCore
# @Desc : tidb数据库操作工具集合
import random

from loguru import logger
from typing import Optional

from digiCore.common.decorate import def_retry
from digiCore.db.config import TIDB_PORT, TIDB_USER, TIDB_PWD, TIDB_SERVER
from digiCore.db.tidb.init import TiDBConnectionPool
from digiCore.db.tidb.util import list_to_sql_values, create_insert_sql


class TiDBDao():
    def __init__(self,
                 host: Optional[str] = random.choice(TIDB_SERVER),
                 port: Optional[int] = TIDB_PORT,
                 user: Optional[str] = TIDB_USER,
                 passwd: Optional[str] = TIDB_PWD
                 ):
        self.conn_pool = TiDBConnectionPool(host,port,user,passwd)

    @def_retry(msg="Mysql: 查询单条数据失败！")
    def query_one(self, sql: str):
        """
        查询并返回数据库中的一条数据
        :param sql: 查询sql语句
        :return: dict
        """
        with self.conn_pool as cursor:
            cursor.execute(sql)
            data = cursor.fetchone()
            return data

    @def_retry(msg="Mysql: 查询批量数据失败！")
    def query_list(self, sql: str):
        """
        查询并返回数据库中的全部数据
        :param sql: 查询sql语句
        :return: list
        """
        with self.conn_pool as cursor:
            cursor.execute(sql)
            data = cursor.fetchall()
            return data

    @def_retry(msg="Mysql: 批量插入失败！")
    def insert_data(self, db_table: str, field_list: list, data_list: [dict]):
        """
        查询并返回数据库中的一条数据
        :param db_table: 数据库及表名称
        :param data_list: 字段对应的列表套字典数据
        :param field_list: 字段列表
        :param sql: 查询sql语句
        :return:
        """
        if not data_list:
            logger.info(f"{db_table}: 无数据插入！")
            return
        sql_values = list_to_sql_values(field_list, data_list)
        insert_sql = create_insert_sql(db_table, field_list, sql_values)
        with self.conn_pool as cursor:
            cursor.execute(insert_sql)

    @def_retry(msg="Mysql: sql语句commit提交失败,检查sql语句！")
    def commit_sql(self, sql: str):
        """
        提交sql语句
        用于 建表 、删除表使用
        :param sql: sql语句
        :return:
        """
        with self.conn_pool as cursor:
            cursor.execute(sql)

    @def_retry(msg="建表失败！")
    def create_table(self, create_sql: str):
        """
        创建表
        :param create_sql: crate table if not exists ...
        :return:
        """
        with self.conn_pool as cursor:
            sql = create_sql.replace('\n', ' ')
            cursor.execute(sql)

if __name__ == '__main__':

    t = TiDBDao(host='192.168.0.200')
    data = t.query_list('select * from dim_prod.dim_cd_inv_lx_supplier_information_i_manual')
    print(data)