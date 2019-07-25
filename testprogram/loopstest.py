from bs4 import BeautifulSoup
import requests

tag_list = list()
for i in range(100):
    url ='https://simonsu.postach.io/{}'.format(i)
    response = requests.get(url)
    soup = BeautifulSoup(response.text , 'html.parser')
    tag_name = soup.select('a.permalink')
    if len(tag_name)<1:
        break
    for tn in tag_name:
        tag_list.append([tn.text,tn.get('href')])

print(tag_list)
    
