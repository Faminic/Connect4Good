from pydantic import BaseModel
import datetime

class UserCreate(BaseModel): #what data format I expect when user creates an account
    email: str
    full_name: str
    password: str

class UserLogin(BaseModel): #what data format I expect when user logs in
    email: str
    password: str