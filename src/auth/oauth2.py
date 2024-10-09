# auth/oauth2.py

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from typing import Optional
from datetime import datetime, timedelta
from jose import JWTError, jwt
from sqlalchemy.orm import Session
from src.db.database import getDB
from src.db.models import DBusers
from src.schemas import User

oauth2Scheme = OAuth2PasswordBearer(tokenUrl='token')

SECRET_KEY = 'd1050c1f9e0ea5a34d37408b1fe78276835d286ca1f5001e0f1e90c558ddff28'
ALGORITHM = 'HS256'
ACCESS_TOKEN_EXPIRE_MINUTES = 300

def createAccessToken(data: dict, expiresDelta: Optional[timedelta] = None):
    toEncode = data.copy()
    if expiresDelta:
        expire = datetime.utcnow() + expiresDelta
    else:
        expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    
    toEncode.update({'exp': expire})
    encodedJwt = jwt.encode(toEncode, SECRET_KEY, algorithm=ALGORITHM)
    return encodedJwt

def getCurrentUser(token: str = Depends(oauth2Scheme), db: Session = Depends(getDB)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail='Could not validate credentials',
        headers={'WWW-Authenticate': 'Bearer'}
    )
    
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get('sub')
        if username is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception

    user = db.query(DBusers).filter(DBusers.username == username).first()
    if user is None:
        raise credentials_exception

    return user

def getCurrentActiveUser(currentUser: User = Depends(getCurrentUser)):
    if not currentUser.is_active:
        raise HTTPException(status_code=400, detail = 'Inactive User')

    return currentUser