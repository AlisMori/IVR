import sqlalchemy
from .db_session import SqlAlchemyBase


class Medicine(SqlAlchemyBase):
    __tablename__ = 'medicines'
    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True, autoincrement=True)
    name = sqlalchemy.Column(sqlalchemy.String, nullable=False)
    user_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("users.id"))
