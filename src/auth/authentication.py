from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from src.auth import oauth2
from src.db import models
from src.db.database import getDB
from src.db.hash import Hash

router = APIRouter(
    tags=['authentication']
)

@router.post('/token')
def getToken(
    request: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(getDB)
):
    user = db.query(models.DBusers).filter(models.DBusers.username == request.username).first()

    if not user:
        raise HTTPException(status_code=404, detail='User not found')
    
    if not Hash.verify(user.password, request.password):
        raise HTTPException(status_code=401, detail='Incorrect password')

    accessToken = oauth2.createAccessToken(data={'sub': user.username})

    return {
        'access_token': accessToken,
        'token_type': 'bearer',
        'user_id': user.id,
        'username': user.username
    }
