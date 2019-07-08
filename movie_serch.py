import requests
from bs4 import BeautifulSoup
import re

keyword = input('電影名稱')
url = 'https://movies.yahoo.com.tw/moviesearch_result.html?keyword={}&type=movie'.format(keyword)
response = requests.get(url)
movie_search = BeautifulSoup(response.text,'html.parser')
result = movie_search.select('li div.release_info')

for r in result:
    if r.find("a", {'class':'btn_s_time no_select'}) is None:
        print('-------------')
        movie_name = ((r.select('div.release_movie_name a'))[0])
        print(movie_name.text)
        movie_url = movie_name.get('href')
        movie_id = re.compile(r'-?\d*$').search(movie_url).group(0)[1:]
        print('+++++++++++++++++++++')
        print(movie_id)
