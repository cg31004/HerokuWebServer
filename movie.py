import requests
from datetime import date, datetime, timedelta
import json
from bs4 import BeautifulSoup



#yahoo api https://movies.yahoo.com.tw/ajax/pc/get_schedule_by_movie?movie_id=9119&date=2019-04-04&area_id=



day = (date.today() + timedelta(days=1)).strftime('%Y-%m-%d')
url = 'https://movies.yahoo.com.tw/ajax/pc/get_schedule_by_movie?movie_id=9924&date=2019-07-06'
movie_json = (requests.get(url)).json()
movie_datas = BeautifulSoup(movie_json["view"],"html.parser")


# area = movie_datas.select("div.pc-movie-schedule-form div.area_timebox")
with open('data.html' , 'w') as f:   
    f.write(str(movie_datas))
# <div class="pc-movie-schedule-form">
#     <div class="area_timebox">
#    <div class="area_title">台北市</div>

#===========================================================================================
