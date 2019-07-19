# from linebot import WebhookHandler, LineBotApi
# from datetime import date, datetime, timedelta
# import tempfile
# import os
# from linebot.models import (
#     # 下列為使用者發送給 Line 訊息
#     MessageEvent, # 聽取 message 事件
#     TextMessage, # 聽取使用者輸入訊息
#     PostbackEvent, # 聽取 Postback 事件
#     FileMessage
# )
# # reply user
# from linebot.models import (
#     TextSendMessage, # （文字訊息）
#     StickerSendMessage, # （貼圖訊息）
#     ImageSendMessage, # （圖片訊息）
#     LocationSendMessage, # （位置訊息）
# )
# # models for replying
# from linebot.models import (
#     TemplateSendMessage,
#     Template,
#     ButtonsTemplate,
#     ConfirmTemplate,
#     CarouselTemplate,
#     CarouselColumn,
#     TemplateAction,
#     PostbackTemplateAction,
#     MessageTemplateAction,
#     URITemplateAction,
#     DatetimePickerTemplateAction,
#     ImageCarouselTemplate,
#     ImageCarouselColumn,

# )
# from django.conf import settings
# import json
# import requests
# from datetime import date, datetime, timedelta
# import json
# from bs4 import BeautifulSoup


# class line_dialogue():
#     def __init__(self,event):
#         self.id = event.source.user_id
#         self.token = event.reply_token
#     def Start(event):
#         lineid = event.source.user_id
#         message = TemplateSendMessage(
#             alt_text='大家看電影',
#             template=ButtonsTemplate(
#                 title='請選擇下列方式',
#                 text='您想選擇的方式是:  ',
#                 actions=[
#                     PostbackTemplateAction(
#                         label='本週熱門',
#                         data='StartMoive-1'
#                     ),
#                     PostbackTemplateAction(
#                         label='關鍵字搜尋',
#                         data='StartMoive-2'
#                     ),
#                     PostbackTemplateAction(
#                         label='取消',
#                         data='StartMoive-0'
#                     )
#                 ]
#             )
#         )
#         line_bot_api.reply_message(event.reply_token, message)