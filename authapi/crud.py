import models
import schemas
import bcrypt


def get_user(user_id: int):
    return models.User.filter(models.User.id == user_id).first()


def get_user_by_email(email: str):
    return models.User.filter(models.User.email == email).first()


def get_users(skip: int = 0, limit: int = 100):
    return list(models.User.select().offset(skip).limit(limit))


def create_user(user: schemas.UserCreate):
    fake_hashed_password = bcrypt.hashpw(user.password.encode('utf-8'), bcrypt.gensalt())
    db_user = models.User(email=user.email, hashed_password=fake_hashed_password, first_name=user.first_name, last_name=user.last_name)
    db_user.save()
    return db_user


def create_task():
    db_task = models.Task()
    db_task.save()
    return db_task


def get_task(task_id: int):
    return models.Task.filter(models.Task.id == task_id).first()
