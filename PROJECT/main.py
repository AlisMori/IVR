from kivy.lang import Builder
from kivymd.app import MDApp
from kivymd.uix.pickers import MDDatePicker
from kivy.uix.screenmanager import ScreenManager, Screen
import bs4
import requests
from datetime import datetime
import find_info


class Med(MDApp):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.screen = Builder.load_file('main.kv')
        self.theme_cls.material_style = "M3"
        self.signup_sc = Builder.load_file('signup_screen.kv')
        self.login_sc = Builder.load_file('login_screen.kv')

    def signup(self):  # регистрация пользователя
        # чтение введеных пользователем данных
        user = self.signup_sc.ids.username.text
        pw = self.signup_sc.ids.password.text
        birthday = self.signup_sc.ids.birthday.text
        weight = self.signup_sc.ids.weight.text
        height = self.signup_sc.ids.height.text

        # проверка данных на "адекватность"
        if datetime.strptime(birthday, '%d.%m.%Y') > datetime.now():
            self.signup_sc.ids.birthday.error = True
        if int(weight) > 500:
            self.signup_sc.ids.weight.error = True
        if int(height) > 400:
            self.signup_sc.ids.height.error = True
        else:  # добавление в бд, если данные "адекватные"
            response = requests.post("http://127.0.0.1:5000/users/make_new",
                                     json={'full_name': f'{user}', 'password': f'{pw}', 'weight': f'{weight}',
                                           'birthday': f'{birthday}', 'height': f'{height}'})
            if response.text == '401':  # ошибка если такой пользователь уже существует
                self.signup_sc.ids.username.error = True
            elif response.text == '201':
                self.root.current = 'main'

    def login(self):  # вход
        user = self.login_sc.ids.username.text
        pw = self.login_sc.ids.password.text
        response = requests.post("http://127.0.0.1:5000/users/login",
                                 json={'full_name': f'{user}', 'password': f'{pw}'})

        if response.text == '401':  # ошибка если пароль неправильный
            self.login_sc.ids.password.error = True
        elif response.text == '201':
            self.root.current = 'main
            self.screen.ids.username.text = user

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

    def comp(self): # проверка на взаимодействие двух препаратов (вывод совместимы/несовместимы)
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
        pass

    def get_profile(self):
        pass

    def build(self):  # основная функция класса
        sm = ScreenManager()
        sm.add_widget(Builder.load_file('welcome.kv'))
        sm.add_widget(self.signup_sc)
        sm.add_widget(self.login_sc)
        sm.add_widget(self.screen)

        return sm


if __name__ == "__main__":
    Med().run()
