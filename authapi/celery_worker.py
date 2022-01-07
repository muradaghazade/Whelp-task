from time import sleep
from celery import Celery
from celery.utils.log import get_task_logger
from models import User, Task

from requests import get

celery = Celery('tasks', broker='amqp://guest:guest@127.0.0.1:5672//')

celery_log = get_task_logger(__name__)


@celery.task
def get_ip_details(user, task):
    from ipdata import ipdata
    ip = get('https://api.ipify.org').content.decode('utf8')
    ipdata = ipdata.IPData('711208fb9c48844a077f6d18e818d20db5954d83280f3be03f2c9cdf')
    response = ipdata.lookup(ip)
    print(type(response))
    user = User.select().where(User.email == user).get()
    user.ip_details = response
    user.save()
    task = Task.select().where(Task.id == task).get()
    task.status = "Compeleted"
    task.save()
    return {"message": "Okay"}




















# from celery import Celery
# from celery.utils.log import get_task_logger

# # Create the celery app and get the logger
# celery_app = Celery('tasks', broker='amqp://guest@localhost//')
# logger = get_task_logger(__name__)


# @celery_app.task
# def add(x, y):
#     res = x + y
#     logger.info("Adding %s + %s, res: %s" % (x, y, res))
#     return res