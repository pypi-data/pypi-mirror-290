# _*_ coding: utf-8 _*_
# @Time : 2024/7/30
# @Author : 杨洋
# @Email ： yangyang@doocn.com
# @File : DigiCore
# @Desc : 数据库链接使用配置

# tidb数据库链接地址
TIDB_SERVER = [
    '192.168.0.200',
    '192.168.0.201',
    '192.168.0.202',
    '192.168.0.203',
    '192.168.0.204'
]

TIDB_PORT = 4000

TIDB_USER = 'root'

TIDB_PWD = 'DoocnProTidb200.'

# reids链接地址
REDIS_SERVER = '192.168.0.201'

REDIS_PORT = 16379

REDIS_PWD = 'DoocnProRedis201.'

# MongoDB链接地址
MONGODB_URL = "mongodb://root:DoocnProMongoDB201.@192.168.0.201:57017/"

# KAFKA链接地址

KAFKA_BROKERS = [
    '192.168.0.200:9092',
    '192.168.0.201:9092',
    '192.168.0.202:9092'
]

# reids 通用组件的Key
LINGXING_API_ACCESS_TOKEN = "common-lingxing-access-token:common:token"
LINGXING_CRSWLER_ACCESS_TOKEN = "common-lingxing-access-token:common:auth_tokens"
DELIVERR_CRSWLER_AUTHORIZATION = "common-deliverr-authorization:common:authorization"
DELIVERR_API_AUTHORIZATION = "crawler-deliverr-inventory-order:common:api_key"
DIANXIAOMI_CRSWLER_COOKIE = "common-dianxiaomi-cookie:common:cookies"
DINGDING_AUTH_TOKEN = "common-dingding-access-token:common:access_token"
ERP321_AUTH_TOKEN = "common-erp321-access-token:common:access_token"
ERP321_COOKIES = "common-erp321-cookie:common:cookies"
