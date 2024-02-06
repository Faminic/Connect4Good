from fastapi import FastAPI, Depends, HTTPException, status
from sqlalchemy.orm import Session
import schemas, models #schemas represents format expecting from frontend, models represents database format
from database import Base, engine, SessionLocal
from utils import get_password_hash, verify_password, reset_db
import uuid

Base.metadata.create_all(bind=engine) #creates the tables in the database if they don't exist

def get_session(): #function to get the database session
    session = SessionLocal()
    try:
        yield session
    finally:
        session.close()

app = FastAPI()


#call this endpoint to register a user
#expecting a JSON in the schema of UserCreate
#returning a JSON with a success message in the form {'message': message} or an error message if user already exists
@app.post('/register') 
def register_user(request: schemas.UserCreate, db: Session = Depends(get_session)):
    check_existing = db.query(models.User).filter(models.User.email == request.email).first() 
    if check_existing:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='Email already registered')

    unique_id = str(uuid.uuid4())
    password = get_password_hash(request.password)
    
    if request.age <= 0:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='Please enter a valid value for Age')
    if request.gender.lower() not in schemas.profile_choices['gender']:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='Please enter a valid value for Gender: M or F')
    if request.work_status.lower() not in schemas.profile_choices['work_status']:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='Please enter a valid value for Work Status: Student, Employed, or Unemployed')
    if request.immigration_status.lower() not in schemas.profile_choices['immigration_status']:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='Please enter a valid value for Immigration Status: Citizen, PR, Student Visa, or Other')
        
    new_user = models.User(id=unique_id, email=request.email, full_name=request.full_name, password=password, age=request.age, gender=request.gender, phone_number=request.phone_number, work_status=request.work_status, immigration_status=request.immigration_status, skills=request.skills, interests=request.interests, past_volunteer_experience=request.past_volunteer_experience)
    
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    
    return {'message': 'User and Profile registered successfully'}


#call this endpoint to login a user
#expecting a JSON in the schema of UserLogin
#returning a JSON with a success message in the form {'message': message} or an error message if email or password is incorrect
@app.post('/login')
def login_user(request: schemas.UserLogin, db: Session = Depends(get_session)):
    user = db.query(models.User).filter(models.User.email == request.email).first() 
    if not user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='Incorrect Email')
    
    hashed_password = user.password
    if not verify_password(request.password, hashed_password):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='Incorrect Password')
    
    return {'message': 'Login successful'}

#call this endpoint to reset the database -> fully deletes and recreates the tables
#not expecting any input
#returning a JSON with a success message in the form {'message': message}
@app.post('/reset_db')
def reset_database():
    reset_db()
    return {'message': 'Database reset successfully'}





