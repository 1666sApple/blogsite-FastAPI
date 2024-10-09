from typing import List, Optional
from pydantic import BaseModel
from datetime import datetime

class UserBase(BaseModel):
    username: str
    email: str
    password: str

class User(BaseModel):
    id: int
    username: str
    email: str

    class Config:
        orm_mode = True

class Article(BaseModel):
    title: str
    content: str
    published: bool
    
    class Config:
        orm_mode = True

class UserDisplay(BaseModel):
    username: str
    email: str
    items: List[Article] = []
    
    class Config:
        orm_mode = True

class ArticleBase(BaseModel):
    title: str
    content: str
    published: bool
    userID: int

class ArticleDisplay(BaseModel):
    id: int
    title: str
    content: str
    published: bool
    user: Optional[User] = None
    
    class Config:
        orm_mode = True

class FileResponse(BaseModel):
    id: int
    originalFileName: str
    contentType: str
    uploadTime: datetime

    class Config:
        orm_mode = True