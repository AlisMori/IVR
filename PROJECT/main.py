from kivy.lang import Builder
from kivymd.app import MDApp
from kivymd.uix.pickers import MDDatePicker
from kivy.uix.screenmanager import ScreenManager
import requests
from datetime import datetime
import find_info
import subprocess
import sys
from threading import Thread


class Med(MDApp):
    user_id = ''

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.screen = Builder.load_file('main.kv')
        self.theme_cls.material_style = "M3"
        self.signup_sc = Builder.load_file('signup_screen.kv')
        self.login_sc = Builder.load_file('login_screen.kv')
        self.home_drugs = Builder.load_file('home_drugs.kv')

    def signup(self):  # регистрация пользователя
        # чтение введеных пользователем данных
        user = self.signup_sc.ids.username.text
        pw = self.signup_sc.ids.password.text
        birthday = self.signup_sc.ids.birthday.text
        weight = self.signup_sc.ids.weight.text
        height = self.signup_sc.ids.height.text

        # проверка данных на "адекватность"
        if datetime.strptime(birthday, '%m.%d.%Y') > datetime.now():
            self.signup_sc.ids.birthday.error = True
        if int(weight) > 500:
            self.signup_sc.ids.weight.error = True
        if int(height) > 400:
            self.signup_sc.ids.height.error = True
        else:  # добавление в бд, если данные "адекватные"
            response = requests.post("http://127.0.0.1:5000/users/make_new",
                                     json={'full_name': f'{user}', 'password': f'{pw}', 'weight': f'{weight}',
                                           'birthday': f'{birthday}', 'height': f'{height}'})
            if response.text == '401' or response.text == '500':  # ошибка если такой пользователь уже существует
                self.signup_sc.ids.username.error = True
            else:
                global user_id
                user_id = response.text
                self.root.current = 'main'

    def login(self):  # вход
        user = self.login_sc.ids.username.text
        pw = self.login_sc.ids.password.text
        response = requests.post("http://127.0.0.1:5000/users/login",
                                 json={'full_name': f'{user}', 'password': f'{pw}'})

        if response.text == '401' or response.reason == 'INTERNAL SERVER ERROR':  # ошибка если пароль неправильный
            self.login_sc.ids.password.error = True
        else:
            global user_id
            user_id = response.text
            self.root.current = 'main'

    def info(self):  # вывод описания, показаний и противопоказаний к применению введеного препарата
        name = self.screen.ids.drug.text
        description = find_info.info(name)
        indications = find_info.indication(name)
        contraindications = find_info.contraindication(name)
        if not description and not indications and not contraindications:
            self.screen.ids.info.text = 'Препарат не найден'
            self.screen.ids.indications.text = 'Препарат не найден'
            self.screen.ids.contraindications.text = 'Препарат не найден'
            self.screen.ids.drug.error = True
        else:
            self.screen.ids.info.text = description
            self.screen.ids.indications.text = indications
            self.screen.ids.contraindications.text = contraindications

    def incomp(self):  # вывод несовместимых препаратов с данным
        self.screen.ids.list_med.text = 'List of drugs'

    def comp(self):  # проверка на взаимодействие двух препаратов (вывод совместимы/несовместимы)
        self.screen.ids.compatibility.text = 'УРААА'

    def on_save(self, instance, value, date_range):
        self.screen.ids.date.text = f'{str(date_range[0])} - {str(date_range[-1])}'

    def on_cancel(self, instance, value):
        self.screen.ids.date.text = "You clicked Cancel"

    def calendar(self):
        date_dialog = MDDatePicker(mode='range')
        date_dialog.bind(on_save=self.on_save, on_cancel=self.on_cancel)
        date_dialog.open()

    def graph(self):
        weight = self.screen.ids.weight_stat.text
        presure_s = self.screen.ids.pressure_s.text
        presure_d = self.screen.ids.pressure_d.text
        glucose = self.screen.ids.glucose.text
        if int(weight) > 500:
            self.screen.ids.weight.error = True
        if 90 > int(presure_s) or int(presure_s) > 200:
            self.screen.ids.pressure_s.error = True
        if 60 > int(presure_d) or int(presure_d) > 100:
            self.screen.ids.pressure_d.error = True
        if 3.3 > float(glucose) or float(glucose) > 7.8:
            self.screen.ids.glucose.error = True
        else:
            global user_id
            response = requests.post("http://127.0.0.1:5000/users/stats",
                                     json={'user_id': f'{user_id}', 'weight': f'{weight}', 'pressure_s': f'{presure_s}',
                                           'pressure_d': f'{presure_d}', 'glucose': f'{glucose}'})
            if response.text == '201':
                Thread(target=lambda *largs: subprocess.run([sys.executable, "diagram.py"])).start()

    def get_profile(self):
        global user_id
        response = requests.get("http://127.0.0.1:5000/users/user", json={'id': user_id})
        ls = response.json()
        self.screen.ids.username.text = ls[0]
        birthday = datetime.strptime(ls[1][:-13], '%a, %d %b %Y').strftime('%d.%m.%Y')
        self.screen.ids.birthday.text = f'Дата рождения: {birthday}'
        self.screen.ids.weight.text = f'Вес: {ls[2]}'
        self.screen.ids.height.text = f'Рост: {ls[3]}'

    def add_med(self):
        global user_id
        drug = self.home_drugs.ids.drug.text
        url = find_info.find_url(drug)
        if url == '':
            self.home_drugs.ids.drug.error = True
        else:
            requests.post("http://127.0.0.1:5000/medicines/add_medicines",
                          json={'user_id': f'{user_id}', 'name': f'{drug}'})
            response = requests.get("http://127.0.0.1:5000/medicines/get_medicines", json={'id': user_id})
            ls = response.json()
            self.home_drugs.ids.table.text = '\n'.join(ls)

    def show_med(self):
        global user_id
        response = requests.get("http://127.0.0.1:5000/medicines/get_medicines", json={'id': user_id})
        if response:
            ls = response.json()
            self.home_drugs.ids.table.text = '\n'.join(ls)

    def build(self):  # основная функция класса
        sm = ScreenManager()
        sm.add_widget(Builder.load_file('welcome.kv'))
        sm.add_widget(self.signup_sc)
        sm.add_widget(self.login_sc)
        sm.add_widget(self.screen)
        sm.add_widget(self.home_drugs)

        return sm


if __name__ == "__main__":
    Med().run()
