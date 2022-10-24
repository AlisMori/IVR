from flask import Flask, request
from data import db_session
from data.users import User
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
                    birthday=datetime.datetime.strptime(request_data['birthday'], '%m.%d.%Y'),
                    weight=request_data['weight'],
                    height=request_data['height'])
        session.add(user)
        session.commit()
        session.close()
        print(user)
        return '201'


@app.route('/users/login', methods=['POST'])
def login():  # проверка и вход пользователя
    request_data = request.get_json()
    session = db_session.create_session()
    user = session.query(User).filter(User.full_name == request_data['full_name']).first()
    if werkzeug.security.check_password_hash(user.password_hash, request_data['password']):
        return '201'
    else:
        return '401'


def main():
    app.run()


if __name__ == '__main__':
    main()
