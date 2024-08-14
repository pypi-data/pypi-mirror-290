# _*_ coding: utf-8 _*_
# @Time : 2024/8/1
# @Author : 杨洋
# @Email ： yangyang@doocn.com
# @File : DigiCore
# @Desc :
from enum import Enum


class ToUserMsgParam(Enum):
    """
    https:#open.dingtalk.com/document/isvapp/bots-send-group-chat-messages
    """
    Text = 'sampleText'
    Markdown = 'sampleMarkdown'
    ImageMsg = 'sampleImageMsg'
    Link = 'sampleLink'
    ActionCard = 'sampleActionCard'
    Audio = 'sampleAudio'
    File = 'sampleFile'
    Video = 'sampleVideo'

    def describe(self):
        descriptions = {
            'sampleText': {"content": ""},
            'sampleMarkdown': {
                "title": "",
                "text": ""
            },
            'sampleImageMsg': {"photoURL": ""},
            'sampleLink': {
                "text": "",
                "title": "",
                "picUrl": "",
                "messageUrl": ""
            },
            'sampleActionCard': {
                "title": "",
                "text": "",
                "singleTitle": "",
                "singleURL": ""
            },
            'sampleAudio': {
                "mediaId": "",
                "duration": ""
            },
            'sampleFile': {
                "mediaId": "",
                "fileName": "",
                "fileType": "",
            },
            'sampleVideo': {
                "duration": "",
                "videoMediaId": "",
                "videoType": "",
                "picMediaId": ""
            }
        }
        return descriptions.get(self.value, {"unKnown": "未知状态码"})


class ToWebHookMsgParam(Enum):
    Text = 'text'
    Markdown = 'markdown'
    Link = 'link'
    FeedCard = 'feedCard'
    ActionCard = 'actionCard'

    def describe(self):
        descriptions = {
            "link": {
                "messageUrl": "",
                "picUrl": "",
                "text": "",
                "title": ""
            },
            "markdown": {
                "text": "",
                "title": ""
            },
            "feedCard": {
                "links": {
                    "picURL": "",
                    "messageURL": "",
                    "title": ""
                }
            },
            "text": {
                "content": ""
            }
        }
        return descriptions.get(self.value, {"unKnown": "未知状态码"})



# 机器人id
robotCode = 'ding1chemalq8btne6ji'
# 请求接口
robotUrl = 'https://api.dingtalk.com/v1.0/robot/oToMessages/batchSend'
# 消息体图片
MSG_URL = 'http://pmo4be2db.pic49.websiteonline.cn/upload/750.jpg'