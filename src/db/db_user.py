from fastapi import HTTPException
from sqlalchemy.orm.session import Session
from src.db.hash import Hash
from src.db.models import DBusers
from src.schemas import UserBase

def createUser(db: Session, request: UserBase):
    user = db.query(DBusers).filter((DBusers.username == request.username) | (DBusers.email == request.email)).first()
    if user:
        return None
    
    newUser = DBusers(
        username=request.username,
        email=request.email,
        password=Hash.bcrypt(request.password)
    )
    
    db.add(newUser)
    db.commit()
    db.refresh(newUser)
    
    return newUser

def getAllUsers(db: Session):
    return db.query(DBusers).all()

def getUser(db: Session, id: int):
    return db.query(DBusers).filter(DBusers.id == id).first()

def getUserByUsername(db: Session, username: str):
    user = db.query(DBusers).filter(DBusers.username == username).first()
    if not user:
        raise HTTPException(
            status_code=404,
            detail=f"User with username '{username}' not found"
        )
    return user

def updateUser(db: Session, id: int, request: UserBase):
    user = db.query(DBusers).filter(DBusers.id == id).first()
    if not user:
        raise HTTPException(
            status_code=404,
            detail="User not found"
        )
        
    user.username = request.username
    user.email = request.email
    user.password = Hash.bcrypt(request.password)
    
    db.commit()
    db.refresh(user)
    return 'User updated!'

def deleteUser(db: Session, id: int):
    user = db.query(DBusers).filter(DBusers.id == id).first()
    if not user:
        raise HTTPException(
            status_code=404,
            detail="User not found"
        )
    
    db.delete(user)
    db.commit()
    return 'User deleted!'
