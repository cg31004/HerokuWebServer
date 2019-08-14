
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
        if len(name) ==0:
            name = r.select('div.td dd h2')
        name = name[0].text
        try:
            movie_url = ((r.findAll('a', attrs={'href': re.compile("^https://movies.yahoo.com.tw/movieinfo_main/")}))[0]).get('href')
            movie_id = re.compile(r'-?\d*$').search(movie_url).group(0)[1:]
        except:
            name+="(台灣尚未上映)"
            movie_id = '999999'

    ########     將 Rank_list  存入DB
        RankModel.objects.create(
            rank_date = today,
            rank = rank,
            movie_id = movie_id,
            movie_name = name,
        )

    ########     將 Movie id name  存入DB
        MovieDB(movie_id,name[0].text)

            
#++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
#++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
#++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
#++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++




def movie_insert(movie_id,date):
    url = 'https://movies.yahoo.com.tw/ajax/pc/get_schedule_by_movie?movie_id={}&date={}'.format(movie_id,date)
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
    if movie_id != '999999':
        try:
            MovieModel.objects.create(
                movie_id = movie_id,
                movie_name = movie_name,
            )
        except IntegrityError as e:
            ###   帳號已經創立
            pass
    else:
        ### 電影尚未上映  ID不填入
        return 0
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

def keyword_search(keyword):
    url = 'https://movies.yahoo.com.tw/moviesearch_result.html?keyword={}&type=movie'.format(keyword)
    response = requests.get(url)
    movie_search = BeautifulSoup(response.text,'html.parser')
    result = movie_search.select('li div.release_info')
    movie_list = list()
    count = 0
    for r in result:
        if r.find("a", {'class':'btn_s_time no_select'}) is None:
            count += 1
            movie_name = ((r.select('div.release_movie_name a'))[0])
            movie_url = movie_name.get('href')
            movie_id = re.compile(r'-?\d*$').search(movie_url).group(0)[1:]
            MovieDB(movie_id , movie_name.text)
            movie_list.append((movie_id,movie_name.text))
        if count > 4 :
            break
    
    return movie_list if count > 0 else 0

