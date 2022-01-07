from typing import List
from fastapi import Depends, FastAPI, HTTPException, Request
from fastapi.responses import JSONResponse
from fastapi_jwt_auth import AuthJWT
from fastapi_jwt_auth.exceptions import AuthJWTException
import crud 
import models
import schemas
import database
from pydantic import BaseModel
from database import db_state_default
from celery_worker import get_ip_details

class Settings(BaseModel):
    authjwt_secret_key: str = "secret"

@AuthJWT.load_config
def get_config():
    return Settings()


database.db.connect()
database.db.create_tables([models.User, models.Task])
database.db.close()


app = FastAPI()

sleep_time = 10


async def reset_db_state():
    database.db._state._state.set(db_state_default.copy())
    database.db._state.reset()


def get_db(db_state=Depends(reset_db_state)):
    try:
        database.db.connect()
        yield
    finally:
        if not database.db.is_closed():
            database.db.close()


@app.exception_handler(AuthJWTException)
def authjwt_exception_handler(request: Request, exc: AuthJWTException):
    return JSONResponse(
        status_code=exc.status_code,
        content={"detail": exc.message}
    )


@app.post("/signup/", response_model=schemas.User, dependencies=[Depends(get_db)])
def create_user(user: schemas.UserCreate):
    db_user = crud.get_user_by_email(email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    return crud.create_user(user=user)


@app.get("/users/", response_model=List[schemas.User], dependencies=[Depends(get_db)])
def read_users(skip: int = 0, limit: int = 100):
    users = crud.get_users(skip=skip, limit=limit)
    return users


@app.get("/user/{user_id}", response_model=schemas.User, dependencies=[Depends(get_db)])
def read_user(user_id: int):
    db_user = crud.get_user(user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user



@app.post("/login")
def login(user: schemas.UserAuthenticate, Authorize: AuthJWT = Depends()):
    db_user = crud.get_user_by_email(email=user.email)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    access_token = Authorize.create_access_token(subject=user.email)
    refresh_token = Authorize.create_refresh_token(subject=user.email)
    return {"access_token": access_token, "refresh_token": refresh_token}


@app.post('/refresh')
def refresh(Authorize: AuthJWT = Depends()):
    Authorize.jwt_refresh_token_required()
    current_user = Authorize.get_jwt_subject()
    new_access_token = Authorize.create_access_token(subject=current_user)
    return {"access_token": new_access_token}


@app.get('/user')
def protected(Authorize: AuthJWT = Depends()):
    Authorize.jwt_required()
    current_user = Authorize.get_jwt_subject()
    db_user = crud.get_user_by_email(email=current_user)
    return {"email": db_user.email, "first_name": db_user.first_name, "last_name": db_user.last_name, "is_active": db_user.is_active}


@app.post("/task/", dependencies=[Depends(get_db)])
def create_task(Authorize: AuthJWT = Depends()):
    Authorize.jwt_required()
    task = crud.create_task()
    current_user = Authorize.get_jwt_subject()
    get_ip_details.delay(current_user)
    return {'id': str(task.id)}