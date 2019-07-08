# -*- coding: utf-8 -*-
'''
                    " MAIN " control
            of handler.handle(body, signature)
================================================================================
1. root
2. company
                                            Author: JackaL
                                            Updated: 20180620
'''
from linebot import WebhookHandler, LineBotApi
import tempfile
import os
from linebot.models import (
    # 下列為使用者發送給 Line 訊息
    MessageEvent, # 聽取 message 事件
    TextMessage, # 聽取使用者輸入訊息
    PostbackEvent, # 聽取 Postback 事件
    FileMessage
)
# reply user
from linebot.models import (
    TextSendMessage, # （文字訊息）
    StickerSendMessage, # （貼圖訊息）
    ImageSendMessage, # （圖片訊息）
    LocationSendMessage, # （位置訊息）
)
# models for replying
from linebot.models import (
    TemplateSendMessage,
    Template,
    ButtonsTemplate,
    ConfirmTemplate,
    CarouselTemplate,
    CarouselColumn,
    TemplateAction,
    PostbackTemplateAction,
    MessageTemplateAction,
    URITemplateAction,
    DatetimePickerTemplateAction,
    ImageCarouselTemplate,
    ImageCarouselColumn,

)
from django.conf import settings
import json

handler = WebhookHandler(settings.LINE_CHANNEL_SECRET)
line_bot_api = LineBotApi(settings.LINE_CHANNEL_ACCESS_TOKEN)


send_exit = TextSendMessage(text='輸入  "電影"  or "Q" 重新選擇電影    \n輸入 "B" 回上一頁')
def local_set(name:str , local:str ,lat:float, lng:float):
    location_message = LocationSendMessage(
        title=name,
        address=local,
        latitude=lat,
        longitude=lng
    )
    return location_message

@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    # message_text = (event.message.text)
    print(str(event))
    # print(event.text)
    line_bot_api.reply_message(event.reply_token, [TextSendMessage(text='你好'),TextSendMessage(text = '請輸入你選擇的電影')])










