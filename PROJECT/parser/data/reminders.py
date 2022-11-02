import sqlalchemy
from .db_session import SqlAlchemyBase


class Reminder(SqlAlchemyBase):
    __tablename__ = 'reminders'
    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True, autoincrement=True)
    user_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("users.id"))
    medicine_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("medicines.id"))
    date_time = sqlalchemy.Column(sqlalchemy.DateTime)
    periodicity = sqlalchemy.Column(sqlalchemy.Integer, nullable=True)
