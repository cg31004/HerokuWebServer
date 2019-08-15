import requests
from bs4 import BeautifulSoup
import re
import requests
from bs4 import BeautifulSoup
import re
from datetime import date, datetime, timedelta
url = 'https://movies.yahoo.com.tw/chart.html'
# url = "http://127.0.0.1/line_bot/api/theater/?format=api"
# url = 'http://127.0.0.1/line_bot/api/theater/?format=json'
response = requests.get(url)
# print(response.text)
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
        name+="(未有時刻表)"
        movie_id = '999999'
        
    # movieid = r.select('div.td a')   
# movie_search = BeautifulSoup(response.text,'html.parser')
# result = movie_search.select('div.rank_list.rankstyle1 div.tr')
# result.pop(0)

# today = date.today().strftime('%Y-%m-%d')
# for r in result:
#         rank = int((r.select('div.td')[0]).text)
#         name = r.select('div.td div.rank_txt')
#         movie_url = ((r.findAll('a', attrs={'href': re.compile("^https://movies.yahoo.com.tw/movieinfo_main/")}))[0]).get('href')
#         movie_id = re.compile(r'-?\d*$').search(movie_url).group(0)[1:]
#         # movieid = r.select('div.td a')
#         if len(name) ==0:
#                 name = r.select('div.td dd h2')
        