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
from datetime import date, datetime, timedelta,time
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
    URIAction,
    URITemplateAction,
    DatetimePickerTemplateAction,
    ImageCarouselTemplate,
    ImageCarouselColumn,
    PostbackAction,

)
from linebot.models import (
    FlexSendMessage, 
    BubbleContainer,
    CarouselContainer, 
    ImageComponent, 
    BoxComponent,
    TextComponent, 
    SpacerComponent, 
    IconComponent, 
    ButtonComponent,
    SeparatorComponent,
)
from django.conf import settings
import json
import requests
from datetime import date, datetime, timedelta
import json
from bs4 import BeautifulSoup
from apps.line_bot.models import (
    ScheduleModel,
    ControllerModel,
    RankModel,
    MovieModel,
    TheaterModel,
)

from apps.line_bot.movietaker.movie_handler import (
    rank_insert,
    movie_insert,
    MovieDB
)
from math import ceil


handler = WebhookHandler(settings.LINE_CHANNEL_SECRET)
line_bot_api = LineBotApi(settings.LINE_CHANNEL_ACCESS_TOKEN)


# send_exit = TextSendMessage(text='輸入  "電影"  or "Q" 重新選擇電影    \n輸入 "B" 回上一頁')
# def local_set(name:str , local:str ,lat:float, lng:float):
#     location_message = LocationSendMessage(
#         title=name,
#         address=local,
#         latitude=lat,
#         longitude=lng
#     )
#     return location_message
today = date.today().strftime('%Y-%m-%d')
# yesterday = (date.today() - timedelta(days=1)).strftime('%Y-%m-%d')
# ScheduleModel.objects.filter(movie_date = yesterday).all().delete()
#=================    Main  text back
@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    message_text = (event.message.text)
    line_id = event.source.user_id
    ControllerModel.objects.filter(line_id = line_id)
    #{"message": {"id": "10210860238221", "text": "5566", "type": "text"}, "replyToken": "a5c9fcb1839843ca8bb24c79036d4406", "source": {"type": "user", "userId": "U0f254622cb2a6d76452f38b93602081e"}, "timestamp": 1563094438502, "type": "message"}
    if message_text == "1":
        Start(event)
    elif message_text == "2":
        movie_print(event,'10020', '2019-07-17','台北市')
        # movie_print(event)
    elif message_text == "3":
        movie_bubble_create(event,'9467', '2019-07-18','台南')
    elif message_text == "5":
        yesterday = (date.today() - timedelta(days=5)).strftime('%Y-%m-%d')
        ScheduleModel.objects.filter(movie_date = yesterday).all().delete()
    else:
        Reset(event)


    return 0

#=================    Main  postback
@handler.add(PostbackEvent)
def handle_postback(event):
    txt_data = event.postback.data
    
######### postback 字元集
    pb_start = 'StartMoive-'
    pb_date = 'MovieDatetime-'
    pb_rankmovieid = "RankList-"
    pb_rest = 'RESET-rest'

    pb_tag = 'slimofy.tk'
    pb_area = 'AREA-'

    line_id = event.source.user_id

    controller = ControllerModel.objects.get(line_id = line_id)
    
###########################    contrl Start List  #################################################
    if pb_start in event.postback.data: #contrl mod 
        selector = txt_data.strip(pb_start)

        ControllerModel.objects.filter(line_id = line_id).update(mod = selector)
        #######  本週熱門
        if int(selector) == 1:
            Ranklist(event)
        elif int(selector) == 2:
            text = '本功能尚未完成'
            line_bot_api.reply_message(event.reply_token, TextSendMessage(text=text))

        elif int(selector) == 0:
            Reset(event)
        # line_bot_api.reply_message(event.reply_token, TextSendMessage(text=selector))

###########################    contrl rank movie ID  #################################################
    elif pb_rankmovieid in event.postback.data: #contrl rank- movieid
        selector = txt_data.strip(pb_rankmovieid)
        ControllerModel.objects.filter(line_id = line_id).update(movie_id = selector)
        Movie_Date(event,line_id)
        # line_bot_api.reply_message(event.reply_token, TextSendMessage(text=selector))

###########################    contrl date  #################################################
    elif pb_date in event.postback.data: #contrl date 
        selector = txt_data.strip(pb_date)

        ControllerModel.objects.filter(line_id = line_id).update(date = selector)
        controller =  ControllerModel.objects.get(line_id = line_id)
       

        schedule_data_check = ScheduleModel.objects.filter(movie_id = controller.movie_id , movie_date = controller.date).all()
        if len(schedule_data_check) == 0:
            line_bot_api.push_message(line_id, TextSendMessage(text='查詢中,請稍後...'))
            movie_insert(controller.movie_id , controller.date)     

        Area_selector(event, controller.movie_id, controller.date)
        # text = '您選擇的是\nName :{}\n時間{}'.format(movie_name,user.date)

        # line_bot_api.reply_message(event.reply_token, TextSendMessage(text=text))



############################   contrl  contrl  #################################################
    elif pb_tag in event.postback.data: #contrl  contrl
        ControllerModel.objects.filter(line_id = line_id).update(control = event.postback.data)
        control_list = (event.postback.data).split(pb_tag)
        controller =  ControllerModel.objects.get(line_id = line_id)
        if pb_area in control_list[0]:  
            area = control_list[0].strip(pb_area)#contrl movie area
            # line_bot_api.reply_message(event.reply_token, TextSendMessage(text=selector))

            # movie_print(event, controller.movie_id, controller.date,area)
            # movie_print(event,'10020', '2019-07-17','台北市')
            movie_bubble_create(event,controller.movie_id, controller.date,area)

############################   contrl  rest  #################################################
    elif pb_rest in event.postback.data: #contrl  rest
        Reset(event)
        Start(event)
    else:
        print('haha')

    return 0

# {"postback": {"data": "2"}, "replyToken": "3eed9b81074c47099759c51c9ec145f6", "source": {"type": "user", "userId": "U0f254622cb2a6d76452f38b93602081e"}, "timestamp": 1563196939593, "type": "postback"}




    






#====================== clean data
def Reset(event):
    line_id = event.source.user_id
    ControllerModel.objects.filter(line_id=line_id).update(
        mod = 0,
        movie_id = None,
        date = None,
        control = None,
    )


#====================== Start_list    (Postback)
def Start(event):
    lineid = event.source.user_id
    message = TemplateSendMessage(
        alt_text='大家看電影',
        template=ButtonsTemplate(
            title='請選擇下列方式',
            text='您想選擇的方式是:  ',
            actions=[
                PostbackTemplateAction(
                    label='本週熱門',
                    data='StartMoive-1'
                ),
                PostbackTemplateAction(
                    label='關鍵字搜尋',
                    data='StartMoive-2'
                ),
                # PostbackTemplateAction(
                #     label='取消',
                #     data='StartMoive-0'
                # )
            ]
        )
    )
    line_bot_api.reply_message(event.reply_token, message)


#====================== Movie_Date    (Postback)
def Movie_Date(event,line_id):
    today = (date.today()).strftime('%Y-%m-%d')
    tomorrow = (date.today() + timedelta(days=1)).strftime('%Y-%m-%d')
    after_tomorrow = (date.today() + timedelta(days=2)).strftime('%Y-%m-%d')
    movie_id = (ControllerModel.objects.get(line_id = line_id).movie_id)
    movie_name = (MovieModel.objects.get(movie_id = movie_id)).movie_name

    message = TemplateSendMessage(
        alt_text='大家看電影',
        template=ButtonsTemplate(
            title='請選擇想看的日期',
            text='您看的電影是:  {}'.format(movie_name),
            actions=[
                PostbackTemplateAction(
                    label='今天({})'.format(today),
                    data='MovieDatetime-{}'.format(today)
                ),
                PostbackTemplateAction(
                    label='明天({})'.format(tomorrow),
                    data='MovieDatetime-{}'.format(tomorrow)
                ),
                PostbackTemplateAction(
                    label='後天({})'.format(after_tomorrow),
                    data='MovieDatetime-{}'.format(after_tomorrow)
                ),
                PostbackTemplateAction(
                    label='取消',
                    data='RESET-rest',
                )
            ]
        )
    )
    line_bot_api.reply_message(event.reply_token, message)


#============================================================================= Schedule
def Schedule_print(event):
    message = TemplateSendMessage(
        alt_text='大家看電影',
        template=CarouselTemplate(
            columns=[
                CarouselColumn(
                    title='AAA影城',
                    text='時間:▼  \n10:00\n12:00\n14:00',
                    actions=[
                        URITemplateAction(
                            label='新北市樹林區大雅路7777號',
                            uri='http://example.com/1'
                        ),
                        PostbackTemplateAction(
                            label='Y',
                            text='Y',
                            data='123'
                        )
                    ]
                ),
                CarouselColumn(
                    title='AAA影城',
                    text='時間:▼  \n10:00\n12:00\n14:00',
                    actions=[
                        URITemplateAction(
                            label='新北市樹林區大雅路7777號',
                            uri='http://example.com/1'
                        ),
                        PostbackTemplateAction(
                            label='Y',
                            text='Y',
                            data='123'
                        )
                    ]
                ),
            ]
        )
    )
    line_bot_api.reply_message(event.reply_token, message)

#============================================================================= ranklist
def Ranklist(event):
    
    rank_date_check = (RankModel.objects.filter(rank_date=today).all())
    if len(rank_date_check) == 0:
        rank_insert()
    rank_date_check = (RankModel.objects.filter(rank_date=today).all())

    content1 = list()
    content2 = list()
    ###############  text
    for i in range(len(rank_date_check)):
        rank = rank_date_check[i].rank
        movie_name = rank_date_check[i].movie_name
        movie_id = rank_date_check[i].movie_id


################################################ flex carousel button for loops
        sc = SeparatorComponent(height = 'sm',)
                # callAction
        bc = ButtonComponent(
            height	 = 'sm',
            action=PostbackAction(label='{}.   {}'.format(rank,movie_name), data='RankList-{}'.format(movie_id)),
        )
        if i <10:
            content1.append(sc)
            content1.append(bc)
        else:
            content2.append(sc)
            content2.append(bc)

################################################ make message
    message = CarouselContainer(
        contents=[
            ######  Bubble1            
            BubbleContainer(
                direction='ltr',
                body=BoxComponent(
                    layout='vertical',
                    contents=[
                        # title
                        TextComponent(text='電影排行榜', weight='bold', size='xl'),
                        # info
                        BoxComponent(
                            layout='vertical',
                            margin='lg',
                            spacing='sm',
                            contents=[
                                BoxComponent(
                                    layout='baseline',
                                    spacing='sm',
                                    contents=[
                                        TextComponent(
                                            text='1-10名:▼',
                                            color='#aaaaaa',
                                            size='sm',
                                            flex=2
                                        ),
                                    ],
                                ),
                            ],
                        )
                    ],
                ),
                footer=BoxComponent(
                    layout='vertical',
                    spacing='sm',
                    contents=content1
                ),
            ),
            ######  Bubble2
            BubbleContainer(
                direction='ltr',
                body=BoxComponent(
                    layout='vertical',
                    contents=[
                        # title
                        TextComponent(text='電影排行榜', weight='bold', size='xl'),
                        # info
                        BoxComponent(
                            layout='vertical',
                            margin='lg',
                            spacing='sm',
                            contents=[
                                BoxComponent(
                                    layout='baseline',
                                    spacing='sm',
                                    contents=[
                                        TextComponent(
                                            text='10-20名:▼',
                                            color='#aaaaaa',
                                            size='sm',
                                            flex=2
                                        ),
                                    ],
                                ),
                            ],
                        )
                    ],
                ),
                footer=BoxComponent(
                    layout='vertical',
                    spacing='sm',
                    contents=content2
                ),
            ),
        ]
    )
        
    message = FlexSendMessage(alt_text="大家看電影", contents=message)
    line_bot_api.reply_message(event.reply_token, message)

def control_check(line_id):
    control_check = ControllerModel.objects.get(line_id = line_id)


def Area_selector(event,movie_id ,date):
    area_total = ['台北市', '新北市', '桃園', '新竹', '苗栗', '台中', '彰化', '南投', '雲林', '嘉義', '台南', '高雄', '屏東', '基隆', '宜蘭', '花蓮', ' 台東', '金門', '澎湖','台東']
    all_Schs = ScheduleModel.objects.filter(movie_id=movie_id,movie_date=date).all()
    area_set = set()
    for allsch in all_Schs:
        area_set.add(allsch.area)
    area_lists = list(area_set)
    area_lists.sort(key=area_total.index)

    area_len = len(area_set)
    Carousel_count = ceil(area_len/10)
    start =0
    end = 9
    search_rest = ButtonComponent(
                height	 = 'sm',
                action=PostbackAction(label='取消', data='RESET-rest',)
            )

    area_contents = []
    for cc in range(Carousel_count):
        content_ation = []
        for area_list in area_lists[start:end]:
            sc = SeparatorComponent(size = 'sm',)
                    # callAction
            bc = ButtonComponent(
                height	 = 'sm',
                action=PostbackAction(label='{}'.format(area_list), data='AREA-{}slimofy.tk'.format(area_list)),
            )
            content_ation.append(sc)
            content_ation.append(bc)
        start +=9

        if end < area_len :
            end +=9
            content_ation.append(sc)
            content_ation.append(search_rest)
        else:
            end += (area_len%9)
    ######### reset postback
            content_ation.append(sc)
            content_ation.append(search_rest)

        one_bubble = Area_Bubble_create(content_ation)
        area_contents.append(Area_Bubble_create(content_ation))
    
    message = CarouselContainer(contents = area_contents)
    message = FlexSendMessage(alt_text="大家看電影", contents=message)
    line_bot_api.reply_message(event.reply_token, message)

        
#######    Area_selector  縣市 Bubble 創建
def Area_Bubble_create(area_list):
    
    BC = BubbleContainer(
        direction='ltr',
        body=BoxComponent(
            layout='vertical',
            contents=[
                # title
                TextComponent(text='所在縣市', weight='bold', size='xl'),
                # info
                BoxComponent(
                    layout='vertical',
                    margin='lg',
                    spacing='sm',
                    contents=[
                        BoxComponent(
                            layout='baseline',
                            spacing='sm',
                            contents=[
                                TextComponent(
                                    text='選擇所在縣市',
                                    color='#aaaaaa',
                                    size='sm',
                                    flex=2
                                ),
                            ],
                        ),
                    ],
                ),
                BoxComponent(
                    layout='vertical',
                    spacing='sm',
                    contents=area_list
                ),
            ],
        ),
        # footer=
    )
    return BC

            
# def movie_print(event,movie_id, movie_date,area):


#     message = FlexSendMessage(alt_text="大家看電影", contents=bubble)
#     line_bot_api.reply_message(event.reply_token, message)

def movie_bubble_create(event,movie_id, movie_date,area):
    sof = ScheduleModel.objects.filter(movie_id = movie_id , movie_date = movie_date ,area = area,).all()
    sof_set = set()
    movie_content = list()
    for so in sof:
        oneline = (so.theater_id, so.movie_type)
        sof_set.add(oneline)
    # print(sof_set)
    # print(len(sof_set))

    for theater,movie_type in sof_set:
        sof = ScheduleModel.objects.filter(movie_id = movie_id , movie_date = movie_date,theater_id =theater ,area = area,  movie_type = movie_type).all()
        time_sche = time_schedule(sof)

        theater_address = (TheaterModel.objects.get(theater_name = theater , theater_area = area)).theater_address

        bubble = BubbleContainer(
                direction='ltr',
                body=BoxComponent(
                    layout='vertical',
                    contents=[
                        # title
                        TextComponent(text=theater, weight='bold', size='lg'),
                        # date
                        BoxComponent(
                            layout='vertical',
                            margin='md',
                            contents=[
                                TextComponent(text= theater_address, ssize='xs', color='#999999', margin='xl', flex=0),
                                TextComponent(text = '{}'.format(movie_date), size='xs', color='#0001eb', margin='xl', flex=5),
                                TextComponent(text='版本:  {}'.format(movie_type), size='xs', color='#81005f', margin='xl', flex=6),
                            ]
                        ),
                        # info
                        BoxComponent(
                            layout='vertical',
                            margin='lg',
                            spacing='sm',
                            contents=time_sche,
                        ),
                    ],
                ),
                footer=BoxComponent(
                    layout='vertical',
                    spacing='sm',
                    contents=[
                        # callAction, separator, websiteAction
                        SpacerComponent(size='xs'),
                        # websiteAction
                        ButtonComponent(
                            style='link',
                            height='sm',
                            action=URIAction(label='GoogleMap', uri="https://maps.google.com.tw/maps?f=q&hl=zh-TW&geocode=&q={}".format(theater_address.replace(' ','')))
                            # action=URIAction(label='GoogleMap', uri='https://google.com')
                        )
                    ]
                ),
            )
        movie_content.append(bubble)
    
    message = CarouselContainer(contents = movie_content)
       
    message = FlexSendMessage(alt_text="大家看電影", contents=message)
    # print(message) 
    # line_bot_api.push_message(event.source.user_id, message)
    line_bot_api.reply_message(event.reply_token, message)



def movie_print(event,movie_id, movie_date,area):
# def movie_print(event):
    sof = ScheduleModel.objects.filter(movie_id = movie_id , movie_date = movie_date,theater_id ='國賓影城(台北長春廣場)' ,area = area,  movie_type = '數位').all()
    time_sche = time_schedule(sof)

    theater_address = (TheaterModel.objects.get(theater_name = sof[0].theater_id , theater_area = area)).theater_address
    movie_type = sof[0].movie_type


    bubble = BubbleContainer(
            direction='ltr',
            body=BoxComponent(
                layout='vertical',
                contents=[
                    # title
                    TextComponent(text=sof[0].theater_id, weight='bold', size='lg'),
                    # date
                    BoxComponent(
                        layout='vertical',
                        margin='md',
                        contents=[
                            TextComponent(text= theater_address, ssize='xs', color='#999999', margin='xl', flex=0),
                            TextComponent(text='2019-07-14', size='xs', color='#0001eb', margin='xl', flex=5),
                            TextComponent(text='版本:  {}'.format(movie_type), size='xs', color='#81005f', margin='xl', flex=6),
                        ]
                    ),
                    # info
                    BoxComponent(
                        layout='vertical',
                        margin='lg',
                        spacing='sm',
                        contents=time_sche,
                    ),
                ],
            ),
            footer=BoxComponent(
                layout='vertical',
                spacing='sm',
                contents=[
                    # callAction, separator, websiteAction
                    SpacerComponent(size='xs'),
                    # websiteAction
                    ButtonComponent(
                        style='link',
                        height='sm',
                        action=URIAction(label='GoogleMap', uri="https://maps.google.com.tw/maps?f=q&hl=zh-TW&geocode=&q={}".format(theater_address))
                    )
                ]
            ),
        )
        
    message = FlexSendMessage(alt_text="大家看電影", contents=bubble)
    
    # line_bot_api.push_message(event.source.user_id, message)
    line_bot_api.reply_message(event.reply_token, message)


def time_schedule(time_list):
    time_content = list()
    title = BoxComponent(
        layout='baseline',
        spacing='lg',
        contents=[
            TextComponent(
                text='時刻表:▼ ',
                color='#000000',
                size='sm',
                flex=1
            ),
        ],
    )
    time_content.append(title)
    time_now = (datetime.now()).strftime('%H:%M')
    for tl in time_list:
        if time_now < str(tl.movie_time):
            times = (tl.movie_time).strftime("%H:%M")
            # print(tl.movie_time)
            tc =  BoxComponent(
                layout='baseline',
                spacing='sm',
                contents=[TextComponent(
                    text=times,
                    align = 'center',
                    wrap=True,
                    color='#666666',
                    size='xs',
                    flex=5,
                )]
            )
        
            time_content.append(tc) 
                        
    return time_content


            
            

    

    

    # message = TemplateSendMessage(
    #     alt_text='大家看電影',
    #     template=CarouselTemplate(
    #         columns=[
    #             CarouselColumn(
    #                 title='本週強檔',s
    #                 text='1-10名:▼ ',
    #                 actions=action1
    #             ),
    #             CarouselColumn(
    #                 title='本週強檔~',
    #                 text='10-20名:▼ ',
    #                 actions=action2
    #             )]
    #     )
    # )


            


# bubble = BubbleContainer(
#         direction='ltr',
#         hero=ImageComponent(
#             url='https://example.com/cafe.jpg',
#             size='full',
#             aspect_ratio='20:13',
#             aspect_mode='cover',
#             action=URIAction(uri='http://example.com', label='label')
#         ),
#         body=BoxComponent(
#             layout='vertical',
#             contents=[
#                 # title
#                 TextComponent(text='Brown Cafe', weight='bold', size='xl'),
#                 # review
#                 BoxComponent(
#                     layout='baseline',
#                     margin='md',
#                     contents=[
#                         IconComponent(size='sm', url='https://example.com/gold_star.png'),
#                         IconComponent(size='sm', url='https://example.com/grey_star.png'),
#                         IconComponent(size='sm', url='https://example.com/gold_star.png'),
#                         IconComponent(size='sm', url='https://example.com/gold_star.png'),
#                         IconComponent(size='sm', url='https://example.com/grey_star.png'),
#                         TextComponent(text='4.0', size='sm', color='#999999', margin='md',
#                                         flex=0)
#                     ]
#                 ),
#                 # info
#                 BoxComponent(
#                     layout='vertical',
#                     margin='lg',
#                     spacing='sm',
#                     contents=[
#                         BoxComponent(
#                             layout='baseline',
#                             spacing='sm',
#                             contents=[
#                                 TextComponent(
#                                     text='Place',
#                                     color='#aaaaaa',
#                                     size='sm',
#                                     flex=1
#                                 ),
#                                 TextComponent(
#                                     text='Shinjuku, Tokyo',
#                                     wrap=True,
#                                     color='#666666',
#                                     size='sm',
#                                     flex=5
#                                 )
#                             ],
#                         ),
#                         BoxComponent(
#                             layout='baseline',
#                             spacing='sm',
#                             contents=[
#                                 TextComponent(
#                                     text='Time',
#                                     color='#aaaaaa',
#                                     size='sm',
#                                     flex=1
#                                 ),
#                                 TextComponent(
#                                     text="10:00 - 23:00",
#                                     wrap=True,
#                                     color='#666666',
#                                     size='sm',
#                                     flex=5,
#                                 ),
#                             ],
#                         ),
#                     ],
#                 )
#             ],
#         ),
#         footer=BoxComponent(
#             layout='vertical',
#             spacing='sm',
#             contents=[
#                 # callAction, separator, websiteAction
#                 SpacerComponent(size='sm'),
#                 # callAction
#                 ButtonComponent(
#                     style='link',
#                     height='sm',
#                     action=URIAction(label='CALL', uri='tel:000000'),
#                 ),
#                 # separator
#                 SeparatorComponent(),
#                 # websiteAction
#                 ButtonComponent(
#                     style='link',
#                     height='sm',
#                     action=URIAction(label='WEBSITE', uri="https://example.com")
#                 )
#             ]
#         ),
#     )
# message = FlexSendMessage(alt_text="hello", contents=bubble)
# line_bot_api.reply_message(event.reply_token, message)