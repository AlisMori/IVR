import requests


def test_make_new_user_with_correct_data():
    assert requests.post("http://127.0.0.1:5000/users/make_new",
                         json={'full_name': 'Chelovek', 'password': '123123', 'weight': '90', 'birthday': '10.11.1994',
                               'height': '150'}).text not in ('IncorrectData', '401')


def test_make_already_existing_user():
    assert requests.post("http://127.0.0.1:5000/users/make_new",
                         json={'full_name': 'Chelovek', 'password': '123123', 'weight': '90', 'birthday': '10.11.1994',
                               'height': '150'}).text == '401'


def test_login_correct():
    assert requests.post("http://127.0.0.1:5000/users/login",
                         json={'full_name': 'Chelovek', 'password': '123123'}).text != '401'


def test_login_incorrect_password():
    assert requests.post("http://127.0.0.1:5000/users/login",
                         json={'full_name': 'Chelovek', 'password': '1231223'}).text == '401'


def test_login_incorrect_login():
    assert requests.post("http://127.0.0.1:5000/users/login",
                         json={'full_name': 'Chelovek321', 'password': '123123'}).reason == 'INTERNAL SERVER ERROR'

