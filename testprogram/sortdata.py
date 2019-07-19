from bs4 import BeautifulSoup



with open('data.html' , 'r') as f:
    data = f.read()


soup = BeautifulSoup(data,'html.parser')

movie_area = soup.select("div.pc-movie-schedule-form div.area_timebox")

for ma in movie_area[:6]:
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
            print('版本 :   '+ ((movie_type[type_time]).text).strip('\n'))
            times = movie_times[type_time].select('label')
            for time in times :
                print('時間:  '+ time.text)
            print('====================================================================================')
    print('------------------------------')
    print('------------------------------')




# <ul class="area_time _c jq_area_time" data-theater_name="國賓影城(台北長春廣場)" data-theater_schedules="https://movies.yahoo.com.tw/theater_result.html/id=29" data-theater_url="http://www.ambassador.com.tw/" id="theater_id_29">
# <li class="adds">
# <a href="https://movies.yahoo.com.tw/theater_result.html/id=29">國賓影城(台北長春廣場)</a>
# <span>02-25155755</span>
# </li>
# <li class="taps">
# <span class="tapR">數位</span> </li>
# <li class="time _c">
# <div class="input_picker jq_input_picker">
# <input class="gabtn" data-ga="['電影頁_時刻表', '電影頁_時刻表_場次', '阿拉丁']" data-movie_date="07.05" data-movie_time="10:50" data-movie_title="阿拉丁" data-movie_type="數位" data-news="news" id="71491917" name="schedule_list" type="radio" value="2019-07-05 10:50:00"/>
# <label class="" for="71491917">10:50</label>
# <input class="gabtn" data-ga="['電影頁_時刻表', '電影頁_時刻表_場次', '阿拉丁']" data-movie_date="07.05" data-movie_time="13:10" data-movie_title="阿拉丁" data-movie_type="數位" data-news="news" id="71491918" name="schedule_list" type="radio" value="2019-07-05 13:10:00"/>
# <label class="" for="71491918">13:10</label>
# <input class="gabtn" data-ga="['電影頁_時刻表', '電影頁_時刻表_場次', '阿拉丁']" data-movie_date="07.05" data-movie_time="17:50" data-movie_title="阿拉丁" data-movie_type="數位" data-news="news" id="71491919" name="schedule_list" type="radio" value="2019-07-05 17:50:00"/>
# <label class="" for="71491919">17:50</label>
# <input class="gabtn" data-ga="['電影頁_時刻表', '電影頁_時刻表_場次', '阿拉丁']" data-movie_date="07.05" data-movie_time="20:10" data-movie_title="阿拉丁" data-movie_type="數位" data-news="news" id="71491920" name="schedule_list" type="radio" value="2019-07-05 20:10:00"/>
# <label class="" for="71491920">20:10</label>
# <input class="gabtn" data-ga="['電影頁_時刻表', '電影頁_時刻表_場次', '阿拉丁']" data-movie_date="07.05" data-movie_time="22:30" data-movie_title="阿拉丁" data-movie_type="數位" data-news="news" id="71491921" name="schedule_list" type="radio" value="2019-07-05 22:30:00"/>
# <label class="" for="71491921">22:30</label>
# </div>
# </li>
# </ul>