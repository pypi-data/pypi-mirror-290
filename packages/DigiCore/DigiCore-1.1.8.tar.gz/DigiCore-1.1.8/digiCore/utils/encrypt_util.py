# _*_ coding: utf-8 _*_
# @Time : 2024/7/31
# @Author : 杨洋
# @Email ： yangyang@doocn.com
# @File : DigiCore
# @Desc :
import base64
import hashlib

from crypto.Cipher import AES


def do_pad(text, BLOCK_SIZE):
    return text + (BLOCK_SIZE - len(text) % BLOCK_SIZE) * \
        chr(BLOCK_SIZE - len(text) % BLOCK_SIZE)


def aes_encrypt(key, data, BLOCK_SIZE=16):
    """
    AES的ECB模式加密方法
    :param key: 密钥
    :param data:被加密字符串（明文）
    :return:密文
    """
    key = key.encode('utf-8')
    # 字符串补位
    data = do_pad(data, BLOCK_SIZE)
    cipher = AES.new(key, AES.MODE_ECB)
    # 加密后得到的是bytes类型的数据，使用Base64进行编码,返回byte字符串
    result = cipher.encrypt(data.encode())
    encode_str = base64.b64encode(result)
    enc_text = encode_str.decode('utf-8')
    return enc_text


def md5_encrypt(text: str):
    md = hashlib.md5()
    md.update(text.encode('utf-8'))
    return md.hexdigest()
