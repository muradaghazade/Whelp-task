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
# def create_access_token(*, data: dict, expires_delta: timedelta = None):
#     secret_key = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
#     algorithm = "HS256"
#     to_encode = data.copy()
#     if expires_delta:
#         expire = datetime.utcnow() + expires_delta
#     else:
#         expire = datetime.utcnow() + timedelta(minutes=15)
#     to_encode.update({"exp": expire})
#     encoded_jwt = jwt.encode(to_encode, secret_key, algorithm=algorithm)
#     return encoded_jwt


# def check_email_password(user: schemas.UserAuthenticate):
#     db_user_info: models.User = get_user_by_email(db, email=user.email)
#     print(user.password.encode('utf-8'), '___1')
#     print(db_user_info.hashed_password, "___2")
#     return bcrypt.checkpw(user.password.encode('utf-8'), db_user_info.hashed_password)