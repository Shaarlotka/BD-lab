from bs4 import BeautifulSoup
import requests
from time import sleep

url = 'https://gatherer.wizards.com/Pages/Search/Default.aspx?name=+['

def getCardImage(url, cardName):
    sleep(2)
    HEADERS = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.163 Safari/537.36'}

    url += cardName + ']'

    responce = requests.get(url, headers=HEADERS)
    soup = BeautifulSoup(responce.content, 'html.parser')
    items = soup.findAll('div', class_='cardList')
    comps = []

    for i, item in enumerate(items):
        comps.append(item.find('img').get('src'))
        break

    if comps:
        comps[0] = 'https://gatherer.wizards.com' + comps[0][5:]
        
    print(comps)

    image = requests.get(url, stream=True)

    file = open('C:/magic/%s.png' % cardName, 'bw')
    for chunk in image.iter_content(4096):
        file.write(chunk)

    return comps #при получении значения тоже проверяй, не пустой ли массив
                 #если пустой - отправляй строку "NULL", чтобы функция в sql поставила все по дефолту
                 #если не пустой то все норм

getCardImage(url, 'bolas') #это просто пример - 'bolas' типа имя карты, которое ввел пользователь при добавлении данных
