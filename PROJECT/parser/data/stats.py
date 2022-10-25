import datetime
import sqlalchemy
from .db_session import SqlAlchemyBase


class Stats(SqlAlchemyBase):  # база данных со статистиками пользователей
    __tablename__ = 'stats'

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    user_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("users.id"))
    weight = sqlalchemy.Column(sqlalchemy.Integer, nullable=True)
    pressure_s = sqlalchemy.Column(sqlalchemy.Integer, nullable=True)
    pressure_d = sqlalchemy.Column(sqlalchemy.Integer, nullable=True)
    glucose = sqlalchemy.Column(sqlalchemy.Float, nullable=True)
    created_date = sqlalchemy.Column(sqlalchemy.DateTime, default=datetime.datetime.now)
