import requests
from bs4 import BeautifulSoup


def find_interaction(drug_1, drug_2):
    try:
        r = requests.get(f"https://www.vidal.ru/search?t=all&q={drug_1}&bad=on",
                         headers={'User-agent': 'your bot 0.1'})
        soup = BeautifulSoup(r.text, features="html.parser")
        drugs = soup.find("td", class_='products-table-name').a['href']
        r = requests.get("https://www.vidal.ru" + drugs)
        soup = BeautifulSoup(r.text, features="html.parser")
        drug1 = soup.find('div', class_='block-content composition').find('table').find_all('tr')[1].td
        r = requests.get(f"https://www.vidal.ru/search?t=molecule&q={drug1.text}&bad=on")
        soup = BeautifulSoup(r.text, features="html.parser")
        med1_id = soup.find('td', class_='molecule-name').a['href'].split('/')[-1]

        r = requests.get(f"https://www.vidal.ru/search?q={drug_2}&bad=on",
                         headers={'User-agent': 'your bot 0.1'})
        soup = BeautifulSoup(r.text, features="html.parser")
        drugs = soup.find("td", class_='products-table-name').a['href']
        r = requests.get("https://www.vidal.ru" + drugs)
        soup = BeautifulSoup(r.text, features="html.parser")
        med2 = soup.find('div', class_='block-content composition').find('table').find_all('tr')[1].td
        r = requests.get(f"https://www.vidal.ru/search?t=molecule&q={med2.text}&bad=on")
        soup = BeautifulSoup(r.text, features="html.parser")
        med2_id = soup.find('td', class_='molecule-name').a['href'].split('/')[-1]

        r = requests.get(f"https://www.vidal.ru/drugs/ni-interaction/molecule/{med1_id}/{med2_id}")
        soup = BeautifulSoup(r.text, features="html.parser")

        if soup.find('div', class_='not-found'):
            return ''
        else:
            res = soup.find('div', class_='block-content').text
            words = res.split()
            res = " ".join(sorted(set(words), key=words.index))
            return res
    except AttributeError:
        return ''
