import requests
from bs4 import BeautifulSoup


url = 'https://map.tgos.tw/TGOSCloud/Web/Map/TGOSViewer_Map.aspx?addr={}'.format('新北市樹林區大雅路330號')
response = requests.get(url)
response = BeautifulSoup(response.text,'html.parser')
print(response)

