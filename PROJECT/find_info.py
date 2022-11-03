import bs4
import requests


def formatting(temp):  # форматирует найденую информацию в красивый вид
    temp = temp.replace('\r', '')
    temp = temp.replace('\n', ' ')
    return temp


def find_url(name):  # поиск необходимой url
    try:
        url = f"https://www.rlsnet.ru/search_result.htm?word={name}"
        r = requests.get(url, headers={'User-agent': 'your bot 0.1'})
        soup = bs4.BeautifulSoup(r.text, 'lxml')

        medications = list(filter(lambda x: len(x['class']) == 1, soup.find_all("ul")[20].find_all("a", class_="link")))
        if medications:
            for i in medications:
                namemed = i.text.replace('®', '').lower()
                if namemed == name:
                    return i['href']
        else:
            return ''
    except IndexError:
        return ''


def info(drug):  # вывод описания препарата
    url = find_url(drug)
    if url == '':
        return None
    else:
        page = requests.get(url, headers={'User-agent': 'your bot 0.1'})
        soup = bs4.BeautifulSoup(page.text, 'lxml')
        if soup.find('h2', id='opisanie-lekarstvennoi-formy'):
            info = soup.find('h2', id='opisanie-lekarstvennoi-formy').find_next('p').find_parent('div')
            return formatting(info.get_text())
        else:
            return 'Информация не найдена'


def indication(drug):  # вывод показаний к применению препарата
    url = find_url(drug)
    if url == '':
        return None
    else:
        page = requests.get(url, headers={'User-agent': 'your bot 0.1'})
        soup = bs4.BeautifulSoup(page.text, 'lxml')
        if soup.find('h2', id='pokazaniya'):
            indi = soup.find('h2', id='pokazaniya').find_next('p').find_parent('div')
        else:
            indi = soup.find('h2', id='pokazaniya-k-primeneniyu').find_next('p').find_parent('div')
        return formatting(indi.get_text())


def contraindication(drug):  # поиск противопоказаний к применению препарата
    url = find_url(drug)
    if url == '':
        return None
    else:
        page = requests.get(url, headers={'User-agent': 'your bot 0.1'})
        soup = bs4.BeautifulSoup(page.text, 'lxml')
        contra = soup.find('h2', id='protivopokazaniya').find_next('p').find_parent('div')
        return formatting(contra.get_text())
