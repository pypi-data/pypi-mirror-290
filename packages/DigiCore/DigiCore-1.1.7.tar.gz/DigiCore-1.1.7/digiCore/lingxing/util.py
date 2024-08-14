# _*_ coding: utf-8 _*_
# @Time : 2024/7/31
# @Author : 杨洋
# @Email ： yangyang@doocn.com
# @File : DigiCore
# @Desc :
import base64
import hashlib

from crypto.Cipher import AES

BLOCK_SIZE = 16  # Bytes

class EncryptTool:
    """
    加密工具包
    """

    @classmethod
    def do_pad(cls, text):
        return text + (BLOCK_SIZE - len(text) % BLOCK_SIZE) * \
               chr(BLOCK_SIZE - len(text) % BLOCK_SIZE)

    @classmethod
    def aes_encrypt(cls, key, data):
        """
        AES的ECB模式加密方法
        :param key: 密钥
        :param data:被加密字符串（明文）
        :return:密文
        """
        key = key.encode('utf-8')
        # 字符串补位
        data = cls.do_pad(data)
        cipher = AES.new(key, AES.MODE_ECB)
        # 加密后得到的是bytes类型的数据，使用Base64进行编码,返回byte字符串
        result = cipher.encrypt(data.encode())
        encode_str = base64.b64encode(result)
        enc_text = encode_str.decode('utf-8')
        return enc_text

    @classmethod
    def md5_encrypt(cls, text: str):
        md = hashlib.md5()
        md.update(text.encode('utf-8'))
        return md.hexdigest()