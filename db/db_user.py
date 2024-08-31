from sqlalchemy.orm.session import Session
from db.hash import Hash
from db.models import DBusers
from schemas import UserBase

def createUser(db: Session, request: UserBase):
    newUser = DBusers(
        username = request.username,
        email = request.email,
        password = Hash.bcrypt(request.password)
    )
    
    db.add(newUser)
    db.commit()
    db.refresh(newUser)
    
    return newUser