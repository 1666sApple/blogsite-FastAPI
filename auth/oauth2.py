from fastapi.security import OAuth2PasswordBearer
from typing import Optional
from datetime import datetime, timedelta
from jose import jwt

oauth2Scheme = OAuth2PasswordBearer(tokenUrl = 'token')

SECRET_KEY = '45eef581866da63e4f39809238d8f31c376ca92f3bb4e5bbf9489a480f5f5644'
ALGORITHM = 'HS256'
ACCESS_TOKEN_TOKEN_EXPIRE_MINUTES = 30

def createAccessToken(data: dict, expiresDelta: Optional[timedelta] = None):
    toEncode = data.copy()
    if expiresDelta:
        expire = datetime.utcnow() + expiresDelta
    else:
        expire = datetime.utcnow() + timedelta(minutes = 15)
    toEncode.update({
        'exp': expire
    })
    encodedJwt = jwt.encode(toEncode, SECRET_KEY, algorithm=ALGORITHM)
    return encodedJwt