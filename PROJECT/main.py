from kivy.lang import Builder
from kivymd.app import MDApp
from kivymd.uix.pickers import MDDatePicker, MDTimePicker
from kivy.uix.screenmanager import ScreenManager
import requests
from datetime import datetime
import find_info
import find_incomp
import find_comp
import diagram
from kivy.garden.notification import Notification
from threading import Timer


class Med(MDApp):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.screen = Builder.load_file('main.kv')
        self.theme_cls.material_style = "M3"
        self.signup_sc = Builder.load_file('signup_screen.kv')
        self.login_sc = Builder.load_file('login_screen.kv')
        self.home_drugs = Builder.load_file('home_drugs.kv')
        self.user_id = ''

    def signup(self):  # регистрация пользователя
        # чтение введеных пользователем данных
        user = self.signup_sc.ids.username.text
        pw = self.signup_sc.ids.password.text
        birthday = self.signup_sc.ids.birthday.text
        weight = self.signup_sc.ids.weight.text
        height = self.signup_sc.ids.height.text

        # проверка данных на "адекватность"
        if not self.date_test(birthday):
            self.signup_sc.ids.birthday.error = True
        elif int(weight) > 500:
            self.signup_sc.ids.weight.error = True
        elif int(height) > 400:
            self.signup_sc.ids.height.error = True
        else:  # добавление в бд, если данные "адекватные"
            response = requests.post("http://127.0.0.1:5000/users/make_new",
                                     json={'full_name': f'{user}', 'password': f'{pw}', 'weight': f'{weight}',
                                           'birthday': f'{birthday}', 'height': f'{height}'})
            if response.text == '401' or response.text == '500':  # ошибка если такой пользователь уже существует
                self.signup_sc.ids.username.error = True
            else:
                self.user_id = response.text
                self.root.current = 'main'
                self.check_remind()

    def date_test(self, date):
        try:
            datetime.strptime(date, '%d.%m.%Y')
            if date < datetime.now():
                return True
            else:
                return False
        except ValueError:
            return False

    def login(self):  # вход
        user = self.login_sc.ids.username.text
        pw = self.login_sc.ids.password.text
        response = requests.post("http://127.0.0.1:5000/users/login",
                                 json={'full_name': f'{user}', 'password': f'{pw}'})

        if response.text == '401' or response.reason == 'INTERNAL SERVER ERROR':  # ошибка если пароль неправильный
            self.login_sc.ids.password.error = True
        else:
            self.user_id = response.text
            self.root.current = 'main'
            self.check_remind()

    def info(self):  # вывод описания, показаний и противопоказаний к применению введеного препарата
        name = self.screen.ids.drug.text
        description = find_info.info(name.lower())
        indications = find_info.indication(name.lower())
        contraindications = find_info.contraindication(name.lower())
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
        drug = self.screen.ids.incomp_drug.text
        incomp = find_incomp.list_incomp(drug.lower())
        if incomp == '':
            self.screen.ids.list_med.text = 'Информация не найдена'
        else:
            self.screen.ids.list_med.text = '\n'.join(incomp)

    def comp(self):  # проверка на взаимодействие двух препаратов
        drug_1 = self.screen.ids.drug_1.text
        drug_2 = self.screen.ids.drug_2.text
        result = find_comp.find_interaction(drug_1.lower(), drug_2.lower())
        if result != '':
            self.screen.ids.compatibility.text = f'Степень серьезности/тяжести взаимодействия: {result.lower()}'
        else:
            self.screen.ids.compatibility.text = 'Степень серьезности/тяжести взаимодействия: информация не найдена'

    def timer(self, instance, value, date_range):  # выбор времени по средствам виджита TimePiker
        self.screen.ids.date.text = str(value)
        time_dialog = MDTimePicker()
        time_dialog.bind(on_save=self.on_save, on_cancel=self.on_cancel)
        time_dialog.open()

    def on_save(self, instance, value):
        self.screen.ids.time.text = str(value)

    def on_cancel(self, instance, value):  # при нажатии кнопки cancel
        self.screen.ids.date.text = "Необходимо выбрать дату"
        self.screen.ids.time.text = "Необходимо выбрать время"

    def calendar(self):  # выбор даты по средствам виджита DatePiker
        date_dialog = MDDatePicker()
        date_dialog.bind(on_save=self.timer, on_cancel=self.on_cancel)
        date_dialog.open()

    def add_stats(self):  # добавление статистики в БД
        weight = self.screen.ids.weight_stat.text
        presure_s = self.screen.ids.pressure_s.text
        presure_d = self.screen.ids.pressure_d.text
        glucose = self.screen.ids.glucose.text
        if int(weight) > 500:  # проверка введенных данных на "адекватность"
            self.screen.ids.weight.error = True
        elif 90 > int(presure_s) or int(presure_s) > 200:
            self.screen.ids.pressure_s.error = True
        elif 60 > int(presure_d) or int(presure_d) > 100:
            self.screen.ids.pressure_d.error = True
        elif 3.3 > float(glucose) or float(glucose) > 7.8:
            self.screen.ids.glucose.error = True
        else:
            response = requests.post("http://127.0.0.1:5000/users/stats",
                                     json={'user_id': f'{self.user_id}', 'weight': f'{weight}',
                                           'pressure_s': f'{presure_s}',
                                           'pressure_d': f'{presure_d}', 'glucose': f'{glucose}'})
            if response.text == '201':
                self.screen.ids.stats_status.text = 'Данные добавлены'

    def graph(self):  # отрисовка диаграмм по данным из БД
        diagram.graph(self.user_id)

    def get_profile(self):  # вывод данных на страницу профиля
        response = requests.get("http://127.0.0.1:5000/users/user", json={'id': self.user_id})
        ls = response.json()
        self.screen.ids.username.text = ls[0]
        birthday = datetime.strptime(ls[1][:-13], '%a, %d %b %Y').strftime('%d.%m.%Y')
        self.screen.ids.birthday.text = f'Дата рождения: {birthday}'
        self.screen.ids.weight.text = f'Вес: {ls[2]}'
        self.screen.ids.height.text = f'Рост: {ls[3]}'

    def add_med(self):  # добавление препаратов в "домашнюю аптечку"
        drug = self.home_drugs.ids.drug.text
        url = find_info.find_url(drug)
        response = requests.get("http://127.0.0.1:5000/medicines/get_medicines", json={'id': self.user_id})
        listt = response.json()
        if url == '' or drug in listt.values():
            self.home_drugs.ids.drug.error = True
        else:
            requests.post("http://127.0.0.1:5000/medicines/add_medicines",
                          json={'user_id': f'{self.user_id}', 'name': f'{drug}'})
            response_new = requests.get("http://127.0.0.1:5000/medicines/get_medicines", json={'id': self.user_id})
            ls = response_new.json()
            self.home_drugs.ids.table.text = '\n'.join(ls.keys())

    def show_med(self):  # отображение препаратов из "Домашней аптечки"
        response = requests.get("http://127.0.0.1:5000/medicines/get_medicines", json={'id': self.user_id})
        if response:
            ls = response.json()
            self.home_drugs.ids.table.text = '\n'.join(ls.keys())

    def remind(self):  # добавление напоминания в бд о приеме препарата
        date_r = self.screen.ids.date.text
        time_r = self.screen.ids.time.text
        periodicity = self.screen.ids.periodicity.text
        drug = self.screen.ids.drugs.text
        datet = date_r + ' ' + time_r
        response = requests.get("http://127.0.0.1:5000/medicines/get_medicines", json={'id': self.user_id})
        if response:
            ls = response.json()
            if drug in ls.keys():  # проверка есть ли введеный препарат в "Домашней аптечке"
                response_r = requests.post("http://127.0.0.1:5000/medicine/add_reminder",
                                           json={'user_id': self.user_id, 'medicine_id': ls[drug.lower()],
                                                 'date_time': datet, 'periodicity': periodicity})
                if response_r.text == '201':
                    self.screen.ids.remind_s.text = 'Напоминание создано'
            else:
                self.screen.ids.drugs.error = True

    def check_remind(self):  # проверка необходимости уведомления о приеме препарата
        response = requests.get("http://127.0.0.1:5000/medicine/check_reminder",
                                json={'user_id': self.user_id})
        # print(response.text)
        if response.text != 'No' and response.reason != 'INTERNAL SERVER ERROR':
            Notification().open(title='MedNoti',
                                message=f'Скоро время приема препарата {response.text}')

        Timer(300, self.check_remind).start()  # каждые 5 минут возвращается к этой функции

    def build(self):  # основная функция класса
        sm = ScreenManager()
        sm.add_widget(Builder.load_file('welcome.kv'))
        sm.add_widget(self.signup_sc)
        sm.add_widget(self.login_sc)
        sm.add_widget(self.screen)
        sm.add_widget(self.home_drugs)
        sm.add_widget(Builder.load_file('graph.kv'))

        return sm


if __name__ == "__main__":
    Med().run()
