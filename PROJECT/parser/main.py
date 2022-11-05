from flask import Flask, request
from data import db_session
from data.users import User
from data.stats import Stats
from data.medicines import Medicine
from data.reminders import Reminder
import werkzeug
import datetime

app = Flask(__name__)

app.config['SECRET_KEY'] = 'alis_mori'

db_session.global_init("db/baza.sqlite")


@app.route('/users/make_new', methods=['POST'])
def make_new():  # проверка и создание нового пользователя
    request_data = request.get_json()
    session = db_session.create_session()
    if session.query(User).filter(User.full_name == request_data['full_name']).first():
        session.close()
        return '401'
    else:
        user = User(full_name=request_data['full_name'],
                    password_hash=werkzeug.security.generate_password_hash(request_data['password']),
                    birthday=datetime.datetime.strptime(request_data['birthday'], '%d.%m.%Y'),
                    weight=request_data['weight'],
                    height=request_data['height'])
        session.add(user)
        session.commit()
        stat = Stats(user_id=user.id,
                     weight=request_data['weight'])
        session.add(stat)
        session.commit()
        print(user)
        return str(user.id)


@app.route('/users/login', methods=['POST'])
def login():  # проверка и вход пользователя
    request_data = request.get_json()
    session = db_session.create_session()
    user = session.query(User).filter(User.full_name == request_data['full_name']).first()
    if werkzeug.security.check_password_hash(user.password_hash, request_data['password']):
        return str(user.id)
    else:
        return '401'


@app.route('/users/stats', methods=['POST'])
def stats():  # добавление статистики в бд
    request_data = request.get_json()
    session = db_session.create_session()
    stat = Stats(user_id=request_data['user_id'],
                 weight=request_data['weight'],
                 pressure_s=request_data['pressure_s'],
                 pressure_d=request_data['pressure_d'],
                 glucose=request_data['glucose'])
    session.add(stat)
    session.commit()
    session.close()
    return '201'


@app.route('/users/get_stats', methods=['GET'])
def get_stats():
    request_data = request.get_json()
    session = db_session.create_session()
    user_stats = session.query(Stats).filter(Stats.user_id == request_data['id']).all()
    data = []
    for i in range(len(user_stats)):
        data.append([user_stats[i].weight, user_stats[i].pressure_s, user_stats[i].pressure_d, user_stats[i].glucose,
                     user_stats[i].created_date])
    return data


@app.route('/medicines/add_medicines', methods=['POST'])
def add_medicines():  # Добавление препаратов в отдельную бд. Создание "домашняя аптечка"
    request_data = request.get_json()
    session = db_session.create_session()
    medicine = Medicine(user_id=request_data['user_id'],
                        name=request_data['name'], )
    session.add(medicine)
    session.commit()
    session.close()
    return '201'


@app.route('/medicine/add_reminder', methods=['POST'])
def add_reminder():
    request_data = request.get_json()
    session = db_session.create_session()
    reminder = Reminder(user_id=request_data['user_id'],
                        medicine_id=request_data['medicine_id'],
                        date_time=datetime.datetime.strptime(request_data['date_time'], '%Y-%m-%d %H:%M:%S'),
                        periodicity=request_data['periodicity'])
    session.add(reminder)
    session.commit()
    session.close()
    return '201'


@app.route('/medicine/check_reminder', methods=['GET'])
def check_reminder():  # Уведомления о приеме препарата
    request_data = request.get_json()
    session = db_session.create_session()
    datet = session.query(Reminder).filter(Reminder.user_id == request_data['user_id']).order_by(
        Reminder.date_time).first()
    if (datetime.datetime.strptime(str(datet.date_time),
                                   '%Y-%m-%d %H:%M:%S') - datetime.datetime.now()) <= datetime.timedelta(minutes=15):
        print(datet.date_time)
        datet.date_time = datet.date_time + datetime.timedelta(minutes=datet.periodicity)
        print(datet.date_time)
        session.add(datet)
        session.commit()

        return session.query(Medicine).filter(Medicine.id == datet.medicine_id).first().name
    else:
        return 'No'


@app.route('/users/user', methods=['GET'])
def user():  # Получение информации о пользователе
    request_data = request.get_json()
    session = db_session.create_session()
    user = session.query(User).filter(User.id == request_data['id']).first()
    info = [user.full_name, user.birthday, user.weight, user.height]
    return info


@app.route('/medicines/get_medicines', methods=['GET'])
def get_medicines():  # Получение данных "домашняя аптечка"
    request_data = request.get_json()
    session = db_session.create_session()
    med = session.query(Medicine).filter(Medicine.user_id == request_data['id']).all()
    data = {}
    for i in range(len(med)):
        data.update({med[i].name: med[i].id})
    return data


def main():
    app.run()


if __name__ == '__main__':
    main()
