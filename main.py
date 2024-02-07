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


#call this endpoint to get all information about a user
#expecting the email of the user as a string
#returning a JSON with all the information about the user - see format below 
@app.get('/user/get_user')
def get_user(email: str, db: Session = Depends(get_session)):
    user = db.query(models.User).filter(models.User.email == email).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='User not found')
    
    return {'email': user.email,
            'full_name': user.full_name,
            'age': user.age,
            'gender': user.gender,
            'phone_number': user.phone_number,
            'work_status': user.work_status,
            'immigration_status': user.immigration_status,
            'skills': user.skills,
            'interests': user.interests,
            'past_volunteer_experience': user.past_volunteer_experience,
            'events_registered': user.events_registered #note this is a list of event ids, can be empty
            }


#call this endpoint to update the information about a user
#when a user calls them, show them their profile with all their current info filled in -> send me the entire profile with all fields and I will update
#in the DB -> this way you don't need to specify which fields are being updated as I will simply be updating all fields
#expecting a JSON in the schema of UserCreate
#returning a JSON with a success message in the form {'message': message} or an error message if any of the updated values are invalid
@app.post('/user/update_user')
def update_user(request: schemas.UserCreate, db: Session = Depends(get_session)):
    user = db.query(models.User).filter(models.User.email == request.email).first()
    
    if not user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='User not found')
    if request.age <= 0:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='Please enter a valid value for Age')
    if request.gender.lower() not in schemas.profile_choices['gender']:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='Please enter a valid value for Gender: M or F')
    if request.work_status.lower() not in schemas.profile_choices['work_status']:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='Please enter a valid value for Work Status: Student, Employed, or Unemployed')
    if request.immigration_status.lower() not in schemas.profile_choices['immigration_status']:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='Please enter a valid value for Immigration Status: Citizen, PR, Student Visa, or Other')
    
    user.email = request.email
    user.full_name = request.full_name
    user.password = get_password_hash(request.password)
    user.age = request.age
    user.gender = request.gender
    user.phone_number = request.phone_number
    user.work_status = request.work_status
    user.immigration_status = request.immigration_status
    user.skills = request.skills
    user.interests = request.interests
    user.past_volunteer_experience = request.past_volunteer_experience
    
    db.commit()
    return {'message': 'User and Profile updated successfully'}


#call this endpoint to delete a user
#expecting the email of the user as a string
#returning a JSON with a success message in the form {'message': message} or an error message if user not found
@app.post('/user/delete_user')
def delete_user(email: str, db: Session = Depends(get_session)):
    user = db.query(models.User).filter(models.User.email == email).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='User not found')
    
    db.delete(user)
    db.commit()
    return {'message': 'User and Profile deleted successfully'}


#call this endpoint to check if user is an admin
#expecting the email of the user as a string
#returning a JSON with a boolean value in the form {'is_admin': is_admin} or an error message if user not found
@app.get('/user/is_admin')
def is_admin(email: str, db: Session = Depends(get_session)):
    user = db.query(models.User).filter(models.User.email == email).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='User not found')
    
    return {'is_admin': user.is_admin}



    
