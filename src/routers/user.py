from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm.session import Session

from src.db import db_user
from src.db.database import getDB
from src.schemas import UserBase, UserDisplay

router = APIRouter(prefix='/user', tags=['user'])

@router.post('/', response_model=UserDisplay)
def create_user(request: UserBase, db: Session = Depends(getDB)):
    user = db_user.create_user(db, request)
    if not user:
        raise HTTPException(status_code=400, detail="Username or email already exists")
    return user
    
@router.get('/', response_model=List[UserDisplay])
def read_users(db: Session = Depends(getDB)):
    return db_user.get_all_users(db)

@router.get('/{id}', response_model=UserDisplay)
def read_user(id: int, db: Session = Depends(getDB)):
    user = db_user.get_user(db, id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user
    
@router.put('/{id}/update', response_model=UserDisplay)
def update_user(id: int, request: UserBase, db: Session = Depends(getDB)):
    user = db_user.update_user(db, id, request)
    if not user:
        raise HTTPException(status_code=404, detail="User not found or not updated")
    return user
    
@router.delete('/{id}/delete')
def delete_user(id: int, db: Session = Depends(getDB)):
    user = db_user.delete_user(db, id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return {"detail": "User deleted successfully"}
