from sqlalchemy import Column, Integer, String, Boolean, DateTime, ARRAY
from database import Base

class User(Base): #table to store users
    __tablename__ = 'users'
    id = Column(String, primary_key=True, index=True) #index=True is used to make the column searchable
    email = Column(String, unique=True, index=True, nullable=False) #nullable=False is used to make the column required
    full_name = Column(String, nullable=False) 
    password = Column(String, nullable=False)
    is_admin = Column(Boolean, default=False) #is_admin represents if the user is an admin -> default is False
    

class Profile(Base): #table to store profiles of users
    __tablename__ = 'profiles'
    id = Column(String, primary_key=True, index=True)
    phone_number = Column(String, nullable=True) #optional
    country = Column(String, nullable=True) #optional
    city = Column(String, nullable=True) #optional
    describe_yourself = Column(String, nullable=False) #required
    interests_and_passions = Column(String, nullable=False) #required
    past_volunteer_experience = Column(String, nullable=False) #required
    events_registered = Column(ARRAY(Integer), nullable=True) #optional -> stores the ids of the events the user has registered for
    

class Event(Base): #table to store volunteer events
    __tablename__ = 'events'
    id = Column(String, primary_key=True, index=True)
    title = Column(String, nullable=False) #required
    dates = Column(String, nullable=False) #required
    location = Column(String, nullable=False) #required
    description = Column(String, nullable=False) #required
    tasks = Column(String, nullable=False) #required
    users_registered = Column(ARRAY(Integer), nullable=True) #optional -> stores the ids of the users who have registered for the event
    