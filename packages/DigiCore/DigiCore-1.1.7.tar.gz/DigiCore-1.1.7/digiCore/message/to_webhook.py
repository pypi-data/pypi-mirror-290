# _*_ coding: utf-8 _*_
# @Time : 2024/8/1
# @Author : 杨洋
# @Email ： yangyang@doocn.com
# @File : DigiCore
# @Desc : 发送消息到群组
import json

import requests
from loguru import logger
from typing import Optional

from digiCore.common.decorate import def_retry
from digiCore.message.config import ToWebHookMsgParam


class ToWebhook:

    def __init__(self, webhook: str,
                 atUserIds: Optional[list] = None,
                 atMobiles: Optional[list] = None,
                 ):
        self.webhook = webhook
        self.atUserIds = atUserIds
        self.atMobiles = atMobiles

    @def_retry()
    def send(self, body):
        """
        Send a message to webhook
        """
        headers = {
            "Content-Type": "application/json",
            "Charset": "UTF-8"
        }
        response = requests.post(
            url=self.webhook,
            data=json.dumps(body),
            headers=headers
        )
        if response.status_code != 200:
            logger.error(response.text)
        else:
            logger.info(f"Successfully sent message to {response.text}")

    def send_text_message(self, content: str):
        '''文本格式'''

        body = {"at": {
            "atMobiles": self.atMobiles,
            "atUserIds": self.atUserIds,
            "isAtAll": "false"
        }, "text": {
            "content": content
        }, "msgtype": ToWebHookMsgParam.Text.value
        }
        self.send(body)

    def send_markdown_message(self, text: str, title: str):
        '''markdown格式'''

        body = {
            "msgtype": ToWebHookMsgParam.Markdown.value,
            ToWebHookMsgParam.Markdown.value: {
                "title": title,
                "text": text

            },
            "at": {
                "atMobiles": self.atMobiles,
                "atUserIds": self.atUserIds,
                "isAtAll": "false"
            }
        }
        self.send(body)

    def send_link_message(self,
                          messageUrl: str,
                          title: str,
                          picUrl: str,
                          text: str):
        """
        link格式
        messageUrl：点击消息跳转的URL
        picUrl:图片地址
        title：标题
        text：内容
        """
        body = {
            ToWebHookMsgParam.Link.value: {
                "messageUrl": messageUrl,
                "picUrl": picUrl,
                "text": text,
                "title": title
            },
            "msgtype": ToWebHookMsgParam.Link.value
        }
        self.send(body)

    def send_feedCard_message(self,
                              messageUrl: str,
                              title: str,
                              picUrl: str):
        """
        feedCard格式
        messageUrl：点击消息跳转的URL
        picUrl:图片地址
        title：标题
        """
        body = {
            ToWebHookMsgParam.FeedCard.value: {
                "links": [
                    {
                        "picURL": picUrl,
                        "messageURL": messageUrl,
                        "title": title
                    }
                ]
            },
            "msgtype": ToWebHookMsgParam.FeedCard.value
        }
        self.send(body)


if __name__ == '__main__':
    t = ToWebhook(
        webhook="https://oapi.dingtalk.com/robot/send?access_token=1d18481ce76de55ebc77d8b0d5c0033c0aaabe9661d06266693e2b1fdc091809"
    )
    t.send_feedCard_message(messageUrl='https://www.baidu.com',
                            title='baidu',
                            picUrl='')
