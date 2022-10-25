import datetime
import sqlalchemy
from .db_session import SqlAlchemyBase


class User(SqlAlchemyBase):  # база данных пользователей
    __tablename__ = 'users'
    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    full_name = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    weight = sqlalchemy.Column(sqlalchemy.Integer, nullable=True)
    height = sqlalchemy.Column(sqlalchemy.Integer, nullable=True)
    birthday = sqlalchemy.Column(sqlalchemy.DateTime, nullable=True)
    password_hash = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    created_date = sqlalchemy.Column(sqlalchemy.DateTime, default=datetime.datetime.now)
