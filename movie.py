import requests
from datetime import date, datetime, timedelta
import json
from bs4 import BeautifulSoup



#yahoo api https://movies.yahoo.com.tw/ajax/pc/get_schedule_by_movie?movie_id=9119&date=2019-04-04&area_id=



day = (date.today() + timedelta(days=1)).strftime('%Y-%m-%d')
# url = 'https://movies.yahoo.com.tw/ajax/pc/get_schedule_by_movie?movie_id=9924&date=2019-07-15'
url = 'https://movies.yahoo.com.tw/ajax/pc/get_schedule_by_movie?movie_id=9924&date=2019-07-30'
movie_json = (requests.get(url)).json()
movie_datas = BeautifulSoup(movie_json["view"],"html.parser")

movie_area = movie_datas.select("div.pc-movie-schedule-form div.area_timebox")

for ma in movie_area[:3]:
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
            all_type =  (((movie_type[type_time]).text).replace(' ','')).replace('\n','')
            print('版本 :   '+ all_type )
            times = movie_times[type_time].select('label')
            for time in times :
                print('時間:  '+ time.text)
            print('------------------------------')
    print('====================================================================================')
    print('====================================================================================')
    
#===========================================================================================
print(len(movie_area))