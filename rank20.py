import requests
from datetime import date, datetime, timedelta
import json
from bs4 import BeautifulSoup



#yahoo api https://movies.yahoo.com.tw/ajax/pc/get_schedule_by_movie?movie_id=9119&date=2019-04-04&area_id=



day = (date.today() + timedelta(days=1)).strftime('%Y-%m-%d')
url = 'https://movies.yahoo.com.tw/ajax/pc/get_schedule_by_movie?movie_id=9924&date=2019-07-15'