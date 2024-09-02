from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm.session import Session

from db import db_user
from db.database import getDB
from schemas import UserBase, UserDisplay

router = APIRouter(
    prefix='/user',
    tags=['user']
)

@router.post('/', response_model=UserDisplay)
def createUser(request: UserBase, db: Session = Depends(getDB)):
    user = db_user.createUser(db, request)
    if not user:
        raise HTTPException(status_code=400, detail="Username or email already exists")
    return user
    
@router.get('/', response_model=List[UserDisplay])
def readUser(db: Session = Depends(getDB)):
    return db_user.getAllUsers(db)
    
@router.get('/{id}', response_model=UserDisplay)
def readOneUser(id: int, db: Session = Depends(getDB)):
    user = db_user.getUser(db, id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user
    
@router.put('/{id}/update', response_model=UserDisplay)
def updateUser(id: int, request: UserBase, db: Session = Depends(getDB)):
    user = db_user.updateUser(db, id, request)
    if not user:
        raise HTTPException(status_code=404, detail="User not found or not updated")
    return user
    
@router.delete('/{id}/delete')
def deleteUser(id: int, db: Session = Depends(getDB)):
    user = db_user.deleteUser(db, id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return {"detail": "User deleted successfully"}
