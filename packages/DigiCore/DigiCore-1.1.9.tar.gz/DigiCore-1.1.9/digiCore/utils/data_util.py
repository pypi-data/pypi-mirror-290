# _*_ coding: utf-8 _*_
# @Time : 2024-08-05
# @Author : 李仕春
# @Email ： scli@doocn.com
# @File : DigiCore
# @Desc :
import json
import re
from collections import defaultdict
from typing import List, Dict, Any, Optional

def grouped_vals_data(dict_data: List[Dict[str, Any]], keys: List[str], is_order: bool = True) -> List[
    List[Dict[str, Any]]]:
    """
    将列表字典用多个键，值相同进行分类
    :param dict_data: 字典列表数据
    :param keys: 键值列表
    :return: 分组后的字典列表
    """
    freq_dict = defaultdict(list)
    for item in dict_data:
        if is_order:
            # 使用元组作为分组键，保持键值顺序
            group_key = tuple(item[key] for key in keys)
        else:
            # 使用 frozenset 作为分组键，确保键值顺序无关
            group_key = frozenset(item[key] for key in keys)

        freq_dict[group_key].append(item)
    grouped_vals = list(freq_dict.values())
    return grouped_vals


def original_to_format_key(order_data_list: list, table_dict: dict):
    """
    将读取出来的原始数据的key更换为格式化之后的key，并去多余key。
    :return:
    """
    new_data_list = []
    for data in order_data_list:
        # 找出原始数据中不存在的字段
        diff_keys = set(table_dict.keys()) - set(data.keys())
        new_item = {table_dict.get(k, k): str(v) for k, v in
                    data.items()
                    if k in table_dict}
        # 对不存在的字段进行赋值
        for key in diff_keys:
            if key == "dt":
                continue
            new_item[table_dict[key]] = "None"
        new_data_list.append(new_item)
    return new_data_list


def json_to_dict(invalid_json_string):
    """
    将类似 '{fpurposeid:SFKYT02_SYS}' 的字符串转换为有效的 JSON 格式。
    :param invalid_json_string: 无效的 JSON 格式字符串
    :return: 预处理后的有效 JSON 字符串
    """
    # 使用正则表达式将单引号替换为双引号，并确保键和值都被正确包围
    valid_json_string = re.sub(r"(?<=\{|,)\s*([a-zA-Z0-9_]+)\s*:", r'"\1":', invalid_json_string)
    valid_json_string = re.sub(r":\s*([a-zA-Z0-9_]+)\s*(?=,|\})", r':"\1"', valid_json_string)
    try:
        # 尝试将 JSON 字符串加载为字典
        dict_obj = json.loads(valid_json_string)
        return dict_obj
    except json.JSONDecodeError:
        # 如果 JSON 字符串无效，返回 None
        return None

def data_format(data_list: list, key_list: list):
    """
    将读取到的-数据包-文件数据转化为列表套字典格式
    data_list 数据包 格式列表套列表
    key_list 字典中作为键的列表
    """
    data_dict_list = []
    for one in data_list:
        data = dict(zip(key_list, one))
        data_dict_list.append(data)
    return data_dict_list


def mark_uid(data_package: Optional[List[Dict]], field_list: Optional[List[str]] = None, uid_key_name: str = 'uid'):
    """
    为数据包中的每个数据项添加一个唯一的标识字段'uid'。
    如果提供了field_list，则唯一标识基于field_list中的字段值生成；
    如果未提供field_list，则基于数据项的所有字段值生成。
    """
    # 使用字典存储每个唯一字符串索引对应的计数器
    index_counter = defaultdict(int)
    # 用于存储已经处理过的唯一标识字符串
    unique_key = set()
    # 创建一个新列表，用于存储处理后的数据项
    new_list = []

    for data in data_package:
        # 选择用于生成唯一标识的字段列表
        fields = field_list or list(data.keys())
        # 为当前数据项生成唯一的字符串索引
        try:
            unique_str = '_uid//:{0}'.format(','.join(str(data[field]) for field in fields))
        except KeyError as e:
            raise ValueError(f"Field {e} not found in record") from None
        # 检查当前的唯一字符串索引是否已经存在
        if unique_str in unique_key:
            # 如果存在，则获取当前计数器并加1，然后更新数据项的'unique_index'字段
            index_counter[unique_str] += 1
            data[uid_key_name] = index_counter[unique_str]
        else:
            # 如果不存在，则设置计数器为0，并添加到集合中，同时更新数据项的'unique_index'字段
            index_counter[unique_str] = 0
            data[uid_key_name] = 0
            unique_key.add(unique_str)
        # 将处理后的数据项添加到新列表中
        new_list.append(data)

    # 返回处理后的新数据包
    return new_list


def split_list(big_list, chunk_size):
    """
    将一个大的列表拆分为多个小的列表。

    参数:
    big_list (list): 要拆分的列表。
    chunk_size (int): 每个小列表的最大长度。

    返回:
    list of lists: 包含拆分后的小列表的列表。
    """
    return [big_list[i:i + chunk_size] for i in range(0, len(big_list), chunk_size)]
