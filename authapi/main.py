from typing import List

from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session

from . import crud, models, schemas, database
# from .database import SessionLocal, engine
# from authapi import database

# database.Base.metadata.create_all(bind=engine)
from .database import db_state_default


database.db.connect()
database.db.create_tables([models.User])
database.db.close()


app = FastAPI()

sleep_time = 10


async def reset_db_state():
    database.db._state._state.set(db_state_default.copy())
    database.db._state.reset()


# Dependency
def get_db(db_state=Depends(reset_db_state)):
    try:
        database.db.connect()
        yield
    finally:
        if not database.db.is_closed():
            database.db.close()


@app.post("/users/", response_model=schemas.User, dependencies=[Depends(get_db)])
def create_user(user: schemas.UserCreate):
    db_user = crud.get_user_by_email(email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    return crud.create_user(user=user)


@app.get("/users/", response_model=List[schemas.User], dependencies=[Depends(get_db)])
def read_users(skip: int = 0, limit: int = 100):
    users = crud.get_users(skip=skip, limit=limit)
    return users


@app.get("/users/{user_id}", response_model=schemas.User, dependencies=[Depends(get_db)])
def read_user(user_id: int):
    db_user = crud.get_user(user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user



# @app.post("/authenticate", response_model=schemas.Token)
# def authenticate_user(user: schemas.UserAuthenticate, db: Session = Depends(get_db)):
#     db_user = crud.get_user_by_email(db, email=user.email)
#     if db_user is None:
#         raise HTTPException(status_code=400, detail="Email not existed")
#     else:
#         is_password_correct = crud.check_email_password(db, user)
#         if is_password_correct is False:
#             raise HTTPException(status_code=400, detail="Password is not correct")
#         else:
#             from datetime import timedelta
#             access_token_expires = timedelta(minutes=15)
#             from authapi.crud import create_access_token
#             access_token = create_access_token(
#                 data={"sub": user.email}, expires_delta=access_token_expires)
#             return {"access_token": access_token, "token_type": "Bearer"}