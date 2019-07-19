
import requests
from bs4 import BeautifulSoup
import re
from datetime import date, datetime, timedelta
from ..models import (
    RankModel,
    ScheduleModel,
    MovieModel,
    TheaterModel,
)
from django.db import IntegrityError


#++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
#++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
#++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
#++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

def rank_insert():
    url = 'https://movies.yahoo.com.tw/chart.html'
    response = requests.get(url)
    movie_search = BeautifulSoup(response.text,'html.parser')
    result = movie_search.select('div.rank_list.rankstyle1 div.tr')
    result.pop(0)

    today = date.today().strftime('%Y-%m-%d')
    for r in result:
        rank = int((r.select('div.td')[0]).text)
        name = r.select('div.td div.rank_txt')
        movie_url = ((r.findAll('a', attrs={'href': re.compile("^https://movies.yahoo.com.tw/movieinfo_main/")}))[0]).get('href')
        movie_id = re.compile(r'-?\d*$').search(movie_url).group(0)[1:]
        # movieid = r.select('div.td a')
        if len(name) ==0:
            name = r.select('div.td dd h2')

    ########     將 Rank_list  存入DB
        RankModel.objects.create(
            rank_date = today,
            rank = rank,
            movie_id = movie_id,
            movie_name = name[0].text,
        )

    ########     將 Movie id name  存入DB
        MovieDB(movie_id,name[0].text)

            
#++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
#++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
#++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
#++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++




def movie_insert(movie_id,date):
    url = 'https://movies.yahoo.com.tw/ajax/pc/get_schedule_by_movie?movie_id=9467&date=2019-07-14'#.format(date)
    movie_json = (requests.get(url)).json()
    movie_datas = BeautifulSoup(movie_json["view"],"html.parser")
    area_list = list()
    movie_area = movie_datas.select("div.pc-movie-schedule-form div.area_timebox")
    for ma in movie_area:
        area = ((ma.select("div.area_title"))[0]).text
        all_theater = ma.select('ul')
        for at in all_theater:
            theater_name = (at.select('li.adds a'))[0].text
    #===============================================================================
            movie_type = at.select('li.taps')
            movie_times = at.select('div.input_picker.jq_input_picker')
            for type_time in range(len(movie_type)):
                all_type = (((movie_type[type_time]).text).replace(' ','')).replace('\n','')
                times = movie_times[type_time].select('label')
                for time in times :
                    # sm = ScheduleModel.objects.all().delete()
                    ScheduleModel.objects.create(
                        movie_date = date,
                        movie_id = movie_id,
                        area = area,
                        theater_id = theater_name,
                        movie_type = all_type,
                        movie_time = time.text,
                    )
            TheaterDB(theater_name,area)
    return 0

#++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
#++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
#++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
#++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

def MovieDB(movie_id , movie_name):
    try:
        MovieModel.objects.create(
            movie_id=movie_id,
            movie_name = movie_name,
        )
    except IntegrityError as e:
        ###   帳號已經創立
        pass
    return 0

#++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
#++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
#++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
#++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

def TheaterDB(theater_name,area):
    theater_data_check = TheaterModel.objects.filter(theater_name = theater_name).all()
    try:
        if len(theater_data_check) == 0:
             ########     使用google查詢地址
            url = "https://www.google.com/search?q={}".format(theater_name)
            response = requests.get(url)
            theater_search = BeautifulSoup(response.text,'html.parser')
            address = ((theater_search.select('div.AVsepf span.BNeawe.tAd8D.AP7Wnd'))[0]).text
            TheaterModel.objects.create(
                theater_name = theater_name,
                theater_area = area,
                theater_address = address,
            )
        else:
            #DB 已經有此影城資料
            pass
    except IndexError:
        ########     有些影城無法使用google 直接獲取地址
        TheaterModel.objects.create(
                theater_name = theater_name,
                theater_area = area,
                theater_address = theater_name,
            )

    return 0

    



# def movie(id,date):
#     url = 'https://movies.yahoo.com.tw/ajax/pc/get_schedule_by_movie?movie_id=9924&date={}'.format(date)
#     movie_json = (requests.get(url)).json()
#     movie_datas = BeautifulSoup(movie_json["view"],"html.parser")

#     movie_area = movie_datas.select("div.pc-movie-schedule-form div.area_timebox")

#     for ma in movie_area[:1]:
#         area = ((ma.select("div.area_title"))[0]).text
#         print(area)
#         print('++++++++++++++++++++++++++++++++++++++++++++++++++++++++')
#         all_theater = ma.select('ul')
#         for at in all_theater:
#             theater_name = (at.select('li.adds a'))[0].text
#             print("戲院:    " +theater_name)
#     #===============================================================================
#             movie_type = at.select('li.taps')
#             movie_times = at.select('div.input_picker.jq_input_picker')
#             for type_time in range(len(movie_type)):
#                 all_type = (((movie_type[type_time]).text).replace(' ','')).replace('\n','')
#                 print('版本 :   '+ all_type)
#                 times = movie_times[type_time].select('label')
#                 for time in times :
#                     print('時間:  '+ time.text)
#                     # sm = ScheduleModel.objects.all().delete()
#                     # sm = ScheduleModel.objects.create(
#                     #     movie_date = date,
#                     #     movie_id = '9924',
#                     #     area = area,
#                     #     theater_id = theater_name,
#                     #     movie_type = all_type,
#                     #     movie_time = time.text,
#                     # )

#                 print('------------------------------')
#         print('====================================================================================')
#         print('====================================================================================')
#     return 0