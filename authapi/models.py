import peewee

from .database import db


class User(peewee.Model):
    # id = peewee.AutoField()
    first_name = peewee.CharField()
    last_name = peewee.CharField()
    email = peewee.CharField(unique=True, index=True)
    hashed_password = peewee.CharField()
    is_active = peewee.BooleanField(default=True)

    class Meta:
        database = db



print(User.select())


















# import os

# from peewee import *
# from playhouse.db_url import connect

# mysql_db = MySQLDatabase('my_database')

# db = connect('mysql://user:password@localhost:3306/my_database')

# class BaseModel(Model):
#     """A base model that will use our MySQL database"""
#     class Meta:
#         database = mysql_db

# class User(BaseModel):
#     username = CharField()
#     # etc, etc



# # from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
# # from sqlalchemy.orm import relationship

# # from .database import Base


# # class User(Base):
# #     __tablename__ = "users"

# #     id = Column(Integer, primary_key=True, index=True)
# #     email = Column(String, unique=True, index=True)
# #     first_name = Column(String)
# #     last_name = Column(String)
# #     hashed_password = Column(String)
# #     is_active = Column(Boolean, default=True)
