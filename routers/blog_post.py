from fastapi import FastAPI, APIRouter
from typing import Optional
from pydantic import BaseModel

router = APIRouter(
    prefix='/blog',
    tags=['blog']
)

class BlogModel(BaseModel):
    title: str
    content: str
    nb_comments: int
    published: Optional[bool]
    
@router.post('/new')
def create_blog(blog: BlogModel):
    return {'data': blog}