from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session
from src.auth.oauth2 import createAccessToken
from src.db.database import getDB
from src.db.db_user import getUserByUsername
from src.db.hash import Hash

router = APIRouter(prefix='/auth', tags=['auth'])

class TokenResponse(BaseModel):
    access_token: str
    token_type: str

@router.post('/token', response_model=TokenResponse)
def login(username: str, password: str, db: Session = Depends(getDB)):
    user = getUserByUsername(db, username)
    if not user or not Hash.verify(user.password, password):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    
    access_token = createAccessToken(data={"sub": username})
    return {"access_token": access_token, "token_type": "bearer"}
