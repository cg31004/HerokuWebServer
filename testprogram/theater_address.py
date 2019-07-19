# import requests
# from bs4 import BeautifulSoup
# import re

# url = "https://www.google.com/search?q={}".format('國賓影城(台北長春廣場)')
# # url = 'https://movies.yahoo.com.tw/ajax/pc/get_schedule_by_movie?movie_id=9467&date=2019-07-17'
# response = requests.get(url)
# theater_search = BeautifulSoup(response.text,'html.parser')
# address = ((theater_search.select('div.AVsepf span.BNeawe.tAd8D.AP7Wnd'))[0]).text
# print(address)

# 'AreaList-1952slimofy.tkBeautifoulikeslimofy.tk123'




c = 'AreaList-1952slimofy.tkBeautifoull-1982slimofy.tk'
area = 'AreaList-'
beauti = 'Beautifoull-'

i = c.split('slimofy.tk')
# b = x if 'AreaList-' else 'Beautifoul' for x in i

b = [ x if beauti in x else None for x in i ]

print(b)
# max = lambda m, n: m if m > n else n
# max = lambda b:b[i] if  area in b[i] for i in range(len(b))
def zz(b):
    for i in b:
        if area in i: 
            return i 
# print(zz(b))



