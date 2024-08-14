# _*_ coding: utf-8 _*_
# @Time : 2024/8/2
# @Author : 杨洋
# @Email ： yangyang@doocn.com
# @File : DigiCore
# @Desc :
from enum import Enum,EnumMeta
from typing import Optional
from pydantic import BaseModel
class Status(Enum):
    OK = 200
    CREATED = 201
    ACCEPTED = 202
    NO_CONTENT = 204
    BAD_REQUEST = 400
    UNAUTHORIZED = 401
    FORBIDDEN = 403
    NOT_FOUND = 404
    METHOD_NOT_ALLOWED = 405
    CONFLICT = 409
    INTERNAL_SERVER_ERROR = 500
    NOT_IMPLEMENTED = 501
    BAD_GATEWAY = 502
    SERVICE_UNAVAILABLE = 503

    def describe(self):
        descriptions = {
            200: "正常：请求已成功。",
            201: "已创建：请求已完成并导致一个新的资源被创建。",
            202: "已接受：请求已接受用于处理，但处理尚未完成。",
            204: "无内容：服务器成功处理了请求，但没有返回任何内容。",
            400: "错误请求：由于语法错误，服务器无法理解请求。",
            401: "未授权：客户端必须进行身份验证才能获得请求的响应。",
            403: "禁止：客户端没有访问内容的权限。",
            404: "未找到：服务器找不到请求的资源。",
            405: "方法不允许：请求方法被服务器识别但已禁用，无法使用。",
            409: "冲突：请求无法完成，因为它与资源的当前状态存在冲突。",
            500: "内部服务器错误：服务器遇到错误，无法完成请求。",
            501: "未实现：请求的方法服务器不支持，无法处理。",
            502: "错误网关：服务器作为网关或代理，从上游服务器收到无效响应。",
            503: "服务不可用：服务器尚未准备好处理请求。",
        }
        return descriptions.get(self.value, "未知状态码")


# ------------------------------ POST接口传参声明 --------------------------------
class PostItems(BaseModel):
    """
    传参
    """
    service_name: str
    subserver: str
    operation_type: Optional[str] = 'sync'  # sync:同步，async:异步， 默认同步
    run_sign: Optional[str] = 'start'  # start:启动，stop:停止， 默认启动
    extra_params: Optional[dict] = {}  # 额外传参


class ItemEnum(EnumMeta):
    OPERATION_ASYNC = "async"  # 异步操作
    OPERATION_SYNC = "sync"  # 同步操作
    RUN_START = "start"  # 开始
    RUN_STOP = "stop"  # 停止


if __name__ == '__main__':
    print(Status.describe(Status.BAD_REQUEST))
