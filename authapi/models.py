import peewee

from database import db


class User(peewee.Model):
    first_name = peewee.CharField()
    last_name = peewee.CharField()
    email = peewee.CharField(unique=True, index=True)
    hashed_password = peewee.CharField()
    ip_details = peewee.CharField(default="Empty")
    is_active = peewee.BooleanField(default=True)
    

    class Meta:
        database = db


class Task(peewee.Model):
    status = peewee.CharField(default="Not Completed")

    class Meta:
        database = db
