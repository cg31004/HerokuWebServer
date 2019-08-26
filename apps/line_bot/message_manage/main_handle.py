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
    FileMessage,
    FollowEvent,
    JoinEvent,
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
    MovieDB,
    keyword_search,
)
from math import ceil


handler = WebhookHandler(settings.LINE_CHANNEL_SECRET)
line_bot_api = LineBotApi(settings.LINE_CHANNEL_ACCESS_TOKEN)



today = date.today().strftime('%Y-%m-%d')

#=================    Follow 
@handler.add(FollowEvent)
def handle_follow(event):
    Start(event)

@handler.add(JoinEvent)
def handle_join(event):
    Start(event)

#=================    Main  text back
@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    message_text = (event.message.text)
    line_id = event.source.user_id
    controller = ControllerModel.objects.get(line_id = line_id)
    level = Control_level(line_id)
    if message_text == '89702511':
        coa = ControllerModel.objects.all()
        total_user = (len(coa))
        message = TextSendMessage(text='目前使用者有   {}   位'.format(total_user))
        line_bot_api.reply_message(event.reply_token, message)

    elif controller.mod == 2 and level == 1:
        keyword(event,message_text.replace(" ",''))
    
    elif level == 0 :
        Start(event)


    return 0

#=================    Main  postback
@handler.add(PostbackEvent)
def handle_postback(event):
    txt_data = event.postback.data
    
######### postback 字元集
    pb_start = 'StartMoive-'
    pb_richmenu = 'RichMenu-'
    pb_date = 'MovieDatetime-'
    pb_rankmovieid = "RankList-"
    pb_rest = 'RESET-rest'
    pb_back = 'BACK-back'

    pb_tag = 'slimofy.tk'
    pb_area = 'AREA-'

    line_id = event.source.user_id
    controller = ControllerModel.objects.get(line_id = line_id)
    
    level = Control_level(line_id)


###########################    contrl rank movie ID  #################################################
    if pb_rankmovieid in event.postback.data and level == 1: #contrl rank- movieid
        selector = txt_data.strip(pb_rankmovieid)
        if selector != '999999':
            ControllerModel.objects.filter(line_id = line_id).update(movie_id = selector)
            Movie_Date(event,line_id)  # go Date
        else:
            message = '▼▽▼▽▼▽▼▽▼▽▼▽▼\n\n電影未有時刻表\n\n請誤點擊\n\n\n▲△▲△▲△▲△▲△▲△▲'
            line_bot_api.push_message(line_id, TextSendMessage(text=message))

###########################    contrl date  #################################################
    elif pb_date in event.postback.data and level == 2: #contrl date 
        selector = txt_data.strip(pb_date)
        controller =  ControllerModel.objects.get(line_id = line_id)
       
        schedule_data_check = ScheduleModel.objects.filter(movie_id = controller.movie_id , movie_date = selector).all()

        if len(schedule_data_check) == 0:
            line_bot_api.push_message(line_id, TextSendMessage(text='查詢中,請稍後... '))
            
        count = movie_insert(controller.movie_id , selector)
            
        if count > 0:
            ControllerModel.objects.filter(line_id = line_id).update(date = selector)
            Area_selector(event, controller.movie_id, selector)  # go Area
        else:
            line_bot_api.push_message(line_id, TextSendMessage(text='所選日期沒有此電影了,請再選擇或上一步更換電影'))



############################   contrl  contrl  #################################################
    elif pb_tag in event.postback.data and level == 3: #contrl  contrl
        ControllerModel.objects.filter(line_id = line_id).update(control = event.postback.data)
        control_list = (event.postback.data).split(pb_tag)
        controller =  ControllerModel.objects.get(line_id = line_id)
        if pb_area in control_list[0]:  
            area = control_list[0].strip(pb_area)#contrl movie area

            movie_print(event,controller.movie_id, controller.date,area)  # go movie

###########################    contrl Start List  #################################################
    elif pb_start in event.postback.data and level == 0 : #contrl mod 
        selector = txt_data.strip(pb_start)

        ControllerModel.objects.filter(line_id = line_id).update(mod = selector)
        #######  本週熱門
        if int(selector) == 1:
            Ranklist(event)  # go Rank

        elif int(selector) == 2:
            message = '▼▽▼▽▼▽▼▽▼▽▼▽▼\n\n\n請在左下方切換成對話欄輸入查詢電影名稱\n\n\n或點擊按鈕返回\n\n\n▲△▲△▲△▲△▲△▲△▲'
            line_bot_api.push_message(line_id, TextSendMessage(text=message))
            # backandreset(event)
############################   Rich Menu  #################################################
    elif pb_richmenu in event.postback.data:
        selector = txt_data.strip(pb_richmenu)
        Reset(event)
        ControllerModel.objects.filter(line_id = line_id).update(mod = selector)
        if int(selector) == 1:
            Ranklist(event)  # go Rank

        elif int(selector) == 2:
            message = '▼▽▼▽▼▽▼▽▼▽▼▽▼\n\n\n請在左下方切換成對話欄輸入查詢電影名稱\n\n\n或點擊按鈕返回\n\n\n▲△▲△▲△▲△▲△▲△▲'
            line_bot_api.push_message(line_id, TextSendMessage(text=message))
            # backandreset(event)


############################   contrl  rest  #################################################
    elif pb_rest in event.postback.data: #contrl  rest
        Reset(event)

    elif pb_back in event.postback.data: #contrl  pb_back
        level_back(event)
    else:
        print('request no found')
        line_bot_api.push_message(line_id, TextSendMessage(text='請不要點之前的欄位'))


    return 0


###############   level  #######################
def Control_level(id):
    user_ctrl = ControllerModel.objects.get(line_id = id)
    if user_ctrl.control != None:  #movie controller
        return 4
    elif user_ctrl.date != None:  #movie date
        return 3
    elif user_ctrl.movie_id != None:   #movie id   (rank , keyword)
        return 2
    elif user_ctrl.mod != 0: # mod
        return 1
    else:
        return 0
    




#====================== clean data
def Reset(event):
    line_id = event.source.user_id
    ControllerModel.objects.filter(line_id=line_id).update(
        mod = 0,
        movie_id = None,
        date = None,
        control = None,
    )
    # Start(event)

#====================== level back
def level_back(event):
    line_id = event.source.user_id
    controller = ControllerModel.objects.get(line_id=line_id)
    level = Control_level(line_id)
    if level == 1:
        controller.mod = 0
        Reset(event)
    elif level == 2:
        controller.movie_id = None
        if int(controller.mod) == 1:
            Ranklist(event)  # go Rank

        elif int(controller.mod) == 2:
            Reset(event)
    elif level == 3:
        controller.date = None
        Movie_Date(event,line_id)
    elif level ==4:
        controller.control = None
        Area_selector(event, controller.movie_id, controller.date)

    controller.save()


        
        







#====================== Start_list    (Postback)
def Start(event):
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
                #     label='測試',
                #     data='RESET-rest'
                # ),
            ]
        )
    )
    line_bot_api.reply_message(event.reply_token, message)



def keyword(event,message_text):
    movie_list = keyword_search(message_text)
    line_id = event.source.user_id
    if movie_list != 0 : 
        content = list()
        ###############  text
        for movie_id,movie_name in movie_list:


    ################################################ flex carousel button for loops
            sc = SeparatorComponent(height = 'sm',color='#ff0000',)
                    # callAction
            bc = ButtonComponent(
                height	 = 'sm',
                color = '#000000',
                action=PostbackAction(label='{}'.format(movie_name), data='RankList-{}'.format(movie_id)),
            )
            content.append(sc)
            content.append(bc)


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
                            TextComponent(text='關鍵字搜尋', weight='bold', size='xl'),
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
                                                text='搜尋結果▼',
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
                        contents=content
                    ),
                ),
            ]
        )
            
        message = FlexSendMessage(alt_text="大家看電影", contents=message)

        line_bot_api.push_message(line_id, message)
        # backandreset(event)
    else:
        message = TextSendMessage(text='很抱歉.......\n\n未搜到您選擇的電影,請再次輸入')
        line_bot_api.push_message(line_id, message)
        
        



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
            text='您看的電影是:\n  {}'.format(movie_name),
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
            ]
        )
    )
    line_bot_api.push_message(line_id, message)
    # backandreset(event)

#============================================================================= ranklist
def Ranklist(event):
    line_id = event.source.user_id

    rank_date_check = (RankModel.objects.filter(rank_date=today).all())
    if len(rank_date_check) == 0:
        rank_insert()
    rank_date_check = (RankModel.objects.filter(rank_date=today).all())
    # print(rank_date_check)
    content1 = list()
    content2 = list()
    ###############  text
    for i in range(len(rank_date_check)):
        rank = rank_date_check[i].rank
        movie_name = rank_date_check[i].movie_name
        movie_id = rank_date_check[i].movie_id

################################################ flex carousel button for loops
        sc = SeparatorComponent(height = 'sm',color='#ff0000',)
                # callAction
        bc = ButtonComponent(
            height	 = 'sm',
            color = '#000000',
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
    line_bot_api.push_message(line_id, message)
    # backandreset(event)



def Area_selector(event,movie_id ,date):
    line_id = event.source.user_id
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
    end = 10
    area_contents = []
    for cc in range(Carousel_count):
        content_ation = []
        for area_list in area_lists[start:end]:
            sc = SeparatorComponent(size = 'sm',color='#036100')
                    # callAction
            bc = ButtonComponent(
                height	 = 'sm',
                action=PostbackAction(label='{}'.format(area_list), data='AREA-{}slimofy.tk'.format(area_list)),
            )
            content_ation.append(sc)
            content_ation.append(bc)
        start +=10

        if end < area_len :
            end +=10
        else:
            end += (area_len%10)

        one_bubble = Area_Bubble_create(content_ation)
        area_contents.append(Area_Bubble_create(content_ation))
    message = CarouselContainer(contents = area_contents)
    message = FlexSendMessage(alt_text="大家看電影", contents=message)
    line_bot_api.push_message(line_id, message)
    # backandreset(event)

        
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
                                    size='md',
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


def movie_print(event,movie_id, movie_date,area):
    line_id = event.source.user_id
    sof = ScheduleModel.objects.filter(movie_id = movie_id , movie_date = movie_date ,area = area,).all()
    sof_set = set()
    
    for so in sof:
        oneline = (so.theater_id, so.movie_type)
        sof_set.add(oneline)
    sof_lists = list(sof_set)

    sof_len = len(sof_set)
    message_count = ceil(sof_len/10)
    start = 0
    end =10
    for mc in range(message_count):
        movie_content = []
        for theater,movie_type in sof_lists[start:end]:
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
        start+=10
        if end<sof_len:
            end+=10
        else :
            end +=(sof_len%10)
            
        message = CarouselContainer(contents = movie_content)
        message = FlexSendMessage(alt_text="大家看電影", contents=message)
        line_bot_api.push_message(line_id, message)
    # backandreset(event)


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
    count =0
    for tl in time_list:
        count +=1
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
        if count >16:
            break

    if len(time_content) < 2:
        tc =  BoxComponent(
                layout='baseline',
                spacing='sm',
                contents=[TextComponent(
                    text='今日沒有電影了，明日請早',
                    align = 'center',
                    wrap=True,
                    color='#ff0000',
                    size='lg',
                    flex=5,
                )]
            )
        time_content.append(tc)

    return time_content


    
def backandreset(event):
    message = BubbleContainer(
                direction='ltr',
                body=BoxComponent(
                    layout='horizontal',
                    contents=[
                        # info
                        ButtonComponent(
                            height	 = 'sm',
                            action=PostbackAction(label='上一步', data='BACK-back'),
                        ),
                        SeparatorComponent(size = 'sm',color='#036100'),
                        ButtonComponent(
                            height	 = 'sm',
                            action=PostbackAction(label='重新開始', data='RESET-rest'),
                                )
                    ],
                ),
            )
    message = FlexSendMessage(alt_text="大家看電影", contents=message)
    line_bot_api.reply_message(event.reply_token, message)
