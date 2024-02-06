from pydantic import BaseModel, StringConstraints
from typing import Annotated
import datetime

class UserCreate(BaseModel): #what data format I expect when user creates an account
    email: str
    full_name: str
    password: str
    age: int
    gender: Annotated[str, StringConstraints(max_length=1)] #can be 'M' or 'F'
    phone_number: str
    work_status: str
    immigration_status: str
    skills: str
    interests: str
    past_volunteer_experience: str

class UserLogin(BaseModel): #what data format I expect when user logs in
    email: str
    password: str
    
#key is field name, value is list of possible values
profile_choices = {'gender': ['m', 'f'], 'work_status': ['student', 'employed', 'unemployed'], 'immigration_status': ['citizen', 'pr', 'student visa' , 'other']}