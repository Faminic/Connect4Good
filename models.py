from sqlalchemy import Column, Integer, String, Boolean, DateTime, ARRAY
from database import Base

class User(Base): #table to store users - all fields required
    __tablename__ = 'users'
    id = Column(String, primary_key=True, index=True) #index=True is used to make the column searchable
    email = Column(String, unique=True, index=True, nullable=False) #nullable=False is used to make the column required
    full_name = Column(String, nullable=False) 
    password = Column(String, nullable=False)
    is_admin = Column(Boolean, default=False) #is_admin represents if the user is an admin -> default is False
    

class Profile(Base): #table to store profiles of users - all fields are required
    __tablename__ = 'profiles'
    id = Column(String, primary_key=True, index=True)
    age = Column(Integer, nullable=False)
    gender = Column(String, nullable=False)
    phone_number = Column(String, nullable=False) 
    work_status = Column(String, nullable=False) 
    immigration_status = Column(String, nullable=False)
    skills = Column(String, nullable=False) 
    interests = Column(String, nullable=False)
    past_volunteer_experience = Column(String, nullable=False)
    events_registered = Column(ARRAY(Integer), default=[]) #stores the ids of the events the user has registered for -> default is empty
    

class Event(Base): #table to store volunteer events - all fields required
    __tablename__ = 'events'
    id = Column(String, primary_key=True, index=True)
    title = Column(String, nullable=False) 
    dates = Column(String, nullable=False)
    location = Column(String, nullable=False)
    description = Column(String, nullable=False)
    tasks = Column(String, nullable=False)
    users_registered = Column(ARRAY(Integer), default=[]) #stores the ids of the users who have registered for the event -> default is empty
    