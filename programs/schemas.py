from pydantic import BaseModel
from typing import List, Optional


class Program(BaseModel):
    title: str
    body: str
    
    class Config:
        orm_mode = True


class User(BaseModel):
    name: str
    email: str
    password: str


class ShowUser(BaseModel):
    name: str
    email: str

    class Config:
        orm_mode = True


class ShowUserPrograms(ShowUser):
    programs: List[Program]


class ShowProgram(BaseModel):
    title: str
    body: str
    creator: ShowUser

    class Config:
        orm_mode = True


class Login(BaseModel):
    username: str
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    email: Optional[str] = None