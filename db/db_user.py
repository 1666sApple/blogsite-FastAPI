from sqlalchemy.orm.session import Session
from db.hash import Hash
from db.models import DBusers
from schemas import UserBase

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