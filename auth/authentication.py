import stat
from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from auth import oauth2
from db import models
from db.database import getDB
from db.models import DBusers
from db.hash import Hash

router = APIRouter(
    tags=['authentication']
)

@router.post('/token')
def getToken(
    request: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(getDB)
):
    # Query the user by username
    user = db.query(models.DBusers).filter(models.DBusers.username == request.username).first()
    
    # Check if the user exists
    if not user:
        raise HTTPException(status_code=404, detail='User not found')
    
    # Verify the password
    if not Hash.verify(user.password, request.password):
        raise HTTPException(status_code=401, detail='Incorrect password!')

    # Create access token
    accessToken = oauth2.createAccessToken(data={'sub': user.username})

    # Return the token response
    return {
        'accessToken': accessToken,
        'tokenType': 'bearer',
        'userID': user.id,
        'username': user.username
    }