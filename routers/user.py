from fastapi import APIRouter, Depends
from sqlalchemy.orm.session import Session

from db import db_user
from db.database import get_db
from schemas import UserBase, UserDisplay

router = APIRouter(
    prefix='/user',
    tags=['user']
)

@router.post('/', response_model=UserDisplay)
def createUser(request: UserBase, db: Session = Depends(get_db)):
    return db_user.createUser(db, request)