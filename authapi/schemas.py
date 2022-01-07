from typing import List, Optional, Any

import peewee
from pydantic import BaseModel
from pydantic.utils import GetterDict


class PeeweeGetterDict(GetterDict):
    def get(self, key: Any, default: Any = None):
        res = getattr(self._obj, key, default)
        if isinstance(res, peewee.ModelSelect):
            return list(res)
        return res


class UserBase(BaseModel):
    email: str
    first_name: str
    last_name: str


class UserCreate(UserBase):
    password: str
    

class User(UserBase):
    id: int
    is_active: bool
    ip_details: str

    class Config:
        orm_mode = True


class UserAuthenticate(BaseModel):
    password: str
    email: str


# class TaskCreate(BaseModel):
#     pass

class Task(BaseModel):
    id: int