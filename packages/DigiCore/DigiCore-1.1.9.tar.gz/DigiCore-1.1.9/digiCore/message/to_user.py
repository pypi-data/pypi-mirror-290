# _*_ coding: utf-8 _*_
# @Time : 2024/8/1
# @Author : 杨洋
# @Email ： yangyang@doocn.com
# @File : DigiCore
# @Desc : 发送消息到个人钉钉
import json
from typing import List

import requests
from loguru import logger

from digiCore.common.decorate import def_retry
from digiCore.db.redis.core import RedisDao
from digiCore.message.config import robotUrl, robotCode, ToUserMsgParam, MSG_URL
from typing import Optional


class ToUser:

    def __init__(self, user_ids: List[str],
                 robotCode: Optional[str] = robotCode, ):
        self.user_ids = user_ids
        self.redis = RedisDao()
        self.robotCode = robotCode

    @def_retry()
    def send(self, param, msgKey):
        """
        Send a message to webhook
        """
        access_token = self.redis.get_dingding_access_token()
        headers = {
            "Content-Type": "application/json",
            "Charset": "UTF-8",
            "x-acs-dingtalk-access-token": access_token,
            "robotCode": self.robotCode
        }
        body = {
            "msgParam": json.dumps(param),
            "msgKey": msgKey,
            "robotCode": self.robotCode,
            "userIds": self.user_ids
        }
        response = requests.post(
            url=robotUrl,
            json=body,
            headers=headers
        )
        if response.status_code != 200:
            logger.error(response.text)
        else:
            logger.info(f"Successfully sent message to {response.text}")

    def send_text_message(self, content: str):
        '''文本格式'''
        param = {"content": content}
        msgKey = ToUserMsgParam.Text.value
        self.send(param, msgKey)

    def send_markdown_message(self, text: str, title: str):
        '''markdown格式'''

        param = {
            "title": title,
            "text": text
        }
        msgKey = ToUserMsgParam.Markdown.value
        self.send(param, msgKey)

    def send_images_message(self, photoURL: str):
        '''markdown格式'''

        param = {"photoURL": photoURL}
        msgKey = ToUserMsgParam.ImageMsg.value
        self.send(param, msgKey)

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
        param = {
            "text": text,
            "title": title,
            "picUrl": picUrl,
            "messageUrl": messageUrl
        }
        msgKey = ToUserMsgParam.Link.value
        self.send(param, msgKey)

    def send_action_card_message(self,
                                 singleTitle: str,
                                 title: str,
                                 text: str,
                                 singleURL: str
                                 ):

        """
        action_card格式
        """
        param = {
            "title": title,
            "text": text,
            "singleTitle": singleTitle,
            "singleURL": singleURL
        }
        msgKey = ToUserMsgParam.ActionCard.value
        self.send(param, msgKey)

    def send_audio_message(self,
                           mediaId: str,
                           duration: str
                           ):

        """
        sampleAudio格式
        """
        param = {
            "mediaId": mediaId,
            "duration": duration
        }
        msgKey = ToUserMsgParam.Audio.value
        self.send(param, msgKey)

    def send_file_message(self,
                          mediaId: str,
                          fileName: str,
                          fileType: str
                          ):

        """
        sampleAudio格式
        """
        param = {
            "mediaId": mediaId,
            "fileName": fileName,
            "fileType": fileType
        }
        msgKey = ToUserMsgParam.File.value
        self.send(param, msgKey)

    def send_video_message(self,
                           duration: str,
                           videoMediaId: str,
                           videoType: str,
                           picMediaId: str
                           ):

        """
        sampleVideo格式
        """
        param = {
            "duration": duration,
            "videoMediaId": videoMediaId,
            "videoType": videoType,
            "picMediaId": picMediaId
        }
        msgKey = ToUserMsgParam.Video.value
        self.send(param, msgKey)


if __name__ == '__main__':
    t = ToUser([
        '16566389302394979'
    ])
    t.send_images_message(
        MSG_URL
    )
