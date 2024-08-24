from fastapi import FastAPI, APIRouter, Query
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
    
@router.post('/new/{id}')
def create_blog(blog: BlogModel, id: int, version: int):
    return {
        'id': id,
        'data': blog,
        'version': version
    }
    
@router.post('/new/{id}/comment')
def create_comment(
    blog: BlogModel,
    id: int,
    comment_id: int = Query(None,
        title='Id of the comment',
        description = 'Description for the comment',
        alias = 'commentId'
    )
):
    return {
        'blog': blog,
        'title': id,
        'comment_id': comment_id
    }