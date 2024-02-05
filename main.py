from fastapi import FastAPI, Depends, HTTPException, status
from sqlalchemy.orm import Session
import schemas, models #schemas represents format expecting from frontend, models represents database format
from database import Base, engine, SessionLocal
from utils import get_password_hash, verify_password
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
def register_user(user: schemas.UserCreate, db: Session = Depends(get_session)):
    #check if the user already exists
    check_existing = db.query(models.User).filter(models.User.email == user.email).first() 
    if check_existing:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='Email already registered')

    #create a new user
    unique_id = str(uuid.uuid4())
    password = get_password_hash(user.password)
    new_user = models.User(id=unique_id, email=user.email, full_name=user.full_name, password=password)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    
    return {'message': 'User registered successfully'}
    

    
        

