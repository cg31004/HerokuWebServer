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
from datetime import date, datetime, timedelta
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
import requests
from datetime import date, datetime, timedelta
import json
from bs4 import BeautifulSoup
from apps.line_bot.models import ScheduleModel


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

    message_text = (event.message.text)
    print(str(event))
    # print(event.text)
    today = (date.today()).strftime('%Y-%m-%d')
    tomorrow = (date.today() + timedelta(days=1)).strftime('%Y-%m-%d')
    after_tomorrow = (date.today() + timedelta(days=2)).strftime('%Y-%m-%d')
    message = TemplateSendMessage(
        alt_text='電影',
        template=ButtonsTemplate(
            title='選擇想看的日期',
            text='你看的電影是:  ',
            actions=[
                PostbackTemplateAction(
                    label='Today({})'.format(today),
                    data=today
                ),
                PostbackTemplateAction(
                    label='Tomorrow({})'.format(tomorrow),
                    data=tomorrow
                ),
                PostbackTemplateAction(
                    label='After_Tomorrow({})'.format(after_tomorrow),
                    data=after_tomorrow
                )
            ]
        )
    )
    line_bot_api.reply_message(event.reply_token, message)

    # line_bot_api.reply_message(event.reply_token, [TextSendMessage(text=event.postback.data),TextSendMessage(text = '請輸入你選擇的電影')])

@handler.add(PostbackEvent)
def handle_postback(event):
    date = event.postback.data
    movie(date)
    line_bot_api.reply_message(event.reply_token, [TextSendMessage(text=event.postback.data),TextSendMessage(text = '請輸入你選擇的電影')])



def movie(id,date):
    url = 'https://movies.yahoo.com.tw/ajax/pc/get_schedule_by_movie?movie_id=9924&date={}'.format(date)
    movie_json = (requests.get(url)).json()
    movie_datas = BeautifulSoup(movie_json["view"],"html.parser")

    movie_area = movie_datas.select("div.pc-movie-schedule-form div.area_timebox")

    for ma in movie_area[:1]:
        area = ((ma.select("div.area_title"))[0]).text
        print(area)
        print('++++++++++++++++++++++++++++++++++++++++++++++++++++++++')
        all_theater = ma.select('ul')
        for at in all_theater:
            theater_name = (at.select('li.adds a'))[0].text
            print("戲院:    " +theater_name)
    #===============================================================================
            movie_type = at.select('li.taps')
            movie_times = at.select('div.input_picker.jq_input_picker')
            for type_time in range(len(movie_type)):
                all_type = (((movie_type[type_time]).text).replace(' ','')).replace('\n','')
                print('版本 :   '+ all_type)
                times = movie_times[type_time].select('label')
                for time in times :
                    print('時間:  '+ time.text)
                    # sm = ScheduleModel.objects.all().delete()
                    # sm = ScheduleModel.objects.create(
                    #     movie_date = date,
                    #     movie_id = '9924',
                    #     area = area,
                    #     theater_id = theater_name,
                    #     movie_type = all_type,
                    #     movie_time = time.text,
                    # )

                print('------------------------------')
        print('====================================================================================')
        print('====================================================================================')
    return 0
