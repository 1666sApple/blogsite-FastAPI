from typing_extensions import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm.session import Session

from db import db_user
from db.database import get_db
from db.models import DBusers
from schemas import UserBase, UserDisplay

router = APIRouter(
    prefix='/user',
    tags=['user']
)

@router.post('/', response_model=UserDisplay)
def createUser(request: UserBase, db: Session = Depends(get_db)):
    user = db_user.createUser(db, request)
    if not user:
        raise HTTPException(status_code=400, detail="Username or email already exists")
    return user
    
@router.get('/', response_model=List[UserDisplay])
def readUser(db: Session = Depends(get_db)):
    return db_user.getAllUsers(db)
    
@router.get('/{id}', response_model=UserDisplay)
def readOneuser(id: int, db: Session = Depends(get_db)):
    return db_user.getUser(db, id)