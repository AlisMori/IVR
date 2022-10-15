from kivy.lang import Builder
from kivymd.app import MDApp
from kivymd.uix.pickers import MDDatePicker
import bs4
import requests


class Med(MDApp):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.screen = Builder.load_file('main.kv')
        self.theme_cls.material_style = "M3"

    def formatting(self, temp):
        ls = []
        for i in temp:
            desc = i.text
            desc = desc.replace('\r', ' ')
            desc = desc.replace('\n', ' ')
            ls.append(" ".join(desc.split()))
            return "\n".join(ls)

    def find_url(self, name):
        url = f"https://www.rlsnet.ru/search_result.htm?word={name}"
        r = requests.get(url, headers={'User-agent': 'your bot 0.1'})
        soup = bs4.BeautifulSoup(r.text, 'lxml')

        medications = list(filter(lambda x: len(x['class']) == 1, soup.find_all("ul")[20].find_all("a", class_="link")))

        for i in medications:
            namemed = i.text.replace('®', '').lower()
            if namemed == name:
                return i['href']

    def info(self):
        name = self.screen.ids.drug.text
        url = self.find_url(name)
        page = requests.get(url, headers={'User-agent': 'your bot 0.1'})
        soup = bs4.BeautifulSoup(page.text, 'lxml')
        info_1 = soup.find("div", {"id": "fc64"})
        desc = info_1.find_all("p", class_="Opis_Pole")
        self.screen.ids.info.text = self.formatting(desc)
        info_2 = soup.find("div", {"id": "fc4096"})
        indi = info_2.find_all("p", class_="Opis_Pole")
        self.screen.ids.indications.text = self.formatting(indi)
        info_3 = soup.find("div", {"id": "fc8192"})
        contra = info_3.find_all("p", class_="Opis_Pole")
        self.screen.ids.contraindications.text = self.formatting(contra)

    def incomp(self):
        self.screen.ids.list_med.text = 'List of drugs'

    def comp(self):
        self.screen.ids.compatibility.text = 'УРААА'

    def on_save(self, instance, value, date_range):
        self.screen.ids.date.text = f'{str(date_range[0])} - {str(date_range[-1])}'

    def on_cancel(self, instance, value):
        self.screen.ids.date.text = "You clicked Cancel"

    def calendar(self):
        date_dialog = MDDatePicker(mode='range')
        date_dialog.bind(on_save=self.on_save, on_cancel=self.on_cancel)
        date_dialog.open()

    def build(self):
        return self.screen


if __name__ == "__main__":
    Med().run()
