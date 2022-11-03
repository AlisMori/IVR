import requests
from bs4 import BeautifulSoup


def list_incomp(med):
    r = requests.get(f"https://www.vidal.ru/search?t=all&q={med}&bad=on",
                     headers={'User-agent': 'your bot 0.1'})
    soup = BeautifulSoup(r.text, features="html.parser")

    lekarstva = soup.find("td", class_='products-table-name').a['href']
    r = requests.get("https://www.vidal.ru" + lekarstva)
    soup = BeautifulSoup(r.text, features="html.parser")
    r = requests.get("https://www.vidal.ru" + soup.find_all('a', class_='btn-red')[1]['href'])
    if soup.find_all('a', class_='btn-red')[1]['href'] != '#':
        soup = BeautifulSoup(r.text, features="html.parser")

        drugs = []
        for i in soup.find('table', class_='products-table molecules').find_all('tr'):
            if i.find('a'):
                if 'class' not in i.find('a').attrs and 'Таб.' not in i.find('a').text and 'Сусп.' not in i.find(
                        'a').text and 'Капс.' not in i.find('a').text:
                    drugs.append(i.find('a').text)

        return drugs
    else:
        return ''
